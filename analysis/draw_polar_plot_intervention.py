import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def create_intervention_plots(df, output_dir='analysis/plots', filename='intervention_radar_plot'):
    # Create a copy of the dataframe to avoid modifying the original
    plot_df = df.copy()
    
    # Set up the figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7), subplot_kw={'projection': 'polar'})
    
    # Colors matching draw_tendency_plot.py
    RED = 'red'    # For interventions
    BLUE = 'blue'   # For pure separation/baseline
    max_bar_width = np.pi/3  # 60 degrees in radians
    
    def plot_radar(ax, data, title, n=2):
        # Get unique conflict types
        labels = data['Conflict'].unique()
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
        
        # Apply square root transformation if n is specified
        if n is not None:
            data['PAR'] = data['PAR'] ** (1/n)
            data['1-|CB|'] = data['1-|CB|'] ** (1/n)
        
        # Plot data for each model
        for model in data['Model'].unique():
            model_data = data[data['Model'] == model]
            
            # PAR values
            bar_lengths = model_data['PAR'].values
            # Width values from 1-|CB|
            bar_widths = model_data['1-|CB|'].values
            bar_widths = np.clip(bar_widths * max_bar_width, 0, max_bar_width)
            
            # Plot bars
            for angle, length, width in zip(angles, bar_lengths, bar_widths):
                color = RED if model != 'Llama-8B' else BLUE
                ax.bar(angle, length, width=width, alpha=0.6, color=color,
                      edgecolor='black', linewidth=2, bottom=0)
        
        # Add circle at r=1 with subtle, light gray line
        ax.plot(np.linspace(0, 2*np.pi, 100), np.ones(100), 
                color='lightgray', linewidth=0.05, alpha=0.3)
        
        # Customize the plot
        ax.set_xticks(angles)
        ax.set_xticklabels(labels, fontsize=16)
        ax.set_yticklabels([])
        ax.set_title(title, fontsize=20, y=1.05)
        ax.set_ylim(0, 1)
        
        # Make the polar spine (outer circle) very subtle
        ax.spines['polar'].set_color('lightgray')
        ax.spines['polar'].set_linewidth(0.05)
        ax.spines['polar'].set_alpha(0.3)
    
    # Create the two plots (switched order)
    prompting_data = plot_df[plot_df['Model'].isin(['Llama-8B', 'Llama-8B-Prompting'])].copy()
    finetuning_data = plot_df[plot_df['Model'].isin(['Llama-8B', 'Fintuned Llama-8B'])].copy()
    
    plot_radar(ax1, prompting_data, 'Prompting', n=2)
    plot_radar(ax2, finetuning_data, 'Finetuning', n=2)
    
    # Add legend
    legend_elements = [
        plt.Rectangle((0,0), 1, 1, facecolor=RED, alpha=0.6, label='Interventions'),
        plt.Rectangle((0,0), 1, 1, facecolor=BLUE, alpha=0.6, label='Pure Separation')
    ]
    fig.legend(handles=legend_elements, loc='center', bbox_to_anchor=(0.5, 0),
              ncol=2, fontsize=12)
    
    # Adjust layout
    plt.subplots_adjust(hspace=0.2)
    plt.tight_layout(rect=[0, 0.05, 1, 0.95])
    
    # Save plots
    plt.savefig(f"{output_dir}/{filename}.pdf", format='pdf', bbox_inches='tight', dpi=300)
    plt.close()

# Read and process the data
df = pd.read_csv('/Users/yigeng/Documents/Github/instruction_conflicts/analysis/tables/polar_plot_interventions_simple.csv')
create_intervention_plots(df)