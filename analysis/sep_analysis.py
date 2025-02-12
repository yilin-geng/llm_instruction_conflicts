import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# df = pd.read_csv('analysis/conflict_level_summary_response.csv')
# tag = 'raw'


df = pd.read_csv('analysis/conflict_level_summary_processed_response.csv')
tag = 'processed'


conflict_name_mapping = {
    'case_conflict': 'Case',
    'keyword_forbidden_conflict: awesome_need': 'Keyword Usage',
    'keyword_frequency_conflict: like_5_2': 'Keyword Frequency',
    'language_conflict: en_fr': 'Language',
    'num_sentence_conflict: 10_5': 'Sentence Count',
    'word_length_conflict: 300_50': 'Word Length'
}


models = [
    "qwen2.5-7b-instruct",
    "gpt-4o-mini-2024-07-18",
    "gpt-4o-2024-11-20",
    "claude-3-5-sonnet-20241022",
    "Llama-3.1-8B",
    "Llama-3.1-70B",
]

output_dir = 'analysis/plots'

def csv_to_latex(df):
    # Round numeric columns to 3 decimal places
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    df[numeric_columns] = df[numeric_columns].round(3)
    
    # Convert to latex with specific float format
    latex_text = df.to_latex(index=False, float_format=lambda x: '{:.3f}'.format(x))
    return latex_text
    
    

def metrics_computation(model, policy, conflict_name, inspect=False):
    """Compute Priority Effectiveness Score (PES) and Instruction Neutrality Score (INS)"""
    
    def get_values(dataset):
                base = df[(df['model'] == model) & 
                         (df['policy'] == policy) & 
                         (df['conflict_name'] == conflict_name) &
                         (df['dataset'] == dataset)]
                return (base['primary_constraint_met'].values[0],
                       base['secondary_constraint_met'].values[0])

    # Get values for each dataset
    p_a_a, p_b_a = get_values('conflicting_instructions')
    p_b_b, p_a_b = get_values('conflicting_instructions_reversed') 
    p_a_a_rich, p_b_a_rich = get_values('conflicting_instructions_rich_context')
    p_b_b_rich, p_a_b_rich = get_values('conflicting_instructions_rich_context_reversed')

    # Calculate metrics
    # PES = 0.25[P(A|A_p) + P(B|B_p)] - 0.25[P(B|A_p) + P(A|B_p)] + 0.5
    simple_pes = 0.25 * (p_a_a + p_b_b) - 0.25 * (p_b_a + p_a_b) + 0.5
    rich_pes = 0.25 * (p_a_a_rich + p_b_b_rich) - 0.25 * (p_b_a_rich + p_a_b_rich) + 0.5

    # Calculate INS for simple context
    # INS = 1 - 0.5 * |[P(A|A_p) + P(A|B_p)] - [P(B|A_p) + P(B|B_p)]|
    simple_ins = 1 - 0.5 * abs((p_a_a + p_a_b) - (p_b_a + p_b_b))
    rich_ins = 1 - 0.5 * abs((p_a_a_rich + p_a_b_rich) - (p_b_a_rich + p_b_b_rich))


    if inspect:
        return {
            'p_a_a': p_a_a,
            'p_b_a': p_b_a,
            'p_b_b': p_b_b,
            'p_a_b': p_a_b,
            'p_a_a_rich': p_a_a_rich,
            'p_b_a_rich': p_b_a_rich,
            'p_b_b_rich': p_b_b_rich,
            'p_a_b_rich': p_a_b_rich,
            'PES simple': simple_pes,
            'INS simple': simple_ins,
            'PES rich': rich_pes,
            'INS rich': rich_ins
        }
    else:
        return {
            'PES simple': simple_pes,
            'INS simple': simple_ins,
            'PES rich': rich_pes,
            'INS rich': rich_ins
        }



