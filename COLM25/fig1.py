import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import matplotlib.ticker as mtick
plt.style.use('default')
font = {'family' : 'DejaVu Sans', 'weight' : 'normal', 'size'   : 14, }
lines = {'linewidth' : 2, 'color' : 'black'}
axes = {'edgecolor' : 'black', 'grid' : True, 'titlesize' : 'medium'}
grid = {'alpha' : 0.1, 'color' : 'black'}
figure = {'titlesize' : 32, 'autolayout' : True, 'figsize' : "4, 12"}
matplotlib.rc('font', **font)
matplotlib.rc('lines', **lines)
matplotlib.rc('axes', **axes) # Use the new dict name
matplotlib.rc('grid', **grid)  # Use the new dict name
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
# Updated categories - removed 'Evaluation'
categories = ['Assignments', 'Projects', 'Exams']
# Use the provided means and standard deviations - removed last element
means_before = [82.85215520675105, 78.3773494413502, 71.30934479473683]
sds_before = [14.573274435585818, 17.756692449218235, 17.895182787400838]
means_after = [86.35056446666667, 85.403125, 72.54760871224491]
sds_after = [10.204025835675843, 24.155505575425874, 18.957714727076105]
p_values_for_stars = [0.027654510800612268, 0.018444220194880675, 0.6926134042781723]
x = np.arange(len(categories))  # the label locations
width = 0.35  # the width of the bars
fig, ax = plt.subplots()
fig.set_size_inches(6,3.2) # Set figure size
# Add yerr for standard deviation and capsize for the error bar caps
rects1 = ax.bar(x - width/2, means_before, width, label='Before', yerr=sds_before, capsize=5, edgecolor='black', ecolor='black')
rects2 = ax.bar(x + width/2, means_after, width, label='After', yerr=sds_after, capsize=5, edgecolor='black', ecolor='black')
# Adjusting labels and titles
# ax.set_xlabel('Categories') # Uncomment if you want an x-axis label
ax.set_ylabel('Percentage')
# ax.set_title('Merged and Normalized Scores by Category and Time') # Uncomment for a title
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(ncol=2, loc="upper right", bbox_to_anchor=(0.80, 1.30))
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
ax.set_ylim(0, 125) # Adjusted to give space for error bars if they go high
# Updated function to show percentage on top of error bars
def autolabel(rects, means, sds):
    for i, rect in enumerate(rects):
        mean_value = means[i]
        sd_value = sds[i]
        # Position the label at the top of the error bar (mean + standard deviation)
        label_height = mean_value + sd_value
        # Display the mean value on top of the error bar
        ax.annotate(f'{mean_value:.1f}%',
                    xy=(rect.get_x() + rect.get_width() / 2, label_height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=10) # Smaller font for clarity
autolabel(rects1, means_before, sds_before)
autolabel(rects2, means_after, sds_after)
# Add p-values below category labels
for i, p_value in enumerate(p_values_for_stars):
    ax.text(x[i], -22, f'(p = {p_value:.3f})',
            ha='center', va='top', fontsize=12,
            color='black')
fig.tight_layout()
# Save the figure as a PDF file
fig.savefig("fig1_with_sd.pdf") # Changed filename to reflect update
plt.show()