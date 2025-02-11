import pandas as pd
import numpy as np


def generate_latex_table1(df):
    latex_str = []
    # Start table
    latex_str.append(r"\begin{table*}[t]")
    latex_str.append(r"\centering")
    latex_str.append(r"\small")
    
    # Column format: one for model name, 4 for simple, 4 for rich, 1 for average
    latex_str.append(r"\begin{tabular}{l|cccc|cccc|c}")
    latex_str.append(r"\toprule")
    
    # Main header
    latex_str.append(r"& \multicolumn{4}{c|}{\textbf{Simple Instructions}} & " + 
                    r"\multicolumn{4}{c|}{\textbf{Rich Instructions}} & ")
    latex_str.append(r"\multicolumn{1}{c}{\textbf{Model}}")
    latex_str.append(r"\\")
    
    # Subheader
    latex_str.append(r"\cmidrule(lr){2-5} \cmidrule(lr){6-9}")
    latex_str.append(r"\textbf{Model} & IF. & Basic & Task & Emph. & " + 
                    r"IF. & Basic & Task & Emph. & \textbf{Average} \\")
    latex_str.append(r"& Baseline& Sep. & Sep. & Sep. & Baseline & Sep. & Sep. & Sep. & \textbf{Sep.} \\")
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
    
    # Caption
    latex_str.append(r"\caption{IF. Baseline stands for the Instruction Following Baseline, where only a single constraint is present, and averaged over the conflicting pair. 'Sep.' stands for Separation. Sep. values show the percentage of responses where the primary constraint was followed. Model Average shows the overall prioritization performance of the model with different separation templates and on different data.}")
    latex_str.append(r"\label{tab:model_performance}")
    latex_str.append(r"\end{table*}")
    
    return "\n".join(latex_str)


# Read the evaluation results
df = pd.read_csv('analysis/conflict_level_summary_response.csv')
# df = pd.read_csv('analysis/dataset_level_summary_response.csv')

models = [
    "qwen2.5-7b-instruct",
    "gpt-4o-mini-2024-07-18",
    "gpt-4o-2024-11-20",
    "claude-3-5-sonnet-20241022",
    "Llama-3.1-8B",
    "Llama-3.1-70B",
]

output_dir = 'plots'


def table1():
    """Generate Table 1 comparing model performance across different policies."""


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
    result_df.to_csv(f'{output_dir}/table1.csv', index=False)
    latex_table = generate_latex_table1(result_df)
    with open(f'{output_dir}/table1_latex', 'w') as f:
        f.write(latex_table)
    # print(result_df.to_string())


def table2():
    """Generate Table 2 analyzing baseline_all_user performance by conflict type. (constraint preference)"""


    policy = "baseline_all_user"
    
    # Create the result table
    results = []
    
    # Group by model and conflict_name
    for model in models:
        # Get all conflict names for this model
        conflict_names = df[df['model'] == model]['conflict_name'].unique()
        
        for conflict_name in conflict_names:
            row = {'model': model, 'conflict_name': conflict_name}
            
            # Simple context (normal and reversed)
            normal_simple_A = df[(df['model'] == model) & 
                             (df['policy'] == policy) & 
                             (df['conflict_name'] == conflict_name) &
                             (df['dataset'] == 'conflicting_instructions')]['primary_constraint_met'].values[0]
            
            reversed_simple_A = df[(df['model'] == model) & 
                               (df['policy'] == policy) & 
                               (df['conflict_name'] == conflict_name) &
                               (df['dataset'] == 'conflicting_instructions_reversed')]['secondary_constraint_met'].values[0]
            
            normal_simple_B = df[(df['model'] == model) & 
                             (df['policy'] == policy) & 
                             (df['conflict_name'] == conflict_name) &
                             (df['dataset'] == 'conflicting_instructions')]['secondary_constraint_met'].values[0]
            
            reversed_simple_B = df[(df['model'] == model) & 
                               (df['policy'] == policy) & 
                               (df['conflict_name'] == conflict_name) &
                               (df['dataset'] == 'conflicting_instructions_reversed')]['primary_constraint_met'].values[0]
            
            # Rich context (normal and reversed)
            normal_rich_A = df[(df['model'] == model) & 
                           (df['policy'] == policy) & 
                           (df['conflict_name'] == conflict_name) &
                           (df['dataset'] == 'conflicting_instructions_rich_context')]['primary_constraint_met'].values[0]
            
            reversed_rich_A = df[(df['model'] == model) & 
                             (df['policy'] == policy) & 
                             (df['conflict_name'] == conflict_name) &
                             (df['dataset'] == 'conflicting_instructions_rich_context_reversed')]['secondary_constraint_met'].values[0]
            
            normal_rich_B = df[(df['model'] == model) & 
                           (df['policy'] == policy) & 
                           (df['conflict_name'] == conflict_name) &
                           (df['dataset'] == 'conflicting_instructions_rich_context')]['secondary_constraint_met'].values[0]
            
            reversed_rich_B = df[(df['model'] == model) & 
                             (df['policy'] == policy) & 
                             (df['conflict_name'] == conflict_name) &
                             (df['dataset'] == 'conflicting_instructions_rich_context_reversed')]['primary_constraint_met'].values[0]
            
            simple_constraintA = (normal_simple_A + reversed_simple_A) / 2
            simple_constraintB = (normal_simple_B + reversed_simple_B) / 2
            rich_constraintA = (normal_rich_A + reversed_rich_A) / 2
            rich_constraintB = (normal_rich_B + reversed_rich_B) / 2
            
            row.update({
                'simple_constraintA/B': f"{simple_constraintA:.3f} / {simple_constraintB:.3f}",
                'rich_constraintA/B': f"{rich_constraintA:.3f} / {rich_constraintB:.3f}"
            })
            
            results.append(row)

    # Convert to DataFrame
    result_df = pd.DataFrame(results).round(3)

    # Save the results
    result_df.to_csv(f'{output_dir}/table2.csv', index=False)
    # print(result_df.to_string())


