import matplotlib.pyplot as plt
import matplotlib
import matplotlib.ticker as mtick
import numpy as np
from statsmodels.stats.proportion import proportions_ztest # For z-test of proportions

# # Original script style settings
# plt.style.use('default') # Using default style as a base
# font = {'family' : 'DejaVu Sans', 'weight' : 'normal', 'size'   : 14, }
# lines = {'linewidth' : 2, 'color' : 'black'} # Default line color, bar outlines will be black
# # 'hold' is deprecated, removed. Other axes settings can be applied directly.
# axes_settings = {'edgecolor' : 'black', 'grid' : True, 'titlesize' : 'medium'}
# grid_settings = {'alpha' : 0.1, 'color' : 'black'}
# # figure_settings = {'titlesize' : 32, 'autolayout' : True, 'figsize' : "4, 12"} # figsize set per plot
#
# matplotlib.rc('font', **font)
# matplotlib.rc('lines', **lines)
# # Apply axes and grid settings using plt.rcParams for broader effect if needed,
# # or directly on `ax` object for specific plots.
# # For grid, ax.grid(True, alpha=grid_settings['alpha'], color=grid_settings['color'])
# # For axes edge color, plt.setp(ax.spines.values(), color=axes_settings['edgecolor'])
# matplotlib.rcParams['pdf.fonttype'] = 42
# matplotlib.rcParams['ps.fonttype'] = 42

plt.style.use('default')
font = {'family' : 'DejaVu Sans', 'weight' : 'normal', 'size'   : 14, }
lines = {'linewidth' : 2, 'color' : 'black'}
axes = {'edgecolor' : 'black', 'grid' : True, 'titlesize' : 'medium'}
grid = {'alpha' : 0.1, 'color' : 'black'}
figure = {'titlesize' : 32, 'autolayout' : True, 'figsize' : "4, 12"}

matplotlib.rc('font', **font)
matplotlib.rc('lines', **lines)
matplotlib.rc('axes', **axes)
matplotlib.rc('grid', **grid)
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42



# Your provided data (FP, TP, TN, FN)
# Based on: FT (FP), TT (TP), FF (TN), TF (FN)
llm_performance_data = {
    'gemini-1.0-pro': { # Swapped order to match original plot if it had a specific color order
        'A1': {'FP': 38, 'TP': 91, 'TN': 2,  'FN': 4},
        'A2': {'FP': 19, 'TP': 82, 'TN': 1,  'FN': 3},
        'A3': {'FP': 19, 'TP': 89, 'TN': 58, 'FN': 19},
        'A4': {'FP': 34, 'TP': 85, 'TN': 20, 'FN': 36},
    },
    'gpt-4o': {
        'A1': {'FP': 8,  'TP': 79, 'TN': 32, 'FN': 16},
        'A2': {'FP': 11, 'TP': 79, 'TN': 9,  'FN': 6},
        'A3': {'FP': 19, 'TP': 38, 'TN': 58, 'FN': 70},
        'A4': {'FP': 25, 'TP': 92, 'TN': 29, 'FN': 29},
    },
    'gpt-3.5-turbo': {
        'A1': {'FP': 22, 'TP': 86, 'TN': 18, 'FN': 9},
        'A2': {'FP': 11, 'TP': 62, 'TN': 9,  'FN': 23},
        'A3': {'FP': 21, 'TP': 55, 'TN': 56, 'FN': 53},
        'A4': {'FP': 25, 'TP': 88, 'TN': 29, 'FN': 33},
    }
}

assignments = ['A1', 'A2', 'A3', 'A4']
# Match model order from original script's `models` list if color association is important
models_plot_order = ['gpt-3.5-turbo', 'gpt-4o', 'gemini-1.0-pro']


# Calculate Accuracy, N, and Standard Error of Proportion
accuracies_mean_percent = {model: [] for model in models_plot_order}
accuracies_se_percent = {model: [] for model in models_plot_order}
correct_counts_map = {model: {} for model in models_plot_order}
total_counts_map = {model: {} for model in models_plot_order}

print("--- Individual LLM Performance ---")
for model in models_plot_order: # Use defined plot order
    print(f"\nModel: {model}")
    for assignment in assignments:
        data = llm_performance_data[model][assignment]
        tp = data['TP']
        tn = data['TN']
        fp = data['FP']
        fn = data['FN']

        N = tp + tn + fp + fn
        correct_items = tp + tn
        if N == 0:
            accuracy_p = 0
            se_p = 0
        else:
            accuracy_p = correct_items / N
            se_p = np.sqrt(accuracy_p * (1 - accuracy_p) / N) if N > 0 else 0

        accuracies_mean_percent[model].append(accuracy_p * 100)
        accuracies_se_percent[model].append(se_p * 100)

        correct_counts_map[model][assignment] = correct_items
        total_counts_map[model][assignment] = N
        print(f"  {assignment}: Accuracy = {accuracy_p*100:.2f}% (N={N}, Correct={correct_items}, SE={se_p*100:.2f}%)")


