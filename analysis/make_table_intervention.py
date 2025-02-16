import pandas as pd
import numpy as np
import os

df = pd.read_csv('analysis/conflict_level_summary_processed_response_test_only_merged.csv')
tag = 'processed'

conflict_name_mapping = {
    'case_conflict': 'Case',
    'keyword_forbidden_conflict: awesome_need': 'Keyword Usage',
    'keyword_frequency_conflict: like_5_2': 'Keyword Frequency',
    'language_conflict: en_fr': 'Language',
    'num_sentence_conflict: 10_5': 'Sentence Count',
    'word_length_conflict: 300_50': 'Word Length'
}


model_mapping = {
    'Llama-3.1-8B-conflict': 'Fintuned Llama-8B',
    'Llama-3.1-8B': 'Llama-8B',
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
    'baseline_all_user': 'NP.'
}

output_dir = 'analysis/tables'





def compute_rates_per_conflict(model, policy, conflict_name, context_type='simple'):

    def get_values(dataset):
                base = df[(df['model'] == model) & 
                         (df['policy'] == policy) & 
                         (df['conflict_name'] == conflict_name) &
                         (df['dataset'] == dataset)]
                assert len(base) == 1
                return (float(base['primary_constraint_met'].values[0]),
                       float(base['secondary_constraint_met'].values[0]))

    if context_type == 'simple':
        R1_a, R2_a = get_values('conflicting_instructions')
        R1_b, R2_b = get_values('conflicting_instructions_reversed') 
    else:
        R1_a, R2_a = get_values('conflicting_instructions_rich_context')
        R1_b, R2_b = get_values('conflicting_instructions_rich_context_reversed')

    return {'R1_a': R1_a, 'R2_a': R2_a, 'R1_b': R1_b, 'R2_b': R2_b}
    


def compute_o1_obedience_rate_per_conflict(model, policy, conflict_name, context_type='simple'):
    rates = compute_rates_per_conflict(model, policy, conflict_name, context_type)
    R1 = (rates['R1_a'] + rates['R1_b'])/2

    return R1


def compute_priority_adherence_per_conflict(model, policy, conflict_name, context_type='simple'):
    # Priority Following = R1/(R1+R2) - R2/(R1+R2) where R1 is R1_a+R1_b and R2 is R2_a+R2_b
    rates = compute_rates_per_conflict(model, policy, conflict_name, context_type)
    R1 = (rates['R1_a'] + rates['R1_b'])/2
    R2 = (rates['R2_a'] + rates['R2_b'])/2

    priority_adherence = R1/(R1+R2) # no penalty for R2
    # priority_adherence = (R1-R2)/(R1+R2) # penalty for R2 but we need to normalize to 0-1 (too much explanation)

    # sanity check priority adherence is between 0 and 1
    assert priority_adherence >= 0 and priority_adherence <= 1

    return priority_adherence



def compute_constraint_bias_per_conflict(model, policy, conflict_name, context_type='simple'):
    policy = 'baseline_all_user' # override policy to baseline_all_user
    rates = compute_rates_per_conflict(model, policy, conflict_name, context_type)

    Ra_raw = (rates['R1_a'] + rates['R2_b'])/2
    Rb_raw = (rates['R2_a'] + rates['R1_b'])/2

    Ra = Ra_raw/(Ra_raw+Rb_raw)
    Rb = Rb_raw/(Ra_raw+Rb_raw)

    try:
        # sanity check, with tolerance of 1e-6
        assert np.isclose(Ra + Rb, 1, atol=1e-6)
    except:
        print(f"Ra: {Ra}, Rb: {Rb}, Ra+Rb: {Ra+Rb}")

    constraint_bias = Rb - Ra # where a larger value means more bias towards constraint b

    # sanity check constraint bias is between -1 and 1
    assert constraint_bias >= -1 and constraint_bias <= 1


    return constraint_bias

