import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load data
df_c = pd.read_csv('Cheese_Report_2016.csv')
df_h = pd.read_csv('World_Happiness_Report_2016.csv')

# Find matching countries
labels = []
for hountry in df_h['Country'][:15]:
    for country in df_c['Country'][:15]:
        if country == hountry:
            labels.append(country)

num_vars = len(labels)
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]  # Close the plot


## Convert cheese exports into logarithmically scaled value.

# Convert all values to millions
def convert_cheese(value):
    value = str(value).strip()
    if 'bn' in value:
        value = float(value.replace('bn', '')) * 1000
    elif 'm' in value:
        value = float(value.replace('m', ''))
    else:
        value = float(value) / 1e6

    # Convert values onto a logarithmic scale
    log_min = np.log10(31.25)
    log_max = np.log10(4000)
    log_val = np.log10(value)
    scaled_val = ((log_val - log_min) / (log_max - log_min)) * 8
    return scaled_val


## Prepare data

data_c = [convert_cheese(df_c[df_c['Country'] == eee]['Export value US$'].values[0]) 
          for eee in labels]

data_h = [df_h[df_h['Country'] == eee]['Happiness Score'].values[0] 
          for eee in labels]

# Make sure the ending vlaue loops back to the starting value
# (Close the plot)
data_c += data_c[:1]
data_h += data_h[:1]


## Create plot

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

# Plot Cheese Exports (log scale)
ax.plot(angles, data_c, label='Cheese Exports (USD)', color='blue', linewidth=3)
ax.fill(angles, data_c, alpha=0.25, color='blue')

# Plot Happiness Score
ax.plot(angles, data_h, label='Happiness Score (0-8)', color='red', linewidth=3)
ax.fill(angles, data_h, alpha=0.25, color='red')


## Formatting and labels

ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)
ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels, fontsize=10)

# Custom y-axis labels
ax.set_yticks([0, 2, 4, 6, 8])

# Left side labels for Cheese (blue)
ax.set_yticklabels(['', '63 million', '250 million', '1 billion', '4 billion'], fontsize=15, color='black')

# Right side labels for Happiness (red)
for tick, label in zip(ax.get_yticks(), ['', '2', '4', '6', '8']):
    ax.text(np.pi/2, tick, label, color='black', fontsize=13, 
            ha='left', va='center')

ax.set_ylim(0, 8)
ax.set_rlabel_position(30)

# Add legend
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

# Set title
ax.set_title('Cheese Exports vs Happiness Scores', y=1.15, fontsize=14)

plt.tight_layout()
plt.show()