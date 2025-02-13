# Re-load the uploaded file since execution state was reset
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set up paths
analysis_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(analysis_dir, 'tables', 'polar_plot_simple.csv')
out_dir = os.path.join(analysis_dir, 'plots')

# Mappings
conflict_name_mapping = {
    'case_conflict': 'Case',
    'keyword_forbidden_conflict: awesome_need': 'Keyword Usage',
    'keyword_frequency_conflict: like_5_2': 'Keyword Frequency',
    'language_conflict: en_fr': 'Language',
    'num_sentence_conflict: 10_5': 'Sentence Count',
    'word_length_conflict: 300_50': 'Word Length'
}

model_mapping = {
    'qwen2.5-7b-instruct': 'Qwen',
    'Llama-3.1-8B': 'Llama-8B',
    'Llama-3.1-70B': 'Llama-70B',
    'claude-3-5-sonnet-20241022': 'Claude',
    'gpt-4o-mini-2024-07-18': 'GPT4o-mini',
    'gpt-4o-2024-11-20': 'GPT4o',
}

policy_mapping = {
    'basic_separation': 'Pure',
    'task_specified_separation': 'Task',
    'emphasized_separation': 'Emph.',
    'unmarked_system_basic': 'Sys',
    'marked_system_basic': 'Sys-M',
    'unmarked_user_basic': 'User',
    'marked_user_basic': 'User-M',
    'constraint_following_baseline': 'IF.',
    'baseline_all_user': 'No Pri.'
}

def create_simple_plot(df, n=None):
    """Create polar plot with optional nth root transformation."""
    plot_df = df.copy()
    
    if n is not None:
        numeric_columns = ["Value1", "Value2"]
        plot_df[numeric_columns] = plot_df[numeric_columns] ** (1/n)

    models = plot_df["Model"].unique()
    bar_color = 'blue'
    max_bar_width = np.pi / 3

    fig, axes = plt.subplots(2, 3, figsize=(18, 12), subplot_kw={'projection': 'polar'})
    axes = axes.flatten()

    for i, model in enumerate(models):
        ax = axes[i]
        sub_df = plot_df[plot_df["Model"] == model]
        
        labels = [label.replace(" ", "\n") for label in sub_df["Type"].values]
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
        
        bar_lengths = sub_df["Value1"].values
        bar_widths = np.clip(sub_df["Value2"].values, 0, max_bar_width)

        for angle, length, width in zip(angles, bar_lengths, bar_widths):
            ax.bar(angle, length, width=width, alpha=0.6, color=bar_color,
                  edgecolor='black', linewidth=2, bottom=0)

        # Style the plot
        ax.plot(np.linspace(0, 2*np.pi, 100), np.ones(100), 
                color='lightgray', linewidth=0.05, alpha=0.3)
        ax.set_xticks(angles)
        ax.set_xticklabels(labels, fontsize=16)
        ax.set_yticklabels([])
        ax.set_title(model_mapping.get(model, model), fontsize=20, y=1.05)
        ax.set_ylim(0, 1)
        ax.spines['polar'].set_color('lightgray')
        ax.spines['polar'].set_linewidth(0.05)
        ax.spines['polar'].set_alpha(0.3)

    plt.subplots_adjust(hspace=0.2)
    plt.tight_layout()
    return fig

def create_comparison_plot(df, n=None):
    """Create comparison polar plot showing simple vs rich context."""
    plot_df = df.copy()
    
    if n is not None:
        numeric_columns = ["Value1", "Value2", "Value3", "Value4"]
        plot_df[numeric_columns] = plot_df[numeric_columns] ** (1/n)

    color_values12 = 'blue'  # Simple context
    color_values34 = 'red'   # Rich context
    max_bar_width = np.pi / 3

    fig, axes = plt.subplots(2, 3, figsize=(18, 12), subplot_kw={'projection': 'polar'})
    axes = axes.flatten()

    for i, model in enumerate(plot_df["Model"].unique()):
        ax = axes[i]
        sub_df = plot_df[plot_df["Model"] == model]
        
        labels = [label.replace(" ", "\n") for label in sub_df["Type"].values]
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
        
        bar_lengths1 = sub_df["Value1"].values
        bar_widths1 = np.clip(sub_df["Value2"].values, 0, max_bar_width)
        bar_lengths2 = sub_df["Value3"].values
        bar_widths2 = np.clip(sub_df["Value4"].values, 0, max_bar_width)

        for j, (angle, length1, width1, length2, width2) in enumerate(
            zip(angles, bar_lengths1, bar_widths1, bar_lengths2, bar_widths2)):
            ax.bar(angle - width1/16, length1, width=width1, alpha=0.6, 
                  color=color_values12, edgecolor='black', linewidth=2,
                  label='Simple' if j == 0 else "", bottom=0)
            ax.bar(angle + width2/16, length2, width=width2, alpha=0.6,
                  color=color_values34, edgecolor='black', linewidth=2,
                  label='Rich' if j == 0 else "", bottom=0)

        # Style the plot
        ax.plot(np.linspace(0, 2*np.pi, 100), np.ones(100),
               color='lightgray', linewidth=0.05, alpha=0.3)
        ax.set_xticks(angles)
        ax.set_xticklabels(labels, fontsize=16)
        ax.set_yticklabels([])
        ax.set_title(model_mapping.get(model, model), fontsize=20, y=1.05)
        ax.set_ylim(0, 1)
        ax.spines['polar'].set_color('lightgray')
        ax.spines['polar'].set_linewidth(0.05)
        ax.spines['polar'].set_alpha(0.3)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

    plt.subplots_adjust(hspace=0.2, wspace=0.4)
    plt.tight_layout()
    return fig

def main():

    n = 2
    # Read and process the data
    df = pd.read_csv(file_path, header=None)
    
    # Get number of columns from the first row
    num_columns = len(df.iloc[0])
    
    # Set column names based on number of columns
    if num_columns == 4:
        column_names = ["Model", "Type", "Value1", "Value2"]
    elif num_columns == 6:
        column_names = ["Model", "Type", "Value1", "Value2", "Value3", "Value4"]
    else:
        raise ValueError(f"Expected 4 or 6 columns, got {num_columns}")
    
    # Assign column names and process data
    df.columns = column_names
    df = df[1:].reset_index(drop=True)
    
    # Convert numeric columns to float
    numeric_columns = [col for col in df.columns if col.startswith("Value")]
    df[numeric_columns] = df[numeric_columns].astype(float)
    
    # Create appropriate plot based on number of columns
    if num_columns == 4:
        fig = create_simple_plot(df, n=n)
        plt.savefig(os.path.join(out_dir, f"polar_single_n{n}.pdf"), 
                   format='pdf', bbox_inches='tight')
    else:  # num_columns == 6
        fig = create_comparison_plot(df, n=n)
        plt.savefig(os.path.join(out_dir, f"polar_comparison_n{n}.pdf"), 
                   format='pdf', bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    main()