def table1():
    """Generate Table 1 comparing model performance across different policies."""

    def generate_latex_table1(df):
        latex_str = []

        latex_str.append(r"\begin{tabular}{lccccccccc}")
        latex_str.append(r"\toprule")
        
        # Main header
        latex_str.append(r"\multirow{2}{*}{\textbf{Model}}& \multicolumn{4}{c}{\textbf{Simple Instructions}} & \multicolumn{4}{c}{\textbf{Rich Instructions}} & \multirow{2}{*}{\textbf{Average}}\\")
        latex_str.append(r"\cmidrule(lr){2-5} \cmidrule(lr){6-9}\\")
        
        # Subheader
        latex_str.append(r"\cmidrule(lr){2-5} \cmidrule(lr){6-9}")
        latex_str.append(r" & \textit{IF.} & Pure & Task & Emph. & \textit{IF.} & Pure & Task. & Emph. &  \\")
        latex_str.append(r"\midrule")
        # Data rows
        for idx, row in df.iterrows():
            row_str = f"{row['model']} & "
            # Simple instructions
            row_str += f"{row['constraint_following_baseline_simple']:.2f} & "
            row_str += f"{row['basic_separation_simple']:.2f} & "
            row_str += f"{row['task_specified_separation_simple']:.2f} & "
            row_str += f"{row['emphasized_separation_simple']:.2f} & "
            # Rich instructions
            row_str += f"{row['constraint_following_baseline_rich']:.2f} & "
            row_str += f"{row['basic_separation_rich']:.2f} & "
            row_str += f"{row['task_specified_separation_rich']:.2f} & "
            row_str += f"{row['emphasized_separation_rich']:.2f} & "
            # Model average
            row_str += f"{row['model_average']:.2f} \\\\"
            latex_str.append(row_str)
        
        # Table end
        latex_str.append(r"\bottomrule")
        latex_str.append(r"\end{tabular}")
        
        return "\n".join(latex_str)


    baseline_policies = [
        "constraint_following_baseline",
    ]

    separation_policies = [
        "basic_separation",
        "task_specified_separation",
        "emphasized_separation"
    ]

    policies = baseline_policies + separation_policies

    # Function to get average between normal and reversed datasets
    def get_averaged_metric(df, model, policy, context_type='simple'):
        if context_type == 'simple':
            datasets = ['conflicting_instructions', 'conflicting_instructions_reversed']
        else:
            datasets = ['conflicting_instructions_rich_context', 'conflicting_instructions_rich_context_reversed']
        
        values = []
        for dataset in datasets:
            try:
                value = df[(df['model'] == model) & 
                          (df['policy'] == policy) & 
                          (df['dataset'] == dataset)]['primary_constraint_met']
                values.append(value)
            except:
                continue
        
        return np.mean(values) if values else np.nan

    # Create the result table
    results = []
    for model in models:
        row = {'model': model}
        for policy in policies:
            # Simple context
            row[f'{policy}_simple'] = get_averaged_metric(df, model, policy, 'simple')
            # Rich context
            row[f'{policy}_rich'] = get_averaged_metric(df, model, policy, 'rich')
        results.append(row)

    # Convert to DataFrame
    result_df = pd.DataFrame(results)

    # the model average is the mean of the six columns for the separation_policies
    result_df['model_average'] = result_df[['basic_separation_simple', 
                                            'basic_separation_rich', 
                                            'task_specified_separation_simple', 
                                            'task_specified_separation_rich', 
                                            'emphasized_separation_simple', 
                                            'emphasized_separation_rich']].mean(axis=1)

    # Round values to 3 decimal places
    numeric_columns = result_df.columns.drop('model')
    result_df[numeric_columns] = result_df[numeric_columns].round(3)

    # Save the results

    filename = f'{tag}_o1_obedience'
    result_df.to_csv(f'{output_dir}/{filename}.csv', index=False)
    latex_table = generate_latex_table1(result_df)
    with open(f'{output_dir}/{filename}_latex', 'w') as f:
        f.write(latex_table)



def inspect():

    # check performance of qwen2.5-7b-instruct on all conflicts
    conflict_names = df[df['model'] == 'qwen2.5-7b-instruct']['conflict_name'].unique()
    model = 'qwen2.5-7b-instruct'
    policy = 'basic_separation'
    for conflict_name in conflict_names:
        metrics = metrics_computation(model, policy, conflict_name, inspect=True)
        print(conflict_name)
        print(metrics)
        print('-'*30)
        

