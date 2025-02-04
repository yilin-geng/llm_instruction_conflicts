import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Dict, List
import json

def get_ordered_policies():
    """Return policies in meaningful groups for visualization."""
    return {
        'Baseline': [
            'baseline_all_user'
        ],
        'Separation Policies': [
            'basic_separation',
            'task_specified_separation',
            'emphasized_separation'
        ],
        'Unmarked Policies': [
            'unmarked_system_basic',
            'unmarked_system_detailed',
            'unmarked_user_basic',
            'unmarked_user_detailed'
        ],
        'Marked Policies': [
            'marked_system_basic',
            'marked_system_detailed',
            'marked_user_basic',
            'marked_user_detailed'
        ]
    }

def get_policy_order():
    """Get flat list of policies in correct order."""
    policy_groups = get_ordered_policies()
    return [policy for group in policy_groups.values() for policy in group]

def load_all_results(results_dir: Path, timestamps: Dict[str, Dict[str, str]]) -> pd.DataFrame:
    """Load and process results from all experiments."""
    all_data = []
    
    for model, dataset_configs in timestamps.items():
        for dataset_type, timestamp in dataset_configs.items():
            timestamp_dir = results_dir / timestamp
            results_file = timestamp_dir / f"{model}_results.jsonl"
            
            with open(results_file, 'r') as f:
                for line in f:
                    result = json.loads(line)
                    # Calculate scenarios like in analyze.py
                    conflict_recognized = result['conflict_recognized']
                    primary_met = result['primary_constraint_met']
                    secondary_met = result['secondary_constraint_met']
                    
                    processed_result = {
                        'model': model,
                        'dataset_type': dataset_type,
                        'policy_name': result['policy_name'],
                        'conflict_name': result['conflict_name'],
                        'scenario_conflict_recognized': float(conflict_recognized),
                        'scenario_primary_only': float(not conflict_recognized and primary_met and not secondary_met),
                        'scenario_secondary_only': float(not conflict_recognized and not primary_met and secondary_met),
                        'scenario_none_met': float(not conflict_recognized and not primary_met and not secondary_met)
                    }
                    all_data.append(processed_result)
    
    return pd.DataFrame(all_data)

def get_ordered_policies():
    """Return policies in meaningful groups for visualization."""
    return {
        'Baseline': [
            'baseline_all_user'
        ],
        'Separation Policies': [
            'basic_separation',
            'task_specified_separation',
            'emphasized_separation'
        ],
        'Unmarked Policies': [
            'unmarked_system_basic',
            'unmarked_system_detailed',
            'unmarked_user_basic',
            'unmarked_user_detailed'
        ],
        'Marked Policies': [
            'marked_system_basic',
            'marked_system_detailed',
            'marked_user_basic',
            'marked_user_detailed'
        ]
    }

def get_policy_order():
    """Get flat list of policies in correct order."""
    policy_groups = get_ordered_policies()
    return [policy for group in policy_groups.values() for policy in group]

def plot_success_rates_heatmap(df: pd.DataFrame, output_dir: Path):
    """Plot heatmap of success rates across models, datasets, and policies."""
    success_rates = df.groupby(['model', 'dataset_type', 'policy_name'], observed=True).agg({
        'scenario_conflict_recognized': 'mean',
        'scenario_primary_only': 'mean'
    }).reset_index()
    
    success_rates['success_rate'] = (
        success_rates['scenario_conflict_recognized'] + 
        success_rates['scenario_primary_only']
    ) * 100
    
    # Create more readable dataset type labels
    success_rates['dataset_type'] = success_rates['dataset_type'].map({
        'basic': 'Basic Instructions',
        'reversed': 'Reversed Instructions',
        'rich_context': 'Rich Context',
        'rich_context_reversed': 'Rich Context Reversed'
    })
    
    # Get policy order
    policy_order = get_policy_order()
    
    # Pivot for heatmap
    heatmap_data = success_rates.pivot_table(
        values='success_rate',
        index=['model', 'dataset_type'],
        columns='policy_name'
    )[policy_order]  # Reorder columns
    
    # Create figure
    plt.figure(figsize=(20, 10))
    
    # Plot heatmap
    ax = sns.heatmap(heatmap_data, annot=True, fmt='.1f', cmap='RdYlGn', center=50)
    
    # Add vertical lines to separate policy groups
    policy_groups = get_ordered_policies()
    cumsum = 0
    for group_name, policies in policy_groups.items():
        cumsum += len(policies)
        if cumsum < len(policy_order):  # Don't draw line after last group
            ax.axvline(x=cumsum, color='black', linewidth=2)
    
    plt.title('Success Rates (%) Across Models, Datasets, and Policies')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(output_dir / 'success_rates_heatmap.png', bbox_inches='tight')
    plt.close()

