import json
import logging
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

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
    scenario_both_met: float           # Scenario 5

def load_results(results_dir: Path) -> Dict[str, List[dict]]:
    """Load results from all jsonl files in the results directory."""
    results = {}
    for file_path in results_dir.glob('*_results.jsonl'):
        model_name = file_path.stem.replace('_results', '')
        results[model_name] = []
        
        with open(file_path, 'r') as f:
            for line in f:
                results[model_name].append(json.loads(line))
                
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
                'instruction1': result['instruction1'],
                'instruction2': result['instruction2'],
                'response': result['response']
            })
    
    return pd.DataFrame(analysis_data)

def plot_conflict_analysis(df: pd.DataFrame, output_dir: Path):
    """Generate visualization plots for the analysis."""
    plots_dir = output_dir / 'plots'
    plots_dir.mkdir(exist_ok=True)
    
    scenario_cols = [
        'scenario_conflict_recognized',
        'scenario_primary_only',
        'scenario_secondary_only',
        'scenario_none_met',
        'scenario_both_met'
    ]
    
    # Mapping for prettier scenario names
    scenario_names = {
        'scenario_conflict_recognized': 'Conflict\nRecognized',
        'scenario_primary_only': 'Primary\nOnly',
        'scenario_secondary_only': 'Secondary\nOnly',
        'scenario_none_met': 'None\nMet',
        'scenario_both_met': 'Both\nMet'
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
        plots_dir / 'scenario_distribution_pies.png',
        bbox_inches='tight',
        dpi=300
    )
    plt.close()

def generate_summary_report(df: pd.DataFrame, output_dir: Path):
    """Generate a detailed summary report with instance examples."""
    report_path = output_dir / 'analysis_report.md'
    
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
            f.write(f'- No Constraints Met: {model_data["scenario_none_met"].mean():.2%}\n')
            f.write(f'- Both Constraints Met: {model_data["scenario_both_met"].mean():.2%}\n\n')
        
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
                f.write(f'- Both Constraints Met: {model_policy_data["scenario_both_met"].mean():.2%}\n\n')

                # Add examples for each non-zero scenario
                scenarios = {
                    'Conflict Recognition': 'scenario_conflict_recognized',
                    'Primary Only': 'scenario_primary_only',
                    'Secondary Only': 'scenario_secondary_only',
                    'None Met': 'scenario_none_met',
                    'Both Met': 'scenario_both_met'
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
                            f.write(f'Instruction 1: {example["instruction1"]}\n')
                            f.write(f'Instruction 2: {example["instruction2"]}\n')
                            f.write(f'Response: {example["response"]}\n')
                            f.write('```\n\n')
                
                f.write('---\n\n')

def main():
    results_dir = root_dir / 'results'
    results = load_results(results_dir)
    
    # Perform analysis
    df = analyze_by_conflict_type(results)
    
    # Generate visualizations
    plot_conflict_analysis(df, results_dir)
    
    # Generate summary report
    generate_summary_report(df, results_dir)
    
    logger.info(f"Analysis complete. Results saved to {results_dir}")

if __name__ == "__main__":
    main()