def table2(): # tendency analysis table -> plot
    """Generate Table 2 analyzing baseline_all_user performance by conflict type. (constraint preference)"""


    policy = "baseline_all_user"
    
    # Create the result table
    results = []
    
    # Group by model and conflict_name
    for model in models:
        # Get all conflict names for this model
        conflict_names = df[df['model'] == model]['conflict_name'].unique()
        
        for conflict_name in conflict_names:
            row = {'model': model, 'Conflict Type': conflict_name_mapping[conflict_name]}

            
            def get_values(dataset):
                base = df[(df['model'] == model) & 
                         (df['policy'] == policy) & 
                         (df['conflict_name'] == conflict_name) &
                         (df['dataset'] == dataset)]
                return (base['primary_constraint_met'].values[0],
                       base['secondary_constraint_met'].values[0])

            # Get values for each dataset
            normal_simple = get_values('conflicting_instructions')
            reversed_simple = get_values('conflicting_instructions_reversed') 
            normal_rich = get_values('conflicting_instructions_rich_context')
            reversed_rich = get_values('conflicting_instructions_rich_context_reversed')

            # Calculate metrics
            simple_constraintA = (normal_simple[0] + reversed_simple[1])
            simple_constraintB = (normal_simple[1] + reversed_simple[0])
            rich_constraintA = (normal_rich[0] + reversed_rich[1])
            rich_constraintB = (normal_rich[1] + reversed_rich[0])

            simple_leading = (normal_simple[0] + reversed_simple[0])
            simple_trailing = (normal_simple[1] + reversed_simple[1])
            rich_leading = (normal_rich[0] + reversed_rich[0])
            rich_trailing = (normal_rich[1] + reversed_rich[1])
            
            row.update({
                'Sim. Pos.': f"{((simple_leading - simple_trailing)/2):.3f}",
                'Sim. Sem.': f"{((simple_constraintA - simple_constraintB)/2):.3f}",
                'Rich Pos.': f"{((rich_leading - rich_trailing)/2):.3f}",
                'Rich Sem.': f"{((rich_constraintA - rich_constraintB)/2):.3f}"
            })


            
            results.append(row)

    # Convert to DataFrame
    result_df = pd.DataFrame(results).round(3)

    # Save the results
    result_df.to_csv(f'{output_dir}/table2_{tag}.csv', index=False)
    latex_table = csv_to_latex(result_df)
    with open(f'{output_dir}/table2_latex_{tag}', 'w') as f:
        f.write(latex_table)



