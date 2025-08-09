import matplotlib.pyplot as plt
import numpy as np
import matplotlib

plt.style.use('default')
font = {'family' : 'DejaVu Sans', 'weight' : 'normal', 'size'   : 14, }
lines = {'linewidth' : 2, 'color' : 'black'}
axes = {'hold' : True, 'edgecolor' : 'black', 'grid' : True, 'titlesize' : 'medium'}
grid = {'alpha' : 0.1, 'color' : 'black'}
figure = {'titlesize' : 32, 'autolayout' : True, 'figsize' : "4, 12"}

matplotlib.rc('font', **font)
matplotlib.rc('lines', **lines)
#matplotlib.rc('axes', **axes)
matplotlib.rc('grid', **grid)
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42


# Data
models = ['playground (gpt-3.5-turbo)', 'grader (gpt-3.5-turbo)', 'grader (gpt-4o)', 'grader (gemini-1.0-pro)']
answers = ['A1', 'A2', 'A3', 'A4']

playground_costs = {
    'playground (gpt-3.5-turbo)': [0.754, 2.247, 0.633, 1.469],
    'grader (gpt-3.5-turbo)': [2.071, 4.106, 0.633, 0.757],
    'grader (gpt-4o)': [49.85, 89.21, 18.98, 11.86],
    'grader (gemini-1.0-pro)': [2.2621515, 5.0862155, 0.777128, 0.8507885]
}

# Plotting
x = np.arange(len(answers))  # the label locations
width = 0.2  # the width of the bars

# Plotting with data labels
fig, ax = plt.subplots(figsize=(8, 3))

for i, (model, costs) in enumerate(playground_costs.items()):
    bars = ax.bar(x + i * width, costs, width, label=model, edgecolor='black')
    # Add data labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=10)

# Add some text for labels, title and custom x-axis tick labels, etc.
#ax.set_xlabel('Answers')
ax.set_ylabel('Cost (USD)')
#ax.set_title('Playground Costs by Model and Answer')
ax.set_xticks(x + width * 1.5)
ax.set_xticklabels(answers)
ax.legend(fontsize=10, ncol=2, loc='upper right')
ax.set_ylim([0.1, 2000])
ax.set_yscale('log')


fig.tight_layout()
# Save the figure as a PDF file
fig.savefig("fig2.pdf")
plt.show()


