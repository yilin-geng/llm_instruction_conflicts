import json
import logging
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import argparse

root_dir = Path(__file__).parent.parent
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@dataclass
class AnalysisResult:
    model_name: str
    policy_name: str
    conflict_name: str
    scenario_conflict_recognized: float  # Scenario 1
    scenario_primary_only: float        # Scenario 2 
    scenario_secondary_only: float      # Scenario 3
    scenario_none_met: float           # Scenario 4
    scenario_both_met: float           # Scenario 5: sanity check - should never happen

def load_results(results_dir: Path, timestamp: str = None) -> Dict[str, List[dict]]:
    """Load results from specified timestamp directory or all available results."""
    results = {}
    
    if timestamp:
        # Load specific timestamp results
        timestamp_dir = results_dir / timestamp
        if not timestamp_dir.exists():
            raise ValueError(f"No results found for timestamp {timestamp}")
        
        for file_path in timestamp_dir.glob('*_results.jsonl'):
            model_name = file_path.stem.replace('_results', '')
            results[f"{model_name}_{timestamp}"] = []
            
            with open(file_path, 'r') as f:
                for line in f:
                    results[f"{model_name}_{timestamp}"].append(json.loads(line))
    else:
        # Load all timestamp directories
        for timestamp_dir in sorted(results_dir.glob('*')):
            if not timestamp_dir.is_dir():
                continue
                
            timestamp = timestamp_dir.name
            for file_path in timestamp_dir.glob('*_results.jsonl'):
                model_name = file_path.stem.replace('_results', '')
                results[f"{model_name}_{timestamp}"] = []
                
                with open(file_path, 'r') as f:
                    for line in f:
                        results[f"{model_name}_{timestamp}"].append(json.loads(line))
                
    return results

def analyze_by_conflict_type(results: Dict[str, List[dict]]) -> pd.DataFrame:
    """Analyze results grouped by conflict type with non-overlapping scenarios."""
    analysis_data = []
    
    for model_name, model_results in results.items():
        for result in model_results:
            # Calculate non-overlapping scenarios
            conflict_recognized = result['conflict_recognized']
            primary_met = result['primary_constraint_met']
            secondary_met = result['secondary_constraint_met']
            
            # Scenario 1: Conflict recognized
            scenario_conflict_recognized = float(conflict_recognized)
            
            # Only calculate other scenarios if conflict not recognized
            if not conflict_recognized:
                # Scenario 2: Only primary met
                scenario_primary_only = float(primary_met and not secondary_met)
                
                # Scenario 3: Only secondary met
                scenario_secondary_only = float(not primary_met and secondary_met)
                
                # Scenario 4: Neither constraint met
                scenario_none_met = float(not primary_met and not secondary_met)
                
                # Scenario 5: Both constraints met
                scenario_both_met = float(primary_met and secondary_met)
            else:
                # If conflict recognized, other scenarios are 0
                scenario_primary_only = 0.0
                scenario_secondary_only = 0.0
                scenario_none_met = 0.0
                scenario_both_met = 0.0
            
            analysis_data.append({
                'model_name': model_name,
                'policy_name': result['policy_name'],
                'conflict_name': result['conflict_name'],
                'scenario_conflict_recognized': scenario_conflict_recognized,
                'scenario_primary_only': scenario_primary_only,
                'scenario_secondary_only': scenario_secondary_only,
                'scenario_none_met': scenario_none_met,
                'scenario_both_met': scenario_both_met,
                'base_instruction': result['base_instruction'],
                'constraint1': result['constraint1'],
                'constraint2': result['constraint2'],
                'response': result['response'],
                'system_prompt': result['system_prompt'],
                'user_prompt': result['user_prompt']
            })
    
    return pd.DataFrame(analysis_data)

