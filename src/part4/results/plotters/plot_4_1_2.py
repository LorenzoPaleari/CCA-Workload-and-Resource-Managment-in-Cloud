import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.font_manager import FontProperties

# Read the CSV data
df_0 = pd.read_csv('../part1/Question_4/data_0.csv')
df_1 = pd.read_csv('../part1/Question_4/data_1.csv')
df_2 = pd.read_csv('../part1/Question_4/cpu_data_1.csv')
df_3 = pd.read_csv('../part1/Question_4/cpu_data_2.csv')


# Set dimension
fig, ax = plt.subplots(figsize=(14, 9))

plt.rc('font', family='sans serif', size=12)
font = FontProperties()
font.set_family('sans serif')

# Set Title
title = ax.set_title('2 Thread 1 Core', fontproperties=font, fontsize=16, fontweight='bold', pad=12, ha='center')
title.set_position((0.5, 1))


# Create the line plot
ax.plot(df_0['x'], df_0['Core_1_Thread_2'], color='orange', linewidth=1.5, marker="o", markersize=8, label='95th Latency',
       markeredgecolor='white', zorder=20, clip_on=False)
#ax.plot(df_1['x'], df_1['Core_2_Thread_2'], color='orange', linewidth=1.5, marker="o", markersize=8, label='95th Latency',
#        markeredgecolor='white', zorder=12, clip_on=False)

# Error bars

ax.axhline(y=1, color='red', linestyle='dotted', linewidth=2, zorder=6)

ax2 = ax.twinx()
ax2.plot(df_2['x'], df_2['cpu'], color='blue', linewidth=1.5, label='Cpu utilization', zorder=18, clip_on=False)
#ax2.plot(df_3['x'], df_3['cpu'], color='blue', linewidth=1.5, label='Cpu utilization', zorder=10, clip_on=False)
ax2.set_ylabel('[Cpu Usage]', fontname='sans serif', fontsize=14, rotation='horizontal')
ax2.yaxis.set_label_coords(1.06, 1.04)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax2.spines['bottom'].set_linewidth(2)
ax2.tick_params(axis='y', length=0, pad=10, labelsize=14)
ax2.tick_params(axis='x', pad=6, width=2, length=5, labelsize=14)
ax2.set_ylim(0, 101)
ax2.set_xticks([0,20,40,60,80,100,120,140,160,180,200])


# Set x axis label, limits and ticks
ax.set_xlabel('QPS', fontname='sans serif', fontsize=14, labelpad=4)
ax.set_xlim(0, 130000)  # y limits from 0 to 1
ticks = list(range(0, 130001, 10000))
ax.set_xticks(ticks)
ticks_label = []
for tick in ticks:
    ticks_label.append(str(int(tick/1000)) + "K")
ax.set_xticklabels(ticks_label)


# Set y axis label, limits and ticks
ax.set_ylabel('[ms]', fontname='sans serif', fontsize=14, rotation='horizontal')
ax.set_ylim(0, 2)  # y limits from 0 to 1
ax.yaxis.set_label_coords(-0.029, 1.02)

# Tick and border settings
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_linewidth(2)
ax.tick_params(axis='y', length=0, pad=10, labelsize=14)
ax.tick_params(axis='x', pad=6, width=2, length=5, labelsize=14)

#LEGEND
#box0 = ax.get_position()
#ax.set_position([box0.x0, box0.y0, box0.width * 0.94, box0.height])
ax.legend(loc='lower right', bbox_to_anchor=(1, 0.05), facecolor='white')
ax2.legend(loc='lower right', bbox_to_anchor=(1, 0), facecolor='white')


# Set the background color to grey
ax.set_facecolor('#e5e5e5')
fig.subplots_adjust(left=0.05, right=0.9, top=0.93, bottom=0.07)

# Show the plot
plt.show()
fig.savefig('../Plot_images/plot1_1_1.svg', format='svg')