def plot_model_comparison(df: pd.DataFrame, output_dir: Path):
    """Plot model comparison across different metrics and datasets."""
    metrics = {
        'Success Rate': ['scenario_conflict_recognized', 'scenario_primary_only'],
        'Failure Rate': ['scenario_secondary_only', 'scenario_none_met']
    }
    
    policy_order = get_policy_order()
    policy_groups = get_ordered_policies()
    
    # Convert policy_name to categorical with ordered categories upfront
    df = df.copy()
    df['policy_name'] = pd.Categorical(df['policy_name'], categories=policy_order, ordered=True)
    
    for metric_name, columns in metrics.items():
        fig, axes = plt.subplots(2, 2, figsize=(20, 15))
        fig.suptitle(f'{metric_name} by Model and Dataset Type', fontsize=16)
        
        dataset_labels = {
            'basic': 'Basic Instructions',
            'reversed': 'Reversed Instructions',
            'rich_context': 'Rich Context',
            'rich_context_reversed': 'Rich Context Reversed'
        }
        
        for idx, dataset in enumerate(['basic', 'reversed', 'rich_context', 'rich_context_reversed']):
            row = idx // 2
            col = idx % 2
            
            dataset_data = df[df['dataset_type'] == dataset].copy()
            metric_sum = dataset_data[columns].sum(axis=1) * 100
            
            # Pre-aggregate the data
            model_metrics = (dataset_data.groupby(['model', 'policy_name'], observed=True)
                           .apply(lambda x: x[columns].sum(axis=1).mean())
                           .reset_index(name='metric_value'))
            
            # Create subplot
            ax = axes[row, col]
            sns.barplot(
                data=model_metrics,
                x='policy_name',
                y='metric_value',
                hue='model',
                ax=ax,
                order=policy_order
            )
            
            # Add vertical lines to separate policy groups
            cumsum = 0
            ylim = ax.get_ylim()
            for group_name, policies in policy_groups.items():
                cumsum += len(policies)
                if cumsum < len(policy_order):  # Don't draw line after last group
                    ax.axvline(x=cumsum - 0.5, color='black', linestyle='--', alpha=0.5)
            ax.set_ylim(ylim)  # Reset y-limits after drawing lines
            
            # Customize subplot
            ax.set_title(f'Dataset: {dataset_labels[dataset]}')
            ax.set_xticklabels(
                ax.get_xticklabels(),
                rotation=45,
                ha='right'
            )
            ax.set_ylabel(f'{metric_name} (%)')
            
            # Add legend only to first subplot
            if idx > 0:
                ax.get_legend().remove()
        
        # Adjust layout
        plt.tight_layout()
        plt.savefig(output_dir / f'model_comparison_{metric_name.lower().replace(" ", "_")}.png', 
                   bbox_inches='tight', 
                   dpi=300)
        plt.close()

def generate_summary_stats(df: pd.DataFrame, output_dir: Path):
    """Generate comprehensive summary statistics."""
    with open(output_dir / 'summary_statistics.md', 'w') as f:
        f.write('# Combined Analysis Summary\n\n')
        
        # Overall model performance by dataset
        f.write('## Model Performance by Dataset Type\n\n')
        model_dataset_stats = df.groupby(
            ['model', 'dataset_type'], 
            observed=True
        ).agg({
            'scenario_conflict_recognized': 'mean',
            'scenario_primary_only': 'mean',
            'scenario_secondary_only': 'mean',
            'scenario_none_met': 'mean'
        }) * 100
        
        f.write(model_dataset_stats.round(2).to_markdown())
        f.write('\n\n')
        
        # Best performing policies
        f.write('## Top Performing Policies by Model and Dataset\n\n')
        for model in df['model'].unique():
            f.write(f'### {model}\n\n')
            for dataset in df['dataset_type'].unique():
                data = df[(df['model'] == model) & (df['dataset_type'] == dataset)]
                success_rates = data.groupby('policy_name').agg({
                    'scenario_conflict_recognized': 'mean',
                    'scenario_primary_only': 'mean'
                }).sum(axis=1).sort_values(ascending=False) * 100
                
                f.write(f'#### {dataset}\n')
                f.write(success_rates.head(3).round(2).to_markdown())
                f.write('\n\n')