def plot_conflict_analysis(df: pd.DataFrame, output_dir: Path, timestamp: str = None):
    """Generate visualization plots for the analysis with timestamp handling."""
    # Validate that scenario_both_met is always 0
    if not (df['scenario_both_met'] == 0).all():
        # print the df['scenario_both_met'] != 0 cases, show detailed information
        for index, row in df[df['scenario_both_met'] != 0].iterrows():
            print(row)
        raise ValueError("Invalid data: Found non-zero values in scenario_both_met")
        
    plots_dir = output_dir / 'plots'
    if timestamp:
        plots_dir = plots_dir / timestamp
    plots_dir.mkdir(exist_ok=True, parents=True)
    
    scenario_cols = [
        'scenario_conflict_recognized',
        'scenario_primary_only',
        'scenario_secondary_only',
        'scenario_none_met',
    ]
    
    # Mapping for prettier scenario names
    scenario_names = {
        'scenario_conflict_recognized': 'Conflict\nRecognized',
        'scenario_primary_only': 'Primary\nOnly',
        'scenario_secondary_only': 'Secondary\nOnly',
        'scenario_none_met': 'None\nMet',
    }
    
    # Calculate number of rows and columns for subplots
    n_models = len(df['model_name'].unique())
    n_policies = len(df['policy_name'].unique())
    n_cols = n_policies
    n_rows = n_models
    
    # Create figure with subplots
    fig = plt.figure(figsize=(20, 8))
    
    # Create pie charts for each model-policy combination
    for i, model in enumerate(df['model_name'].unique()):
        model_data = df[df['model_name'] == model]
        
        for j, policy in enumerate(model_data['policy_name'].unique()):
            policy_data = model_data[model_data['policy_name'] == policy]
            
            # Calculate scenario percentages
            values = [policy_data[col].mean() * 100 for col in scenario_cols]
            labels = [scenario_names[col] for col in scenario_cols]
            
            # Create subplot
            ax = plt.subplot(n_rows, n_cols, i * n_cols + j + 1)
            
            # Create pie chart
            wedges, texts, autotexts = ax.pie(
                values,
                labels=labels,
                autopct='%1.1f%%',
                pctdistance=0.85,
                labeldistance=1.1
            )
            
            # Customize appearance
            plt.setp(autotexts, size=8, weight="bold")
            plt.setp(texts, size=8)
            
            # Add title
            if i == 0:
                ax.set_title(f'{policy}', pad=20, fontsize=10)
            if j == 0:
                ax.text(-1.5, 0, model, rotation=90, fontsize=10, ha='center', va='center')
    
    # Adjust layout
    plt.tight_layout(h_pad=4, w_pad=2)
    
    # Save figure
    plt.savefig(
        plots_dir / f'scenario_distribution_pies_{timestamp or "all"}.png',
        bbox_inches='tight',
        dpi=300
    )
    plt.close()

def generate_summary_report(df: pd.DataFrame, output_dir: Path, timestamp: str = None):
    """Generate a detailed summary report with timestamp handling."""
    reports_dir = output_dir / 'reports'
    if timestamp:
        reports_dir = reports_dir / timestamp
    reports_dir.mkdir(exist_ok=True, parents=True)
    
    report_path = reports_dir / f'analysis_report_{timestamp or "all"}.md'
    
    with open(report_path, 'w') as f:
        f.write('# Conflict Resolution Analysis Report\n\n')
        
        # Overall statistics
        f.write('## Overall Statistics\n\n')
        for model in df['model_name'].unique():
            model_data = df[df['model_name'] == model]
            f.write(f'### {model}\n')
            f.write('#### Scenario Distribution:\n')
            f.write(f'- Conflict Recognition Rate: {model_data["scenario_conflict_recognized"].mean():.2%}\n')
            f.write(f'- Primary Constraint Only: {model_data["scenario_primary_only"].mean():.2%}\n')
            f.write(f'- Secondary Constraint Only: {model_data["scenario_secondary_only"].mean():.2%}\n')
            f.write(f'- No Constraints Met: {model_data["scenario_none_met"].mean():.2%}\n\n')
        
        # Policy-specific analysis with examples
        f.write('## Policy Analysis\n\n')
        for policy in df['policy_name'].unique():
            policy_data = df[df['policy_name'] == policy]
            f.write(f'### {policy}\n')
            for model in df['model_name'].unique():
                model_policy_data = policy_data[policy_data['model_name'] == model]
                f.write(f'#### {model}\n')
                f.write('##### Scenario Distribution:\n')
                f.write(f'- Conflict Recognition Rate: {model_policy_data["scenario_conflict_recognized"].mean():.2%}\n')
                f.write(f'- Primary Constraint Only: {model_policy_data["scenario_primary_only"].mean():.2%}\n')
                f.write(f'- Secondary Constraint Only: {model_policy_data["scenario_secondary_only"].mean():.2%}\n')
                f.write(f'- No Constraints Met: {model_policy_data["scenario_none_met"].mean():.2%}\n')


                # Add examples for each non-zero scenario
                scenarios = {
                    'Conflict Recognition': 'scenario_conflict_recognized',
                    'Primary Only': 'scenario_primary_only',
                    'Secondary Only': 'scenario_secondary_only',
                    'None Met': 'scenario_none_met',
                }

                for scenario_name, scenario_col in scenarios.items():
                    scenario_rate = model_policy_data[scenario_col].mean()
                    if scenario_rate > 0:
                        f.write(f'##### {scenario_name} Examples:\n')
                        # Get examples where this scenario occurred
                        examples = model_policy_data[model_policy_data[scenario_col] == 1]
                        
                        # For 'Both Met', show all instances
                        num_examples = len(examples) if scenario_col == 'scenario_both_met' else min(2, len(examples))
                        
                        for _, example in examples.head(num_examples).iterrows():
                            f.write('```\n')
                            f.write(f'Base Instruction: {example["base_instruction"]}\n')
                            f.write(f'Constraint 1: {example["constraint1"]}\n')
                            f.write(f'Constraint 2: {example["constraint2"]}\n')
                            f.write(f'System Prompt: {example["system_prompt"]}\n')
                            f.write(f'User Prompt: {example["user_prompt"]}\n')
                            f.write(f'Response: {example["response"]}\n')
                            f.write('```\n\n')
                
                f.write('---\n\n')

