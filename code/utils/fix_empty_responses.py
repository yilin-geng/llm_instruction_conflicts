#!/usr/bin/env python3
"""
Script to identify and fix empty or abnormal LLM responses in experiment results.

This script:
1. Scans a timestamped results directory for response files
2. Identifies empty, null, or abnormally short responses
3. Recalls the corresponding LLMs to regenerate missing responses
4. Provides a detailed report of fixes applied

Usage:
    python fix_empty_responses.py /path/to/results/20250730_233805
    python fix_empty_responses.py /path/to/results/20250730_233805 --min-length 10 --dry-run
"""

import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Tuple, Set
import argparse
from datetime import datetime
import shutil
from tqdm import tqdm

# Import the existing LLM infrastructure
from llmclient import Next_Client, OpenAI_Client
from api_keys import NEXT_BASE_URL, NEXT_API_KEY, OPENAI_API_KEY

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ResponseFixer:
    def __init__(self, results_dir: Path, min_response_length: int = 5, 
                 next_base_url: str = NEXT_BASE_URL, max_requests_per_minute: int = 20):
        self.results_dir = Path(results_dir)
        self.min_response_length = min_response_length
        self.next_base_url = next_base_url
        self.max_requests_per_minute = max_requests_per_minute
        
        # Statistics
        self.stats = {
            'files_processed': 0,
            'total_responses': 0,
            'empty_responses': 0,
            'short_responses': 0,
            'null_responses': 0,
            'regenerated_responses': 0,
            'failed_regenerations': 0,
            'files_with_issues': set(),
            'models_used': set()
        }
        
        # Cache for LLM clients
        self._llm_clients = {}
        
    def is_abnormal_response(self, response: str) -> Tuple[bool, str]:
        """
        Check if a response is abnormal (empty, null, or too short).
        
        Returns:
            Tuple of (is_abnormal, reason)
        """
        if response is None:
            return True, "null"
        
        if not isinstance(response, str):
            return True, "non_string"
            
        if response.strip() == "":
            return True, "empty"
            
        if len(response.strip()) < self.min_response_length:
            return True, "too_short"
            
        # Check for common error patterns
        error_patterns = [
            "error",
            "failed to generate",
            "timeout",
            "rate limit",
            "api error",
            "connection error"
        ]
        
        response_lower = response.lower()
        for pattern in error_patterns:
            if pattern in response_lower:
                return True, f"error_pattern_{pattern.replace(' ', '_')}"
                
        return False, "normal"
    
    def get_llm_client(self, model: str, use_next_client: bool = True):
        """Get or create an LLM client for the specified model."""
        if model in self._llm_clients:
            return self._llm_clients[model]
            
        if use_next_client:
            api_config = {
                "NEXT_BASE_URL": self.next_base_url,
                "NEXT_API_KEY": NEXT_API_KEY,
                "OPENAI_API_KEY": OPENAI_API_KEY,
            }
            client = Next_Client(
                model=model, 
                api_config=api_config, 
                max_requests_per_minute=self.max_requests_per_minute
            )
        else:
            # For OpenAI models, use OpenAI client directly
            if "gpt" in model.lower():
                api_config = {"OPENAI_API_KEY": OPENAI_API_KEY}
                client = OpenAI_Client(
                    model=model,
                    api_config=api_config,
                    max_requests_per_minute=self.max_requests_per_minute
                )
            else:
                # Use Next client for other models
                api_config = {
                    "NEXT_BASE_URL": self.next_base_url,
                    "NEXT_API_KEY": NEXT_API_KEY,
                    "OPENAI_API_KEY": OPENAI_API_KEY,
                }
                client = Next_Client(
                    model=model, 
                    api_config=api_config, 
                    max_requests_per_minute=self.max_requests_per_minute
                )
        
        self._llm_clients[model] = client
        return client
    
    def regenerate_response(self, model: str, input_data: List[Dict], temperature: float = None) -> str:
        """Regenerate a single response using the appropriate LLM client."""
        try:
            client = self.get_llm_client(model, use_next_client=True)
            
            # Prepare messages for single call
            messages = [input_data]
            
            if temperature is not None:
                responses = client.multi_call(messages, temperature=temperature)
            else:
                responses = client.multi_call(messages)
                
            if responses and len(responses) > 0:
                return responses[0] if responses[0] else ""
            else:
                return ""
                
        except Exception as e:
            logger.error(f"Failed to regenerate response for model {model}: {e}")
            return ""
    
    def scan_response_file(self, file_path: Path) -> Tuple[List[Dict], List[int]]:
        """
        Scan a response file and identify problematic responses.
        
        Returns:
            Tuple of (all_responses, indices_of_abnormal_responses)
        """
        try:
            responses = []
            abnormal_indices = []
            
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f):
                    try:
                        data = json.loads(line.strip())
                        responses.append(data)
                        
                        response_text = data.get('response', '')
                        is_abnormal, reason = self.is_abnormal_response(response_text)
                        
                        if is_abnormal:
                            abnormal_indices.append(line_num)
                            if reason == "null":
                                self.stats['null_responses'] += 1
                            elif reason == "empty":
                                self.stats['empty_responses'] += 1
                            elif reason == "too_short":
                                self.stats['short_responses'] += 1
                            
                            logger.debug(f"Found abnormal response in {file_path}:{line_num} - {reason}")
                        
                        self.stats['total_responses'] += 1
                        
                    except json.JSONDecodeError as e:
                        logger.error(f"JSON decode error in {file_path}:{line_num}: {e}")
                        abnormal_indices.append(line_num)
                        
            return responses, abnormal_indices
            
        except Exception as e:
            logger.error(f"Error scanning file {file_path}: {e}")
            return [], []
    
    def fix_response_file(self, file_path: Path, dry_run: bool = False) -> Dict:
        """
        Fix abnormal responses in a single file.
        
        Returns:
            Dictionary with fix results
        """
        logger.info(f"Processing {file_path.name}")
        
        responses, abnormal_indices = self.scan_response_file(file_path)
        
        if not abnormal_indices:
            logger.info(f"No abnormal responses found in {file_path.name}")
            return {
                'file': file_path.name,
                'total_responses': len(responses),
                'abnormal_responses': 0,
                'regenerated': 0,
                'failed': 0
            }
        
        logger.info(f"Found {len(abnormal_indices)} abnormal responses in {file_path.name}")
        self.stats['files_with_issues'].add(file_path.name)
        
        if dry_run:
            return {
                'file': file_path.name,
                'total_responses': len(responses),
                'abnormal_responses': len(abnormal_indices),
                'regenerated': 0,
                'failed': 0,
                'dry_run': True
            }
        
        # Create backup
        backup_path = file_path.with_suffix(f'.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.jsonl')
        shutil.copy2(file_path, backup_path)
        logger.info(f"Created backup: {backup_path.name}")
        
        # Fix abnormal responses
        regenerated = 0
        failed = 0
        
        for idx in tqdm(abnormal_indices, desc=f"Fixing {file_path.name}"):
            if idx >= len(responses):
                continue
                
            response_data = responses[idx]
            model = response_data.get('model', '')
            input_data = response_data.get('input_data', [])
            
            if not model or not input_data:
                logger.warning(f"Missing model or input_data in response {idx}")
                failed += 1
                continue
            
            self.stats['models_used'].add(model)
            
            # Try to regenerate
            logger.debug(f"Regenerating response {idx} for model {model}")
            new_response = self.regenerate_response(model, input_data)
            
            if new_response and not self.is_abnormal_response(new_response)[0]:
                responses[idx]['response'] = new_response
                regenerated += 1
                self.stats['regenerated_responses'] += 1
                logger.debug(f"Successfully regenerated response {idx}")
            else:
                failed += 1
                self.stats['failed_regenerations'] += 1
                logger.warning(f"Failed to regenerate response {idx}")
        
        # Write fixed responses back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            for response in responses:
                f.write(json.dumps(response, ensure_ascii=False) + '\n')
        
        logger.info(f"Fixed {regenerated} responses in {file_path.name} ({failed} failed)")
        
        return {
            'file': file_path.name,
            'total_responses': len(responses),
            'abnormal_responses': len(abnormal_indices),
            'regenerated': regenerated,
            'failed': failed,
            'backup_created': backup_path.name
        }
    
    def process_directory(self, dry_run: bool = False) -> List[Dict]:
        """Process all response files in the results directory."""
        if not self.results_dir.exists():
            raise ValueError(f"Results directory does not exist: {self.results_dir}")
        
        # Find all .jsonl files that look like response files
        response_files = []
        for file_path in self.results_dir.iterdir():
            if (file_path.is_file() and 
                file_path.suffix == '.jsonl' and 
                'responses' in file_path.name and
                not file_path.name.startswith('experiment_log')):
                response_files.append(file_path)
        
        if not response_files:
            logger.warning(f"No response files found in {self.results_dir}")
            return []
        
        logger.info(f"Found {len(response_files)} response files to process")
        
        results = []
        for file_path in response_files:
            try:
                result = self.fix_response_file(file_path, dry_run)
                results.append(result)
                self.stats['files_processed'] += 1
            except Exception as e:
                logger.error(f"Error processing {file_path}: {e}")
                results.append({
                    'file': file_path.name,
                    'error': str(e)
                })
        
        return results
    
    def generate_report(self, results: List[Dict]) -> str:
        """Generate a detailed report of the fixing process."""
        report_lines = [
            "LLM Response Fixing Report",
            "=" * 50,
            f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Results Directory: {self.results_dir}",
            f"Minimum Response Length: {self.min_response_length}",
            "",
            "Summary Statistics:",
            f"  Files Processed: {self.stats['files_processed']}",
            f"  Total Responses: {self.stats['total_responses']}",
            f"  Empty Responses: {self.stats['empty_responses']}",
            f"  Short Responses: {self.stats['short_responses']}",
            f"  Null Responses: {self.stats['null_responses']}",
            f"  Total Abnormal: {self.stats['empty_responses'] + self.stats['short_responses'] + self.stats['null_responses']}",
            f"  Successfully Regenerated: {self.stats['regenerated_responses']}",
            f"  Failed Regenerations: {self.stats['failed_regenerations']}",
            "",
            f"Files with Issues: {len(self.stats['files_with_issues'])}",
            f"Models Used: {', '.join(sorted(self.stats['models_used']))}",
            "",
            "Detailed Results by File:",
        ]
        
        for result in results:
            if 'error' in result:
                report_lines.append(f"  ❌ {result['file']}: ERROR - {result['error']}")
            else:
                status = "DRY RUN" if result.get('dry_run') else "FIXED"
                report_lines.append(
                    f"  {'🔍' if result.get('dry_run') else '✅'} {result['file']} ({status}): "
                    f"{result['abnormal_responses']}/{result['total_responses']} abnormal, "
                    f"{result['regenerated']} regenerated, {result['failed']} failed"
                )
                
        return "\n".join(report_lines)