def compute_normalized_constraint_bias_per_conflict(model, policy, conflict_name, context_type='simple'):
    constraint_bias = compute_constraint_bias_per_conflict(model, policy, conflict_name, context_type)
    constraint_bias_normalized = 1 - np.abs(constraint_bias)

    # sanity check constraint bias normalized is between 0 and 1
    assert constraint_bias_normalized >= 0 and constraint_bias_normalized <= 1

    return constraint_bias_normalized





def csv_to_latex(df, precision=1):
    latex_text = df.to_latex(index=False, float_format=lambda x: '{:.{precision}f}'.format(x, precision=precision))
    return latex_text

def save_table(table_name, results_df, context_type='simple', percentage_flag = True, precision=1, latex_flag=True):
    numeric_columns = results_df.select_dtypes(include=['float64', 'int64']).columns
    if percentage_flag:
        results_df[numeric_columns] = (100 * results_df[numeric_columns]).round(precision)
    else:
        results_df[numeric_columns] = results_df[numeric_columns].round(precision)
    results_df.to_csv(f'{output_dir}/{table_name}_{context_type}.csv', index=False)

    if latex_flag:
        latex_table = csv_to_latex(results_df, precision=precision)
        with open(f'{output_dir}/{table_name}_{context_type}_latex', 'w') as f:
            f.write(latex_table)


def model_mapping_latex():
    """Generate a LaTeX table showing the mapping between model abbreviations and full names."""
    latex_str = []
    
    # Start table
    latex_str.append(r"\begin{table}[h]")
    latex_str.append(r"\centering")
    latex_str.append(r"\begin{tabular}{ll}")
    latex_str.append(r"\toprule")
    latex_str.append(r"\textbf{Abbreviation} & \textbf{Model Version} \\")
    latex_str.append(r"\midrule")
    
    # Add each model mapping
    for full_name, abbrev in model_mapping.items():
        # Escape underscores in the full name for LaTeX
        full_name_escaped = full_name.replace('_', r'\_')
        latex_str.append(f"{abbrev} & {full_name_escaped} \\\\")
    
    # End table
    latex_str.append(r"\bottomrule")
    latex_str.append(r"\end{tabular}")
    latex_str.append(r"\caption{Model abbreviation mapping}")
    latex_str.append(r"\label{tab:model-mapping}")
    latex_str.append(r"\end{table}")
    
    # Join all lines and write to file
    latex_table = '\n'.join(latex_str)
    with open(f'{output_dir}/model_mapping_latex', 'w') as f:
        f.write(latex_table)
    
    return latex_table


def create_model_policy_table_for_metric(models, policies, metric_function, context_type='simple'):
    "DataFrame with models as rows and policies as columns"
    results = []
    
    for model in models:
        model_results = {'Model': model_mapping[model]}
        
        for policy in policies:
            policy_values = []
            for conflict_name in conflict_name_mapping.keys():
                try:
                    value = metric_function(model, policy, conflict_name, context_type)
                    policy_values.append(value)
                except:
                    continue
            
            # Average across all conflict types
            if policy_values:
                model_results[policy_mapping[policy]] = np.mean(policy_values)
            else:
                model_results[policy_mapping[policy]] = np.nan
                
        results.append(model_results)
    
    # Create DataFrame and round values
    results_df = pd.DataFrame(results)
    return results_df


def create_model_conflict_metric_table_for_policy(models, policy, metric_functions, context_type='simple'):
    "DataFrame with models and conflict types as rows and different metrics as columns"
    results = []
    
    for model in models:
        for conflict_name in conflict_name_mapping.keys():
            row = {
                'Model': model_mapping[model],
                'Conflict': conflict_name_mapping[conflict_name]
            }
            
            # Calculate each metric for this model/conflict combination
            for metric_name, metric_function in metric_functions.items():
                value = metric_function(model, policy, conflict_name, context_type)
                row[metric_name] = value
                    
            results.append(row)
    
    # Create DataFrame and round values
    results_df = pd.DataFrame(results)
    
    # Sort by Model and Conflict
    results_df = results_df.sort_values(['Model', 'Conflict'])
    
    return results_df

