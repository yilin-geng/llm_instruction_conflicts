import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

sns.set_theme(style="whitegrid")

# Example data indicating direction (left = negative, right = positive).
# Each dimension has an array of 6 values (one for each model).
# For illustration, we just pick random left/right signs. 
# Replace these with real data or the correct signs you need:

# mock some data
dimensions = {
    "English vs. French":    [0.25, -0.7, 0.3, 0.5, -0.5, 0.5],
    "capital vs. lower":     [-0.75, 0.14, -0.6, 0.32, 0.4, 0.2],
    "long vs. short":        [0.14, -0.63, 0.38, 0.25, 0.45, -0.3],
    "include vs. exclude":   [0.99, -0.7, 0.5, -0.3, 0.2, 0.4]
}

# Model labels in the order corresponding to the arrays above
models = ["claude", "gpt4o", "gpt4omini", "llama8b", "llama70b", "qwen"]

# Prepare to plot: one subplot per dimension
fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(7, 10))

# Just in case 'axes' is a numpy array, we iterate over it
for ax, (dimension_name, direction_values) in zip(axes, dimensions.items()):
    
    y_positions = np.arange(len(models))
    
    # We will plot horizontal bars
    ax.barh(y_positions, direction_values, 
            color=["#007ACC" if val > 0 else "#FF6B6B" for val in direction_values],
            align='center', height=0.6)
    
    # Add model labels on the y-axis
    ax.set_yticks(y_positions)
    ax.set_yticklabels(models)
    
    # Draw a vertical line at x=0 for visual reference
    ax.axvline(0, color='black', linewidth=1)
    
    # Title for each subplot
    ax.set_title(dimension_name)
    
    # Optionally, set a limit so bars can be seen clearly
    ax.set_xlim(-1.5, 1.5)

# Tight layout for better spacing
plt.tight_layout()
plt.show()
