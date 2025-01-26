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
    primary_satisfaction: float
    secondary_satisfaction: float
    conflict_recognition: float
    joint_satisfaction: float

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
    """Analyze results grouped by conflict type."""
    analysis_data = []
    
    for model_name, model_results in results.items():
        for result in model_results:
            analysis_data.append(AnalysisResult(
                model_name=model_name,
                policy_name=result['policy_name'],
                conflict_name=result['conflict_name'],
                primary_satisfaction=result['primary_constraint_met'],
                secondary_satisfaction=result['secondary_constraint_met'],
                conflict_recognition=result['conflict_recognized'],
                joint_satisfaction=result['joint_satisfaction']
            ))
    
    return pd.DataFrame([vars(r) for r in analysis_data])

def plot_conflict_analysis(df: pd.DataFrame, output_dir: Path):
    """Generate visualization plots for the analysis."""
    # Create output directory for plots
    plots_dir = output_dir / 'plots'
    plots_dir.mkdir(exist_ok=True)
    
    # Plot 1: Conflict Recognition by Model and Policy
    plt.figure(figsize=(12, 6))
    sns.barplot(
        data=df,
        x='policy_name',
        y='conflict_recognition',
        hue='model_name'
    )
    plt.xticks(rotation=45)
    plt.title('Conflict Recognition Rate by Model and Policy')
    plt.tight_layout()
    plt.savefig(plots_dir / 'conflict_recognition.png')
    plt.close()
    
    # Plot 2: Primary vs Secondary Constraint Satisfaction
    plt.figure(figsize=(12, 6))
    df_melted = df.melt(
        id_vars=['model_name', 'policy_name'],
        value_vars=['primary_satisfaction', 'secondary_satisfaction'],
        var_name='constraint_type',
        value_name='satisfaction_rate'
    )
    sns.barplot(
        data=df_melted,
        x='policy_name',
        y='satisfaction_rate',
        hue='constraint_type'
    )
    plt.xticks(rotation=45)
    plt.title('Primary vs Secondary Constraint Satisfaction by Policy')
    plt.tight_layout()
    plt.savefig(plots_dir / 'constraint_satisfaction.png')
    plt.close()

def generate_summary_report(df: pd.DataFrame, output_dir: Path):
    """Generate a detailed summary report."""
    report_path = output_dir / 'analysis_report.md'
    
    with open(report_path, 'w') as f:
        f.write('# Conflict Resolution Analysis Report\n\n')
        
        # Overall statistics
        f.write('## Overall Statistics\n\n')
        for model in df['model_name'].unique():
            model_data = df[df['model_name'] == model]
            f.write(f'### {model}\n')
            f.write(f'- Average Conflict Recognition: {model_data["conflict_recognition"].mean():.2%}\n')
            f.write(f'- Average Primary Constraint Satisfaction: {model_data["primary_satisfaction"].mean():.2%}\n')
            f.write(f'- Average Secondary Constraint Satisfaction: {model_data["secondary_satisfaction"].mean():.2%}\n')
            f.write(f'- Average Joint Satisfaction: {model_data["joint_satisfaction"].mean():.2%}\n\n')
        
        # Policy-specific analysis
        f.write('## Policy Analysis\n\n')
        for policy in df['policy_name'].unique():
            policy_data = df[df['policy_name'] == policy]
            f.write(f'### {policy}\n')
            for model in df['model_name'].unique():
                model_policy_data = policy_data[policy_data['model_name'] == model]
                f.write(f'#### {model}\n')
                f.write(f'- Conflict Recognition: {model_policy_data["conflict_recognition"].mean():.2%}\n')
                f.write(f'- Primary Constraint Satisfaction: {model_policy_data["primary_satisfaction"].mean():.2%}\n')
                f.write(f'- Secondary Constraint Satisfaction: {model_policy_data["secondary_satisfaction"].mean():.2%}\n')
                f.write(f'- Joint Satisfaction: {model_policy_data["joint_satisfaction"].mean():.2%}\n\n')

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