def sep_does_not_work_table(table_name, context_type='simple'):
    metric_function = compute_o1_obedience_rate_per_conflict
    models = model_mapping.keys()
    policies = ['constraint_following_baseline', 'basic_separation', 'task_specified_separation', 'emphasized_separation']
    results_df = create_model_policy_table_for_metric(models, policies, metric_function, context_type)
    # add a average column that averages the values across rows excluding 'Model' and 'IF.' and 'NP.'
    results_df['Ave.'] = results_df.drop(columns=['Model', 'IF.']).mean(axis=1)
    save_table(table_name, results_df, context_type)


def sep_does_not_work_table_concatenated(table_name):
    metric_function = compute_o1_obedience_rate_per_conflict
    models = model_mapping.keys()
    policies = ['constraint_following_baseline',  'basic_separation', 'task_specified_separation', 'emphasized_separation']
    results_df_simple = create_model_policy_table_for_metric(models, policies, metric_function, 'simple')
    results_df_rich = create_model_policy_table_for_metric(models, policies, metric_function, 'rich')
    # add results_df_rich to the right of results_df_simple (rename columns)
    results_df_rich.columns = [f'{col}_rich' for col in results_df_rich.columns]
    results_df = pd.concat([results_df_simple, results_df_rich], axis=1)
    results_df = results_df.drop(columns=['Model_rich'])
    # add a average column that averages the values across rows excluding 'Model' and 'IF.' and 'IF._rich'
    results_df['Ave.'] = results_df.drop(columns=['Model', 'IF.', 'IF._rich']).mean(axis=1)
    save_table(table_name, results_df, 'concatenated')


def prompt_does_not_work_table(table_name, context_type='simple'):
    metric_function = compute_o1_obedience_rate_per_conflict
    models = model_mapping.keys()
    policies = ['basic_separation', 'unmarked_system_basic', 'marked_system_basic', 'unmarked_user_basic', 'marked_user_basic']
    results_df = create_model_policy_table_for_metric(models, policies, metric_function, context_type)
    save_table(table_name, results_df, context_type)


def prompt_does_not_work_table_concatenated(table_name):
    metric_function = compute_o1_obedience_rate_per_conflict
    models = model_mapping.keys()
    policies = ['basic_separation', 'unmarked_system_basic', 'marked_system_basic', 'unmarked_user_basic', 'marked_user_basic']
    results_df_simple = create_model_policy_table_for_metric(models, policies, metric_function, 'simple')
    results_df_rich = create_model_policy_table_for_metric(models, policies, metric_function, 'rich')
    results_df_rich.columns = [f'{col}_rich' for col in results_df_rich.columns]
    results_df = pd.concat([results_df_simple, results_df_rich], axis=1)
    results_df = results_df.drop(columns=['Model_rich'])
    results_df['Ave.'] = results_df.drop(columns=['Model']).mean(axis=1)
    save_table(table_name, results_df, 'concatenated')


def polar_plot_table(table_name, policy, context_type='simple'):
    models = model_mapping.keys()
    metric_functions = {
        'PAR': compute_priority_adherence_per_conflict,
        '1-|CB|': compute_normalized_constraint_bias_per_conflict
    }
    results_df = create_model_conflict_metric_table_for_policy(models, policy, metric_functions, context_type)
    save_table(table_name, results_df, context_type, percentage_flag=False, precision=4)


def tendency_plot_table(table_name, context_type='simple'):
    models = model_mapping.keys()
    policy = "baseline_all_user" # might be overridden by baseline_all_user
    metric_functions = {
        'CB': compute_constraint_bias_per_conflict
    }
    results_df = create_model_conflict_metric_table_for_policy(models, policy, metric_functions, context_type)
    save_table(table_name, results_df, context_type, percentage_flag=False, precision=4)

        