def plot_recognition_rates(df: pd.DataFrame, output_dir: Path):
    """Plot conflict recognition rates across models and policies."""
    policy_order = get_policy_order()
    policy_groups = get_ordered_policies()
    
    fig, axes = plt.subplots(2, 2, figsize=(20, 15))
    fig.suptitle('Conflict Recognition Analysis by Dataset Type', fontsize=16)
    
    dataset_labels = {
        'basic': 'Basic Instructions',
        'reversed': 'Reversed Instructions',
        'rich_context': 'Rich Context',
        'rich_context_reversed': 'Rich Context Reversed'
    }
    
    for idx, dataset in enumerate(['basic', 'reversed', 'rich_context', 'rich_context_reversed']):
        row = idx // 2
        col = idx % 2
        
        dataset_data = df[df['dataset_type'] == dataset]
        
        ax = axes[row, col]
        sns.barplot(
            data=dataset_data,
            x='policy_name',
            y='scenario_conflict_recognized',
            hue='model',
            ax=ax,
            order=policy_order
        )
        
        ax.set_title(f'Dataset: {dataset_labels[dataset]}')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        ax.set_ylabel('Recognition Rate (%)')
        
        if idx > 0:
            ax.get_legend().remove()
    
    plt.tight_layout()
    plt.savefig(output_dir / 'recognition_rates.png', bbox_inches='tight', dpi=300)
    plt.close()

def plot_conflict_type_performance(df: pd.DataFrame, output_dir: Path):
    """Plot performance across different conflict types."""
    policy_order = get_policy_order()
    
    scenario_data = pd.melt(
        df,
        id_vars=['model', 'policy_name', 'dataset_type'],
        value_vars=[
            'scenario_conflict_recognized',
            'scenario_primary_only',
            'scenario_secondary_only',
            'scenario_none_met'
        ],
        var_name='scenario_type',
        value_name='rate'
    )
    
    scenario_data['scenario_type'] = scenario_data['scenario_type'].map({
        'scenario_conflict_recognized': 'Conflict Recognized',
        'scenario_primary_only': 'Primary Only',
        'scenario_secondary_only': 'Secondary Only',
        'scenario_none_met': 'None Met'
    })
    
    for model in df['model'].unique():
        model_data = scenario_data[scenario_data['model'] == model]
        
        plt.figure(figsize=(20, 10))
        sns.barplot(
            data=model_data,
            x='policy_name',
            y='rate',
            hue='scenario_type',
            order=policy_order
        )
        
        plt.title(f'Scenario Type Distribution - {model}')
        plt.xticks(rotation=45, ha='right')
        plt.ylabel('Percentage (%)')
        plt.legend(title='Scenario Type', bbox_to_anchor=(1.05, 1), loc='upper left')
        
        plt.tight_layout()
        plt.savefig(output_dir / f'conflict_types_{model}.png', bbox_inches='tight', dpi=300)
        plt.close()