def draw_polar_plots(df, filename):

    # Remove the header row and reset the column names
    df.columns = df.iloc[0]
    df = df[1:].reset_index(drop=True)

    # Rename columns for better readability
    df.columns = ["Model", "Type", "Value1", "Value2", "Value3", "Value4"]

    # Convert numeric columns to float
    df[["Value1", "Value2", "Value3", "Value4"]] = df[["Value1", "Value2", "Value3", "Value4"]].astype(float)

    # Function to create the plot with given transformation
    def create_plot(df, n=None):
        # Create a copy of the dataframe to avoid modifying the original
        plot_df = df.copy()
        
        # Apply nth root transformation if specified
        if n is not None:
            numeric_columns = ["Value1", "Value2", "Value3", "Value4"]
            plot_df[numeric_columns] = plot_df[numeric_columns] ** (1/n)

        # Extract unique models
        models = plot_df["Model"].unique()

        # Use a single color instead of sector_colors
        bar_color = 'blue'  # You can change this to any color you prefer

        # Define maximum allowable bar width in radians (60 degrees = π/3 radians)
        max_bar_width = np.pi / 3

        # Create subplots (2x3 layout)
        fig, axes = plt.subplots(2, 3, figsize=(18, 12), subplot_kw={'projection': 'polar'})
        axes = axes.flatten()

        # Plot each model
        for i, model in enumerate(models):
            ax = axes[i]
            
            sub_df = plot_df[plot_df["Model"] == model]
            labels = [label.replace(" ", "\n") for label in sub_df["Type"].values]
            angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)

            bar_lengths = sub_df["Value1"].values
            bar_widths = sub_df["Value2"].values

            # Normalize widths to be at most 60 degrees
            bar_widths = np.clip(bar_widths, 0, max_bar_width)

            for j, (angle, length, width) in enumerate(zip(angles, bar_lengths, bar_widths)):
                # Always draw the bar, even if length is 0
                ax.bar(angle, length, width=width, alpha=0.6, color=bar_color, 
                    edgecolor='black', linewidth=2, bottom=0)  # Added bottom=0

            # Add circle at r=1 with very subtle, light gray line
            ax.plot(np.linspace(0, 2*np.pi, 100), np.ones(100), color='lightgray', linewidth=0.05, alpha=0.3)
            
            ax.set_xticks(angles)
            ax.set_xticklabels(labels, fontsize=16)
            ax.set_yticklabels([])
            ax.set_title(model, fontsize=20, y=1.05)
            ax.set_ylim(0, 1)
            # Make the polar spine (outer circle) very subtle
            ax.spines['polar'].set_color('lightgray')
            ax.spines['polar'].set_linewidth(0.05)
            ax.spines['polar'].set_alpha(0.3)

        # Add more spacing between subplots
        plt.subplots_adjust(hspace=0.2)
        plt.tight_layout()
        return fig

    # Generate both versions
    # Version with square root transformation
    fig1 = create_plot(df, n=2)
    plt.savefig(f"{output_dir}/{filename}_simple_sqrt.pdf", format='pdf', bbox_inches='tight')
    plt.close()

    # Version without transformation
    fig2 = create_plot(df, n=None)
    plt.savefig(f"{output_dir}/{filename}_simple_notrans.pdf", format='pdf', bbox_inches='tight')
    plt.close()



    def create_comparison_plot(df, n=None):
        # Create a copy of the dataframe to avoid modifying the original
        plot_df = df.copy()
        
        # Apply nth root transformation if specified
        if n is not None:
            numeric_columns = ["Value1", "Value2", "Value3", "Value4"]
            plot_df[numeric_columns] = plot_df[numeric_columns] ** (1/n)

        # Define two colors for the different value pairs
        color_values12 = 'blue'  # Color for Value1 and Value2
        color_values34 = 'red'   # Color for Value3 and Value4

        # Define maximum allowable bar width in radians (60 degrees = π/3 radians)
        max_bar_width = np.pi / 3

        # Create subplots (2x3 layout)
        fig, axes = plt.subplots(2, 3, figsize=(18, 12), subplot_kw={'projection': 'polar'})
        axes = axes.flatten()

        # Plot each model
        models = plot_df["Model"].unique()
        for i, model in enumerate(models):
            ax = axes[i]
            
            sub_df = plot_df[plot_df["Model"] == model]
            labels = [label.replace(" ", "\n") for label in sub_df["Type"].values]
            angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)

            bar_lengths1 = sub_df["Value1"].values
            bar_widths1 = sub_df["Value2"].values
            bar_lengths2 = sub_df["Value3"].values
            bar_widths2 = sub_df["Value4"].values

            # Normalize widths to be at most 60 degrees
            bar_widths1 = np.clip(bar_widths1, 0, max_bar_width)
            bar_widths2 = np.clip(bar_widths2, 0, max_bar_width)

            for j, (angle, length1, width1, length2, width2) in enumerate(zip(angles, bar_lengths1, bar_widths1, bar_lengths2, bar_widths2)):
                # Always draw both bars, even if lengths are 0
                ax.bar(angle - width1/16, length1, width=width1, alpha=0.6, color=color_values12, 
                    edgecolor='black', linewidth=2, label='Simple' if j == 0 else "", bottom=0)
                ax.bar(angle + width2/16, length2, width=width2, alpha=0.6, color=color_values34, 
                    edgecolor='black', linewidth=2, label='Rich' if j == 0 else "", bottom=0)

            # Add circle at r=1 with very subtle, light gray line
            ax.plot(np.linspace(0, 2*np.pi, 100), np.ones(100), color='lightgray', linewidth=0.05, alpha=0.3)
            
            ax.set_xticks(angles)
            ax.set_xticklabels(labels, fontsize=16)
            ax.set_yticklabels([])
            ax.set_title(model, fontsize=20, y=1.05)
            ax.set_ylim(0, 1)
            # Make the polar spine (outer circle) very subtle
            ax.spines['polar'].set_color('lightgray')
            ax.spines['polar'].set_linewidth(0.05)
            ax.spines['polar'].set_alpha(0.3)
            
            # Add legend to each subplot
            ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

        # Add more spacing between subplots
        plt.subplots_adjust(hspace=0.2, wspace=0.4)  # Increased wspace for legend
        plt.tight_layout()
        return fig

    # Generate both versions with the comparison plot
    # Version with square root transformation
    fig1 = create_comparison_plot(df, n=2)
    plt.savefig(f"{output_dir}/{filename}_comparison_with_sqrt.pdf", format='pdf', bbox_inches='tight')
    plt.close()

    # Version without transformation
    fig2 = create_comparison_plot(df, n=None)
    plt.savefig(f"{output_dir}/{filename}_comparison_notrans.pdf", format='pdf', bbox_inches='tight')
    plt.close()




def figure1():
    """Generate Figure1 analyzing separation performance by conflict type."""

    policy = "basic_separation"
    
    # Create the result table
    results = []
    
    # Group by model and conflict_name
    for model in models:
        # Get all conflict names for this model
        conflict_names = df[df['model'] == model]['conflict_name'].unique()
        
        for conflict_name in conflict_names:
            row = {'model': model, 'Conflict Type': conflict_name_mapping[conflict_name]}

            metrics = metrics_computation(model, policy, conflict_name)
            row.update(metrics)
            results.append(row)

    # Convert to DataFrame
    result_df = pd.DataFrame(results)

    filename = f'{tag}_radar_plot_sep'
    draw_polar_plots(result_df, filename)

    result_df.to_csv(f'{output_dir}/{filename}.csv', index=False)



if __name__ == "__main__":
    table1()
    figure1()