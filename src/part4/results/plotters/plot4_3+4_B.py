import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.font_manager import FontProperties
import math

number = 1
dir_num = 4

# Read the CSV data
df_0 = pd.read_csv('../part'+ str(dir_num)+'/' + str(number) + '/jobs_time.csv')
df_1 = pd.read_csv('../part'+ str(dir_num)+'/' + str(number) + '/memcache_cores.csv')
df_2 = pd.read_csv('../part'+ str(dir_num)+'/' + str(number) + '/p95.csv')

colors = ["#CCA000",
          "#CCCCAA",
          "#CCACCA",
          "#AACCCA",
          "#0CCA00",
          "#00CCA0",
          "#CC0A00"]

labels = ["blackscholes",
         "canneal",
                "dedup",
                "ferret",
                "freqmine",
                "radix",
                "vips"]

# Set dimension
fig, ax = plt.subplots(figsize=(14, 9))

plt.rc('font', family='sans serif', size=12)
font = FontProperties()
font.set_family('sans serif')

# Set Title
title = ax.set_title(str(number) + 'B', fontproperties=font, fontsize=16, fontweight='bold', pad=12, ha='center')
title.set_position((0.5, 1))

ax2 = ax.twinx()
ax2.zorder = 4
ax.zorder = 6
ax2.set_ylabel('[QPS]', fontname='sans serif', fontsize=14, rotation='horizontal')
ax2.yaxis.set_label_coords(1.035, 0.555)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax2.spines['bottom'].set_linewidth(2)
ax2.tick_params(axis='y', length=0, pad=10, labelsize=14)
ax2.tick_params(axis='x', pad=6, width=2, length=5, labelsize=14)
ax2.set_ylim(0, 200000)
ticks_label = []
ticks = list(range(0, 100001, 10000))
ax2.set_yticks(ticks)
for tick in ticks:
    ticks_label.append(str(int(tick/1000)) + "K")
ax2.set_yticklabels(ticks_label)
# Create the line plot
# ax.plot(df_1['x'], df_1['Core_1_Thread_2'], color='#FF1493', linewidth=1.5, label='1 Core 2 Threads', zorder=12, clip_on=False)
ax2.plot(df_2['time'], df_2['qps'], color='orange', linewidth=1.5, marker="o", markersize=8, label='QPS',
        markeredgecolor='white', zorder=8, clip_on=False, alpha = 0.5)
ax.plot(df_1['time'], df_1['core'], color='blue', linewidth=1, label='Memcached Cores',
        markeredgecolor='white', zorder=20, clip_on=False)

# ax.axhline(y=0.5, color='#b5b5b5', linestyle='-', linewidth=1, zorder=5)
# ax.axhline(y=1.5, color='#b5b5b5', linestyle='-', linewidth=1, zorder=5)
# ax.axhline(y=2, color='#b5b5b5', linestyle='-', linewidth=1, zorder=5)

for i in range(1, 11):
        ax2.axhline(y=i*10000, color='#b5b5b5', linestyle='-', linewidth=1, zorder=5)

start = []
for label in labels:
     start.append(df_0[label].values[0])
for i in range (7):
    ax.axhline(y=7.2 - i / 2.5, color='black', linestyle='-', linewidth=0.5, zorder=1)

index = 0
last = 0
for label in labels:
        last = 0
        for i in range(0, len(df_0[label].values), 2):
                if df_0[label].values[i] >= 0:
                        last = i+1
                        ax.hlines(xmin=df_0[label].values[i] - 0.15, xmax=df_0[label].values[i+1] + 0.15, y=7.2 - index / 2.5, color=colors[index], linewidth=15, zorder=10)
        ax.plot([df_0[label].values[0], df_0[label].values[0]], [0, 7.2 - index / 2.5], color=colors[index], linewidth=1.5, linestyle='--', zorder=6, clip_on=False)
        ax.plot([df_0[label].values[last], df_0[label].values[last]], [0, 7.2 - index / 2.5], color=colors[index], linewidth=1.5, linestyle='--', zorder=6)
        index += 1


# Set x axis label, limits and ticks
ax.set_xlabel('Time [s]', fontname='sans serif', fontsize=14, labelpad=4)
ax.set_xlim(0, df_2['time'].max() + 1)  # y limits from 0 to 1
ticks = list(range(0, int(df_2['time'].max()) + 1, 30))
ax.set_xticks(ticks)

# Set y axis label, limits and ticks
ax.set_ylabel('[N° Cores]', fontname='sans serif', fontsize=14, rotation='horizontal')
ax.set_ylim(0, 8)  # y limits from 0 to 1
ticks = [0,1,2,3,4,4.8,5.2,5.6,6,6.4,6.8,7.2]
ticks_label = ["0", "1", "2", "3", "4", "vips", "radix", "freqmine", "ferret", "dedup", "canneal", "blackscholes"]
ax.set_yticks(ticks)
ax.set_yticklabels(ticks_label)
ax.yaxis.set_label_coords(-0.056, 0.525)

# Tick and border settings
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_linewidth(2)
ax.tick_params(axis='y', length=0, pad=10, labelsize=14)
ax.tick_params(axis='x', pad=6, width=2, length=5, labelsize=12)

#LEGEND
#box0 = ax.get_position()
#ax.set_position([box0.x0, box0.y0, box0.width * 0.94, box0.height])
ax2.legend(loc='upper right', bbox_to_anchor=(0.8, 1), facecolor='white')
ax.legend(loc='upper right', bbox_to_anchor=(1, 1), facecolor='white')


# Set the background color to grey
ax2.set_facecolor('#f7f7f7')
ax2.patch.set_visible(True)
ax.patch.set_visible(False)
fig.subplots_adjust(left=0.12, right=0.95, top=0.93, bottom=0.07)

# Show the plot
plt.show()
fig.savefig('../Plot_images/plot'+ str(dir_num)+'_'+str(number) +'B.svg', format='svg')