def main():
    parser = argparse.ArgumentParser(description='Fix empty or abnormal LLM responses')
    parser.add_argument('results_dir', type=str, 
                       help='Path to timestamped results directory (e.g., results/20250730_233805)')
    parser.add_argument('--min-length', type=int, default=5,
                       help='Minimum response length to consider valid (default: 5)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Only scan and report, do not fix responses')
    parser.add_argument('--next-base-url', type=str, default=NEXT_BASE_URL,
                       help='Base URL for Next API client')
    parser.add_argument('--max-requests-per-minute', type=int, default=20,
                       help='Maximum requests per minute (default: 20)')
    parser.add_argument('--report-file', type=str, 
                       help='Save report to specified file (default: print to stdout)')
    
    args = parser.parse_args()
    
    # Initialize the fixer
    fixer = ResponseFixer(
        results_dir=args.results_dir,
        min_response_length=args.min_length,
        next_base_url=args.next_base_url,
        max_requests_per_minute=args.max_requests_per_minute
    )
    
    try:
        # Process the directory
        logger.info(f"Starting {'scan' if args.dry_run else 'fix'} process...")
        results = fixer.process_directory(dry_run=args.dry_run)
        
        # Generate report
        report = fixer.generate_report(results)
        
        # Output report
        if args.report_file:
            with open(args.report_file, 'w') as f:
                f.write(report)
            logger.info(f"Report saved to {args.report_file}")
        else:
            print("\n" + report)
            
        logger.info("Process completed successfully!")
        
    except Exception as e:
        logger.error(f"Process failed: {e}")
        return 1
        
    return 0


if __name__ == "__main__":
    exit(main())