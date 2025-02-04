import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
import json
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def load_results(results_dir: Path, timestamp: str) -> pd.DataFrame:
    """Load results from a specific experiment run."""
    results = []
    exp_dir = results_dir / timestamp
    
    # Get all result files in the timestamp directory
    result_files = list(exp_dir.glob("*_results.jsonl"))
    
    for file in result_files:
        with open(file, 'r') as f:
            for line in f:
                data = json.loads(line)
                result = {
                    'model': data['model'],
                    'policy': data['policy'],
                    'dataset': data['dataset'],
                    'conflict_recognized': data['evaluation']['conflict_recognized'],
                    'primary_met': data['evaluation']['primary_constraint_met'],
                    'secondary_met': data['evaluation']['secondary_constraint_met'],
                    'success': data['evaluation']['joint_satisfaction']
                }
                results.append(result)
    
    return pd.DataFrame(results)

def plot_success_rates(df: pd.DataFrame, output_dir: Path):
    """Create success rate comparison plot."""
    plt.figure(figsize=(15, 8))
    
    # Calculate success rates
    success_rates = df.groupby(['model', 'policy'])['success'].mean().unstack()
    
    # Create heatmap
    sns.heatmap(success_rates, annot=True, fmt='.2%', cmap='RdYlGn')
    plt.title('Success Rates by Model and Policy')
    plt.xlabel('Policy')
    plt.ylabel('Model')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(output_dir / 'model_comparison_success_rate.png', dpi=300, bbox_inches='tight')
    plt.close()

def plot_recognition_rates(df: pd.DataFrame, output_dir: Path):
    """Create recognition rates plot."""
    plt.figure(figsize=(15, 8))
    
    # Calculate recognition rates
    recognition_rates = df.groupby(['model', 'policy'])['conflict_recognized'].mean()
    
    # Create bar plot
    ax = recognition_rates.unstack().plot(kind='bar', width=0.8)
    plt.title('Conflict Recognition Rates by Model and Policy')
    plt.xlabel('Model')
    plt.ylabel('Recognition Rate')
    plt.legend(title='Policy', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_dir / 'recognition_rates.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_organized_results(df: pd.DataFrame, output_dir: Path):
    """Create organized results CSV."""
    # Group policies
    policy_groups = {
        'Baseline Policies': ['baseline_all_user', 'basic_separation', 'task_specified_separation', 'emphasized_separation'],
        'System Prompt Policies': ['unmarked_system_basic', 'marked_system_basic', 'unmarked_system_detailed', 'marked_system_detailed'],
        'User Prompt Policies': ['unmarked_user_basic', 'marked_user_basic', 'unmarked_user_detailed', 'marked_user_detailed']
    }
    
    # Calculate metrics for each policy and model
    results = df.groupby(['model', 'policy']).agg({
        'conflict_recognized': 'mean',
        'primary_met': 'mean',
        'secondary_met': 'mean',
        'success': 'mean'
    }).round(4)
    
    # Add policy group column
    results['policy_group'] = results.index.get_level_values('policy').map(
        {policy: group for group, policies in policy_groups.items() for policy in policies}
    )
    
    # Sort by policy group and save
    results = results.sort_values(['policy_group', 'policy'])
    results.to_csv(output_dir / 'organized_results.csv')

def main():
    results_dir = Path('results')
    timestamp = input("Enter the timestamp for analysis: ")
    
    analysis_dir = results_dir / 'nextclient_analysis'
    analysis_dir.mkdir(exist_ok=True)
    
    # Load results
    df = load_results(results_dir, timestamp)
    
    # Generate visualizations and reports
    plot_success_rates(df, analysis_dir)
    plot_recognition_rates(df, analysis_dir)
    create_organized_results(df, analysis_dir)

if __name__ == "__main__":
    main()