def compute_failure_rates(df: pd.DataFrame) -> pd.DataFrame:
    """Compute failure rates (scenario_secondary_only + scenario_none_met) for each policy and model."""
    failure_rates = df.groupby(['model_name', 'policy_name']).agg({
        'scenario_secondary_only': 'mean',
        'scenario_none_met': 'mean'
    })
    
    failure_rates['total_failure_rate'] = failure_rates['scenario_secondary_only'] + failure_rates['scenario_none_met']
    return failure_rates

def compute_success_rates(df: pd.DataFrame) -> pd.DataFrame:
    """Compute success rates (scenario_conflict_recognized + scenario_primary_only) for each policy and model."""
    success_rates = df.groupby(['model_name', 'policy_name']).agg({
        'scenario_conflict_recognized': 'mean',
        'scenario_primary_only': 'mean'
    })
    
    success_rates['total_success_rate'] = success_rates['scenario_conflict_recognized'] + success_rates['scenario_primary_only']
    return success_rates

def compute_conflict_type_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Compute statistics for each conflict type, policy, and model combination."""
    stats = df.groupby(['model_name', 'policy_name', 'conflict_name']).agg({
        'scenario_conflict_recognized': 'mean',
        'scenario_primary_only': 'mean',
        'scenario_secondary_only': 'mean',
        'scenario_none_met': 'mean',
    }).round(4)
    
    stats['failure_rate'] = stats['scenario_secondary_only'] + stats['scenario_none_met']
    return stats



def generate_detailed_report(df: pd.DataFrame, output_dir: Path, timestamp: str = None):
    """Generate a detailed report including failure rates and success rates."""
    reports_dir = output_dir / 'reports'
    if timestamp:
        reports_dir = reports_dir / timestamp
    reports_dir.mkdir(exist_ok=True, parents=True)
    
    report_path = reports_dir / f'detailed_analysis_{timestamp or "all"}.md'
    
    # Calculate statistics
    failure_rates = compute_failure_rates(df)
    success_rates = compute_success_rates(df)
    conflict_stats = compute_conflict_type_stats(df)
    
    with open(report_path, 'w') as f:
        f.write('# Detailed Conflict Resolution Analysis\n\n')
        
        # Overall Rates Table
        f.write('## Overall Performance Rates\n\n')
        f.write('| Model | Policy | Success Rate | Failure Rate |\n')
        f.write('|-------|---------|--------------|-------------|\n')
        
        for idx in failure_rates.index:
            model, policy = idx
            success = success_rates.loc[idx, 'total_success_rate']
            failure = failure_rates.loc[idx, 'total_failure_rate']
            f.write(f"| {model} | {policy} | {success:.2%} | {failure:.2%} |\n")
        
        # Detailed Rates Table
        f.write('\n## Detailed Rates\n\n')
        f.write('| Model | Policy | Recognized | Primary Only | Secondary Only | None Met | Success Rate | Failure Rate |\n')
        f.write('|-------|---------|------------|--------------|----------------|----------|--------------|-------------|\n')
        
        for idx in failure_rates.index:
            model, policy = idx
            model_policy_data = df[(df['model_name'] == model) & (df['policy_name'] == policy)]
            recognized = model_policy_data['scenario_conflict_recognized'].mean()
            primary = model_policy_data['scenario_primary_only'].mean()
            secondary = model_policy_data['scenario_secondary_only'].mean()
            none = model_policy_data['scenario_none_met'].mean()
            success = success_rates.loc[idx, 'total_success_rate']
            failure = failure_rates.loc[idx, 'total_failure_rate']
            
            f.write(f"| {model} | {policy} | {recognized:.2%} | {primary:.2%} | "
                   f"{secondary:.2%} | {none:.2%} | {success:.2%} | {failure:.2%} |\n")
        
        # Conflict Type Statistics
        f.write('\n## Statistics by Conflict Type\n\n')
        
        for (model, policy), group in conflict_stats.groupby(['model_name', 'policy_name']):
            f.write(f"\n### {model} - {policy}\n\n")
            f.write('| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |\n')
            f.write('|---------------|------------|---------|-----------|------|-------------|\n')
            
            for idx, row in group.iterrows():
                conflict = idx[2]  # Get conflict name from multi-index
                f.write(f"| {conflict} | {row['scenario_conflict_recognized']:.2%} | "
                       f"{row['scenario_primary_only']:.2%} | {row['scenario_secondary_only']:.2%} | "
                       f"{row['scenario_none_met']:.2%} | "
                       f"{row['failure_rate']:.2%} |\n")

def main():
    results_dir = root_dir / 'results'
    
    # Optional: Add argument parsing for timestamp
    parser = argparse.ArgumentParser()
    parser.add_argument('--timestamp', help='Specific timestamp to analyze')
    args = parser.parse_args()
    
    # Load results
    results = load_results(results_dir, args.timestamp)
    
    # Perform analysis
    df = analyze_by_conflict_type(results)
    
    # Generate visualizations and reports
    plot_conflict_analysis(df, results_dir, args.timestamp)
    generate_summary_report(df, results_dir, args.timestamp)
    generate_detailed_report(df, results_dir, args.timestamp)
    
    logger.info(f"Analysis complete. Results saved to {results_dir}")

if __name__ == "__main__":
    main()
