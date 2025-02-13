import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_style("darkgrid")
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['grid.color'] = '0.8'  # Lighter grid for better contrast
plt.rcParams['grid.linestyle'] = '--'

# Read the data
df = pd.read_csv('analysis/tables/tendency_plot_simple.csv')

# Create a mapping for better labels
tendency_mapping = {
    'Language': 'English ← → French',
    'Case': 'Uppercase ← → Lowercase',
    'Word Length': '>300 words ← → <50 words',
    'Sentence Count': '>10 sentences ← → <5 sentences',
    'Keyword Usage': 'Include keyword ← → Avoid keyword',
    'Keyword Frequency': '>5 occurrences ← → <2 occurrences',
}

# Create subplot for each conflict type
fig, axes = plt.subplots(nrows=len(tendency_mapping), ncols=1, figsize=(12, 18))


for idx, (conflict, tendency_label) in enumerate(tendency_mapping.items()):
    ax = axes[idx]
    
    # Get data for this conflict
    conflict_data = df[df['Conflict'] == conflict]
    
    # Create horizontal bar plot
    y_pos = np.arange(len(conflict_data))
    bars = ax.barh(y_pos, conflict_data['CB'].values,
                  color=["#FF6B6B" if x < 0 else "#007ACC" for x in conflict_data['CB'].values],
                  height=0.65)
    
    # Add value labels on the bars
    for i, bar in enumerate(bars):
        width = bar.get_width()
        label_x = width + 0.02 if width >= 0 else width - 0.02
        ha = 'left' if width >= 0 else 'right'
        ax.text(label_x, bar.get_y() + bar.get_height()/2, 
                f'{width:.2f}', va='center', ha=ha,
                fontsize=10, alpha=0.8)
    
    # Customize plot
    ax.set_yticks(y_pos)
    ax.set_yticklabels(conflict_data['Model'].values, fontweight='bold')
    ax.axvline(0, color='black', linewidth=1, alpha=0.3)
    
    # Add title with custom styling
    ax.set_title(tendency_label, pad=20, fontweight='bold', 
                bbox=dict(facecolor='white', edgecolor='gray', alpha=0.8, pad=5))
    
    # Set consistent scale and grid
    ax.set_xlim(-1.1, 1.1)
    ax.grid(True, axis='x', linestyle='--', alpha=0.3)
    
    # Add subtle background color alternation
    ax.set_facecolor('#f8f9fa')
    for i in range(len(y_pos)):
        if i % 2 == 0:
            ax.axhspan(i-0.4, i+0.4, color='white', alpha=0.4)

# Add a common x-axis label at the bottom
fig.text(0.5, 0.02, 'Bias', ha='center', fontsize=14, fontweight='bold')

# Adjust layout
plt.tight_layout(rect=[0, 0.03, 1, 1])

# Save plot with high DPI
plt.savefig("analysis/plots/tendency_analysis.pdf", format='pdf', 
            bbox_inches='tight', dpi=300)
plt.close()