def table3():
    """Generate Table 2 analyzing baseline_all_user performance by conflict type. (location preference)"""

    policy = "baseline_all_user"
    
    # Create the result table
    results = []
    
    # Group by model and conflict_name
    for model in models:
        # Get all conflict names for this model
        conflict_names = df[df['model'] == model]['conflict_name'].unique()
        
        for conflict_name in conflict_names:
            row = {'model': model, 'conflict_name': conflict_name}
            
            # Simple context (normal and reversed)
            normal_simple_leading = df[(df['model'] == model) & 
                             (df['policy'] == policy) & 
                             (df['conflict_name'] == conflict_name) &
                             (df['dataset'] == 'conflicting_instructions')]['primary_constraint_met'].values[0]
            
            reversed_simple_leading = df[(df['model'] == model) & 
                               (df['policy'] == policy) & 
                               (df['conflict_name'] == conflict_name) &
                               (df['dataset'] == 'conflicting_instructions_reversed')]['primary_constraint_met'].values[0]
            
            normal_simple_trailing = df[(df['model'] == model) & 
                             (df['policy'] == policy) & 
                             (df['conflict_name'] == conflict_name) &
                             (df['dataset'] == 'conflicting_instructions')]['secondary_constraint_met'].values[0]
            
            reversed_simple_trailing = df[(df['model'] == model) & 
                               (df['policy'] == policy) & 
                               (df['conflict_name'] == conflict_name) &
                               (df['dataset'] == 'conflicting_instructions_reversed')]['secondary_constraint_met'].values[0]
            
            # Rich context (normal and reversed)
            normal_rich_leading = df[(df['model'] == model) & 
                           (df['policy'] == policy) & 
                           (df['conflict_name'] == conflict_name) &
                           (df['dataset'] == 'conflicting_instructions_rich_context')]['primary_constraint_met'].values[0]
            
            reversed_rich_leading = df[(df['model'] == model) & 
                             (df['policy'] == policy) & 
                             (df['conflict_name'] == conflict_name) &
                             (df['dataset'] == 'conflicting_instructions_rich_context_reversed')]['primary_constraint_met'].values[0]
            
            normal_rich_trailing = df[(df['model'] == model) & 
                           (df['policy'] == policy) & 
                           (df['conflict_name'] == conflict_name) &
                           (df['dataset'] == 'conflicting_instructions_rich_context')]['secondary_constraint_met'].values[0]
            
            reversed_rich_trailing = df[(df['model'] == model) & 
                             (df['policy'] == policy) & 
                             (df['conflict_name'] == conflict_name) &
                             (df['dataset'] == 'conflicting_instructions_rich_context_reversed')]['secondary_constraint_met'].values[0]
            
            simple_leading = (normal_simple_leading + reversed_simple_leading) / 2
            simple_trailing = (normal_simple_trailing + reversed_simple_trailing) / 2
            rich_leading = (normal_rich_leading + reversed_rich_leading) / 2
            rich_trailing = (normal_rich_trailing + reversed_rich_trailing) / 2
            
            row.update({
                'simple_constraint_leading/trailing': f"{simple_leading:.3f} / {simple_trailing:.3f}",
                'rich_constraint_leading_trailing': f"{rich_leading:.3f} / {rich_trailing:.3f}"
            })
            
            results.append(row)

    # Convert to DataFrame
    result_df = pd.DataFrame(results).round(3)

    # Save the results
    result_df.to_csv(f'{output_dir}/table3.csv', index=False)
    # print(result_df.to_string())


if __name__ == "__main__":
    table1()
    table2()
    table3()