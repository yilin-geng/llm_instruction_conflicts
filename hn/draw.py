# Re-load the uploaded file since execution state was reset
file_path = "basic_sep_no_filter.csv"

# Read the CSV into a DataFrame without preprocessing
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv(file_path, header=None)


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
plt.savefig("basic_sep_with_sqrt.pdf", format='pdf', bbox_inches='tight')
plt.close()

# Version without transformation
fig2 = create_plot(df, n=None)
plt.savefig("basic_sep_no_transform.pdf", format='pdf', bbox_inches='tight')
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
plt.savefig("comparison_with_sqrt.pdf", format='pdf', bbox_inches='tight')
plt.close()

# Version without transformation
fig2 = create_comparison_plot(df, n=None)
plt.savefig("comparison_no_transform.pdf", format='pdf', bbox_inches='tight')
plt.close()