def conflict_acknowledgement_table(table_name, policy, context_type='simple'):
    """Generate table showing conflict acknowledgement rates and constraint following rates when conflicts are acknowledged."""
    
    # Load the evaluated responses
    eval_df = pd.read_csv('analysis/evaluated_processed_response.csv')
    
    results = []
    models = model_mapping.keys()
    
    for model in models:
        row = {'Model': model_mapping[model]}
        
        # Filter data based on context type and policy
        if context_type == 'simple':
            datasets = ['conflicting_instructions', 'conflicting_instructions_reversed']
        else:
            datasets = ['conflicting_instructions_rich_context', 'conflicting_instructions_rich_context_reversed']
            
        model_data = eval_df[
            (eval_df['model'] == model) & 
            (eval_df['policy'] == policy) &
            (eval_df['dataset'].isin(datasets))
        ]
        
        # Calculate ECAR (Explicit Conflict Acknowledgement Rate)
        row['ECAR'] = model_data['conflict_recognized'].mean()
        
        # Calculate R1 and R2 for acknowledged conflicts
        acknowledged_data = model_data[model_data['conflict_recognized'] == 1]
        if len(acknowledged_data) > 0:
            row['R1'] = acknowledged_data['primary_constraint_met'].mean()
            row['R2'] = acknowledged_data['secondary_constraint_met'].mean()
            row['R3'] = 1 - row['R1'] - row['R2']
        else:
            row['R1'] = np.nan
            row['R2'] = np.nan
            row['R3'] = np.nan
            
        results.append(row)
    
    # Create DataFrame and round values
    results_df = pd.DataFrame(results)
    
    # Save table
    save_table(table_name, results_df, context_type)



def polar_plot_table(context_type='simple'):
    baseline_finetune_policy = 'basic_separation' # we want to compare with out of box performance under basic separation
    # we also want to compare with the basic separation policy under finetuned model
    # and we would like to compare the out of box performance under marked_user_basic policy (best prompting policy)
    finetuned_model = 'Llama-3.1-8B-conflict'
    base_model = 'Llama-3.1-8B'
    metric_functions = {
        'PAR': compute_priority_adherence_per_conflict,
        '1-|CB|': compute_normalized_constraint_bias_per_conflict
    }
    results_df_finetune = create_model_conflict_metric_table_for_policy([finetuned_model, base_model], baseline_finetune_policy, metric_functions, context_type)
    prompting_policy = 'marked_user_basic'
    results_df_prompting = create_model_conflict_metric_table_for_policy([base_model], prompting_policy, metric_functions, context_type)
    results_df_prompting['Model'] = 'Llama-8B-Prompting'
    results_df = pd.concat([results_df_finetune, results_df_prompting])
    save_table('polar_plot_interventions', results_df, context_type, percentage_flag=False, precision=4)


def main():
    os.makedirs(output_dir, exist_ok=True)
    # model_mapping_latex()
    # sep_does_not_work_table('sep_does_not_work', 'simple')
    # # sep_does_not_work_table('sep_does_not_work', 'rich')
    # sep_does_not_work_table_concatenated('sep_does_not_work')
    # prompt_does_not_work_table('prompt_does_not_work', 'simple')
    # # prompt_does_not_work_table('prompt_does_not_work', 'rich')
    # prompt_does_not_work_table_concatenated('prompt_does_not_work')
    # tendency_plot_table('tendency_plot', 'simple')
    # conflict_acknowledgement_table('conflict_acknowledgement_basic_separation', 'basic_separation', 'simple')
    # conflict_acknowledgement_table('conflict_acknowledgement_marked_user_basic', 'marked_user_basic', 'simple')

    polar_plot_table('simple')
if __name__ == '__main__':
    main()




    

