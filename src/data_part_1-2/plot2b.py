import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.font_manager import FontProperties
from matplotlib.legend import Legend
from matplotlib.ticker import ScalarFormatter
from matplotlib import ticker

lines = []
x = [1,2,4,8]
y = [1,2,4,8]
# Read the CSV data
df = pd.read_csv('part2b/data.csv')

# Set dimension
fig, ax = plt.subplots(figsize=(9, 6))

plt.rc('font', family='sans serif', size=12)
font = FontProperties()
font.set_family('sans serif')

# Set Title
title = ax.set_title('Parallel Behaviour', fontproperties=font, fontsize=16, fontweight='bold', pad=30)
title.set_position((0.145, 1))


# Create the line plot
lines += ax.plot(df['x'], df['radix'], color='#A9A9A9', linewidth=2, marker="o", markersize=8, label='Radix', markeredgecolor='white')
lines += ax.plot(df['x'], df['freqmine'], color='#87CEEB', linewidth=2, marker="o", markersize=8, label='Freqmine', markeredgecolor='white')
lines += ax.plot(df['x'], df['vips'], color='#000000', linewidth=2, marker="o", markersize=8, label='Vips', markeredgecolor='white')
lines += ax.plot(df['x'], df['ferret'], color='#006400', linewidth=2, marker="o", markersize=8, label='Ferret', markeredgecolor='white')
lines += ax.plot(df['x'], df['blackscholes'], color='#FF8C00', linewidth=2, marker="o", markersize=8, label='Blackscholes', markeredgecolor='white')
lines += ax.plot(df['x'], df['canneal'], color='#FF1493', linewidth=2, marker="o", markersize=8, label='Canneal', markeredgecolor='white')
lines += ax.plot(df['x'], df['dedup'], color='#8B0000', linewidth=2, marker="o", markersize=8, label='Dedup', markeredgecolor='white')
ax.plot(x, y, linestyle='--')


# Set x axis label, limits and ticks
ax.set_xlabel('Threads', fontname='sans serif', fontsize=14, labelpad=4)
ax.set_xlim(0, 8.4)  # y limits from 0 to 1
ax.set_xticks([0, 1, 2, 3, 4, 5, 6,7,8])


# Set y axis label, limits and ticks
ax.set_ylabel('[Speedup]', fontname='sans serif', fontsize=14, rotation='horizontal')
ax.set_ylim(0, 8.2)  # y limits from 0 to 1
ax.yaxis.grid(True, linewidth=2, c="white")
ax.yaxis.set_label_coords(0.04, 1.03)
ax.set_yticks([0, 1, 2, 3, 4, 5, 6,7,8])

# Tick and border settings
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_linewidth(2)
ax.tick_params(axis='y', length=0, pad=10, labelsize=14)
ax.tick_params(axis='x', pad=6, width=2, length=5, labelsize=14)

#LEGEND
box0 = ax.get_position()
ax.set_position([box0.x0, box0.y0, box0.width * 0.88, box0.height])
ax.legend(lines[6:7], ['Dedup'], loc='center left', bbox_to_anchor=(1, 0.322*3/4*40/41), frameon=False)
leg = Legend(ax, lines[0:1], ['Radix'],
             loc='center left', bbox_to_anchor=(1, 0.925*3/4*40/41), frameon=False)
ax.add_artist(leg)
leg = Legend(ax, lines[1:2], ['Freqmine'],
             loc='center left', bbox_to_anchor=(1, 0.805*3/4*40/41), frameon=False)
ax.add_artist(leg)
leg = Legend(ax, lines[2:3], ['Vips'],
             loc='center left', bbox_to_anchor=(1, 0.74*3/4*40/41), frameon=False)
ax.add_artist(leg)
leg = Legend(ax, lines[3:4], ['Ferret'],
             loc='center left', bbox_to_anchor=(1, 0.645*3/4*40/41), frameon=False)
ax.add_artist(leg)
leg = Legend(ax, lines[4:5], ['Blackscholes'],
             loc='center left', bbox_to_anchor=(1, 0.575*3/4*40/41), frameon=False)
ax.add_artist(leg)
leg = Legend(ax, lines[5:6], ['Canneal'],
             loc='center left', bbox_to_anchor=(1, 0.41*3/4*40/41), frameon=False)
ax.add_artist(leg)

# Set the background color to blue
ax.set_facecolor('#e5e5e5')

# Show the plot
plt.show()
fig.savefig('./Plot_Images/plot2b.pdf', format='svg')
