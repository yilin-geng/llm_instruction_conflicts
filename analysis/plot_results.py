import pandas as pd
import numpy as np


conflict_name_mapping = {
    'case_conflict': 'Case',
    'keyword_forbidden_conflict: awesome_need': 'Keyword Usage',
    'keyword_frequency_conflict: like_5_2': 'Keyword Frequency',
    'language_conflict: en_fr': 'Language',
    'num_sentence_conflict: 10_5': 'Sentence Count',
    'word_length_conflict: 300_50': 'Word Length'
}

def csv_to_latex(df):
    # Round numeric columns to 3 decimal places
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    df[numeric_columns] = df[numeric_columns].round(3)
    
    # Convert to latex with specific float format
    latex_text = df.to_latex(index=False, float_format=lambda x: '{:.3f}'.format(x))
    return latex_text
    
    


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


def metrics_computation(model, policy, conflict_name):
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

    return {
        'PES simple': simple_pes,
        'INS simple': simple_ins,
        'PES rich': rich_pes,
        'INS rich': rich_ins
    }
    


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
    result_df.to_csv(f'{output_dir}/table2.csv', index=False)
    latex_table = csv_to_latex(result_df)
    with open(f'{output_dir}/table2_latex', 'w') as f:
        f.write(latex_table)
    # print(result_df.to_string())



def table3():
    """Generate Table 3 analyzing separation performance by conflict type."""

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
    result_df = pd.DataFrame(results).round(3)

    # Save the results
    result_df.to_csv(f'{output_dir}/table3.csv', index=False)
    latex_table = csv_to_latex(result_df)
    with open(f'{output_dir}/table3_latex', 'w') as f:
        f.write(latex_table)



def temp():

    # check performance of qwen2.5-7b-instruct on all conflicts
    conflict_names = df[df['model'] == 'qwen2.5-7b-instruct']['conflict_name'].unique()
    model = 'qwen2.5-7b-instruct'
    policy = 'basic_separation'
    for conflict_name in conflict_names:
        def get_values(dataset):
                    base = df[(df['model'] == model) & 
                            (df['policy'] == policy) & 
                            (df['conflict_name'] == conflict_name) &
                            (df['dataset'] == dataset)]
                    return (base['primary_constraint_met'].values[0],
                        base['secondary_constraint_met'].values[0])
        
        normal_simple = get_values('conflicting_instructions')
        reversed_simple = get_values('conflicting_instructions_reversed') 
        normal_rich = get_values('conflicting_instructions_rich_context')
        reversed_rich = get_values('conflicting_instructions_rich_context_reversed')

        print(f'conflict name: {conflict_name}')
        print(f'normal: {normal_simple}')
        print(f'reversed: {reversed_simple}')
        
        



if __name__ == "__main__":
    # table1()
    table2()
    # table3()
    # temp()