# --- Statistical Tests (Z-test for two proportions) ---
print("\n--- Statistical Comparison (p-values from Z-test) ---")

def perform_z_test_and_print(model1_name, model2_name, assignment_name):
    count1 = correct_counts_map[model1_name][assignment_name]
    nobs1 = total_counts_map[model1_name][assignment_name]

    count2 = correct_counts_map[model2_name][assignment_name]
    nobs2 = total_counts_map[model2_name][assignment_name]

    p_val = 1.0
    if nobs1 > 0 and nobs2 > 0:
        stat, p_val = proportions_ztest(count=[count1, count2], nobs=[nobs1, nobs2], alternative='two-sided')

    print(f"  Comparison: {model1_name} vs {model2_name} on {assignment_name}: p-value = {p_val:.4f}")
    return p_val

for assignment in assignments:
    print(f"\nAssignment: {assignment}")
    for i in range(len(models_plot_order)):
        for j in range(i + 1, len(models_plot_order)):
            model1 = models_plot_order[i]
            model2 = models_plot_order[j]
            perform_z_test_and_print(model1, model2, assignment)


# --- Plotting ---
# Use figsize from original example if desired, or adjust as needed
fig, ax = plt.subplots(figsize=(8, 3)) # Original fig3.pdf was (8,3)
x_indices = np.arange(len(assignments)) # Use np.arange for consistent indexing
num_models = len(models_plot_order)
# Bar width from original example: 0.25
# Total width for a group of bars: num_models * width
# We want bars to be centered around x_indices
# So, first bar starts at x_index - (total_group_width / 2) + (bar_width / 2)
# But the original script used direct offsets from x: [p + width*i for p in x]
# This means x_indices are the start of the first bar in each group.
# Let's replicate that positioning logic.
bar_width = 0.25 # from original script

# Define colors (can be inferred or explicitly set to match the original if known)
# Default color cycle will be used if not specified. Let's use explicit ones for consistency.
# These are common default colors. If your original plot used specific ones, replace them here.
# plot_colors = plt.cm.get_cmap('tab10', num_models).colors # Get distinct colors


for i, model in enumerate(models_plot_order):
    means = accuracies_mean_percent[model]
    ses = accuracies_se_percent[model]

    # Replicating original bar positioning: p + width*i
    # x_indices here represents the 'p' in the original script
    current_bar_positions = [pos + bar_width * i for pos in x_indices]

    bars = ax.bar(current_bar_positions,
                  means,
                  width=bar_width,
                  label=model,
                  yerr=ses,
                  capsize=5, # Standard capsize for error bars
                  edgecolor='black' # Explicitly set edge color
                  )

    # Adding data labels on top of each bar, as in original
    for bar_idx, bar in enumerate(bars):
        yval = bar.get_height()
        # yval + 1 was the original offset. If error bars are present, adjust offset or y position.
        # Place text above the error bar cap
        text_y_position = yval + ses[bar_idx] + 1
        ax.text(bar.get_x() + bar.get_width()/2,
                text_y_position,
                f'{int(round(yval))}%', # Round to nearest int for label
                ha='center',
                va='bottom',
                fontsize=10) # Original was 12, adjust if too crowded with error bars

# Adding labels and title
# ax.set_xlabel('Assignments') # Was commented out
ax.set_ylabel('Grader Accuracy (%)') # Changed from 'Percentage' to be more specific

# X-ticks positioning from original: p + width (assuming p is group center and width is for one bar)
# If x_indices are start of first bar, and we have num_models bars of bar_width:
# Center of group is x_index + (num_models * bar_width) / 2 - bar_width / 2
# Original: ax.set_xticks([p + width for p in x])
# This means the tick is at the center of the SECOND bar if width is bar_width.
# Let's set ticks at the center of each group of bars.
group_centers = [pos + (bar_width * (num_models -1) / 2) for pos in x_indices]
ax.set_xticks(group_centers)
ax.set_xticklabels(assignments)

ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda val, _: f'{int(val)}%'))
ax.set_ylim(0, 100) # Original was (50, 100), adjusted to show full bars and error bars

# Apply original grid style
ax.grid(True, alpha=grid['alpha'], axis='y', linestyle='--')
plt.setp(ax.spines.values())


ax.legend(ncol=num_models, loc='upper center', bbox_to_anchor=(0.5, 1.30)) # Adjusted legend like before

fig.tight_layout(rect=[0, 0.05, 1, 0.9])
#plt.suptitle("LLM Grader Accuracy with Standard Error", fontsize=16) # Or remove if not in original
plt.subplots_adjust(top=0.82) # Adjust top for suptitle and legend
plt.savefig("fig3_replicated_style.pdf")
plt.show()