def generate_latex_table(df: pd.DataFrame, output_dir: Path):
    """Generate LaTeX table with structured comparison of models and policies."""
    policy_groups = {
        'Baseline': ['baseline_all_user', 'basic_separation', 'task_specified_separation', 'emphasized_separation'],
        'System Prompts': ['unmarked_system_basic', 'marked_system_basic', 'unmarked_system_detailed', 'marked_system_detailed'],
        'User Prompts': ['unmarked_user_basic', 'marked_user_basic', 'unmarked_user_detailed', 'marked_user_detailed']
    }
    
    datasets = ['basic', 'reversed', 'rich_context', 'rich_context_reversed']
    dataset_labels = {
        'basic': 'Basic Instructions',
        'reversed': 'Reversed Instructions',
        'rich_context': 'Rich Context',
        'rich_context_reversed': 'Rich Context Reversed'
    }
    
    latex_content = [
        "\\begin{table*}[t]",
        "\\centering",
        "\\caption{Performance Comparison Across Models, Datasets, and Policy Types}",
        "\\label{tab:full_results}",
        "\\begin{tabular}{l" + "c" * 12 + "}",  # 1 for row labels + 12 for policies
        "\\toprule",
        "& \\multicolumn{4}{c}{Baseline Policies} & \\multicolumn{4}{c}{System Prompt Policies} & \\multicolumn{4}{c}{User Prompt Policies} \\\\",
        "\\cmidrule(lr){2-5} \\cmidrule(lr){6-9} \\cmidrule(lr){10-13}"
    ]
    
    # Add policy names
    policy_headers = []
    for group in policy_groups.values():
        policy_headers.extend([p.replace('_', '\\_') for p in group])
    latex_content.append("Dataset & " + " & ".join(policy_headers) + " \\\\")
    latex_content.append("\\midrule")
    
    # Add data rows
    for dataset in datasets:
        dataset_data = df[df['dataset_type'] == dataset]
        
        # Add rows for both models
        for model in ['gpt4', 'llama3']:
            model_data = dataset_data[dataset_data['model'] == model]
            
            # Collect success rates for each policy
            rates = []
            for group in policy_groups.values():
                for policy in group:
                    rate = model_data[model_data['policy_name'] == policy]['scenario_conflict_recognized'].mean() * 100
                    rates.append(f"{rate:.1f}")
            
            # Format row label
            if model == 'gpt4':
                row_label = f"{dataset_labels[dataset]} (GPT-4)"
            else:
                row_label = f"\\quad LLaMA3"
            
            # Add row to table
            latex_content.append(f"{row_label} & " + " & ".join(rates) + " \\\\")
        
        # Add space between dataset blocks
        if dataset != datasets[-1]:
            latex_content.append("\\addlinespace")
    
    # Close table
    latex_content.extend([
        "\\bottomrule",
        "\\end{tabular}",
        "\\end{table*}"
    ])
    
    # Write to file
    with open(output_dir / 'full_results_table.tex', 'w') as f:
        f.write('\n'.join(latex_content))

def create_organized_table(df: pd.DataFrame, output_dir: Path):
    """Create organized table with success rates across datasets and models."""
    # Calculate success rate first
    df = df.copy()
    df['success_rate'] = (df['scenario_conflict_recognized'] + df['scenario_primary_only']) * 100
    
    # Get policy groups from the existing function
    policy_groups = {
        'Baseline Policies': ['baseline_all_user', 'basic_separation', 'task_specified_separation', 'emphasized_separation'],
        'System Prompt Policies': ['unmarked_system_basic', 'marked_system_basic', 'unmarked_system_detailed', 'marked_system_detailed'],
        'User Prompt Policies': ['unmarked_user_basic', 'marked_user_basic', 'unmarked_user_detailed', 'marked_user_detailed']
    }
    
    datasets = ['basic', 'reversed', 'rich_context', 'rich_context_reversed']
    dataset_labels = {
        'basic': 'Basic Instructions',
        'reversed': 'Reversed Instructions',
        'rich_context': 'Rich Context',
        'rich_context_reversed': 'Rich Context Reversed'
    }
    
    # Initialize lists to store rows
    rows = []
    row_labels = []
    
    # Create rows for each dataset block
    for dataset in datasets:
        dataset_data = df[df['dataset_type'] == dataset]
        
        # Add rows for both models
        for model in ['gpt4', 'llama3']:
            model_data = dataset_data[dataset_data['model'] == model]
            row_values = []
            
            # Get success rates for each policy group
            for group in policy_groups.values():
                for policy in group:
                    success_rate = model_data[model_data['policy_name'] == policy]['success_rate'].mean()
                    row_values.append(f"{success_rate:.1f}")
            
            rows.append(row_values)
            label = f"{dataset_labels[dataset]} ({model.upper()})"
            row_labels.append(label)
    
    # Create column labels from all policy groups
    column_labels = []
    for group in policy_groups.values():
        column_labels.extend(group)
    
    # Create DataFrame
    result_df = pd.DataFrame(rows, index=row_labels, columns=column_labels)
    
    # Save to CSV
    result_df.to_csv(output_dir / 'success_rates_table.csv')
    
    return result_df

def plot_conflict_specific_results(df: pd.DataFrame, output_dir: Path):
    """Plot performance analysis for each specific conflict type."""
    # Get unique conflict types from data
    conflict_types = df['conflict_name'].unique()
    policy_order = get_policy_order()
    
    dataset_labels = {
        'basic': 'Basic Instructions',
        'reversed': 'Reversed Instructions',
        'rich_context': 'Rich Context',
        'rich_context_reversed': 'Rich Context Reversed'
    }
    
    # Create figure for each conflict type
    for conflict_type in conflict_types:
        # Filter data for this conflict type
        conflict_data = df[df['conflict_name'] == conflict_type]
        
        # Create figure with subplots for different datasets
        fig, axes = plt.subplots(2, 2, figsize=(20, 16))
        fig.suptitle(f'Success Rate Analysis - {conflict_type}', fontsize=16, y=1.02)
        
        # Calculate success rate (recognized + primary only)
        conflict_data['success_rate'] = (conflict_data['scenario_conflict_recognized'] + 
                                       conflict_data['scenario_primary_only']) * 100
        
        # Plot each dataset
        for idx, dataset in enumerate(['basic', 'reversed', 'rich_context', 'rich_context_reversed']):
            row = idx // 2
            col = idx % 2
            ax = axes[row, col]
            
            # Filter data for this dataset
            dataset_data = conflict_data[conflict_data['dataset_type'] == dataset]
            
            # Calculate mean values for each model-policy combination
            plot_data = []
            for model in df['model'].unique():
                model_data = dataset_data[dataset_data['model'] == model]
                for policy in policy_order:
                    value = model_data[model_data['policy_name'] == policy]['success_rate'].mean()
                    plot_data.append({
                        'Model': model,
                        'Policy': policy,
                        'Rate': value
                    })
            
            plot_df = pd.DataFrame(plot_data)
            
            # Create grouped bar plot
            sns.barplot(
                data=plot_df,
                x='Policy',
                y='Rate',
                hue='Model',
                ax=ax,
                order=policy_order
            )
            
            # Customize subplot
            ax.set_title(f'Dataset: {dataset_labels[dataset]}')
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
            ax.set_ylabel('Success Rate (%)')
            
            # Add value labels on bars
            for container in ax.containers:
                ax.bar_label(container, fmt='%.1f%%', padding=3)
            
            # Only show legend on first subplot
            if idx > 0:
                ax.get_legend().remove()
            
            # Add vertical lines to separate policy groups
            cumsum = 0
            for group in get_ordered_policies().values():
                cumsum += len(group)
                if cumsum < len(policy_order):
                    ax.axvline(x=cumsum - 0.5, color='black', linestyle='--', alpha=0.5)
        
        plt.tight_layout()
        
        # Sanitize conflict type for filename
        safe_conflict_name = conflict_type.replace(':', '_').replace(' ', '_')
        plt.savefig(
            output_dir / f'conflict_analysis_{safe_conflict_name}.png',
            bbox_inches='tight',
            dpi=300
        )
        plt.close()

def main():
    # Define timestamps for each experiment
    timestamps = {
        'gpt4': {
            'basic': '20250201_203055',
            'reversed': '20250201_194735',
            'rich_context': '20250202_004236',
            'rich_context_reversed': '20250201_222556'
        },
        'llama3': {
            'basic': '20250201_151242',
            'reversed': '20250201_235232',
            'rich_context': '20250201_171947',
            'rich_context_reversed': '20250202_042122'
        }
    }
    
    results_dir = Path('results')
    analysis_dir = results_dir / 'combined_analysis'
    analysis_dir.mkdir(exist_ok=True)
    
    # Load and process all results
    df = load_all_results(results_dir, timestamps)
    
    # # Generate visualizations and reports
    # plot_success_rates_heatmap(df, analysis_dir)
    # plot_model_comparison(df, analysis_dir)
    # generate_summary_stats(df, analysis_dir)
    # plot_recognition_rates(df, analysis_dir)
    # plot_conflict_type_performance(df, analysis_dir)
    # # generate_latex_table(df, analysis_dir)
    # create_organized_table(df, analysis_dir)
    plot_conflict_specific_results(df, analysis_dir)

if __name__ == "__main__":
    main()