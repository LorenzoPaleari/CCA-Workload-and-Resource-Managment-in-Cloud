import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.font_manager import FontProperties
import matplotlib.patheffects as pe
import math

df_0 = pd.read_csv('Runs/2/Job_run_1.csv')
df = pd.read_csv('Runs/2/memcached_run_1.csv')

colors = ["#CCCCAA",
          "#CCACCA",
          "#CC0A00",
          "#CCA000",
          "#AACCCA",
          "#0CCA00",
          "#00CCA0",]

machine = ["Node-a",
           "Node-a",
           "Node-a",
              "Node-b",
              "Node-b",
              "Node-c",
            "Node-c"]

df['Width'] = df['End'] - df['Start']

fig, ax = plt.subplots(figsize=(14, 9))

plt.rc('font', family='sans serif', size=12)
font = FontProperties()
font.set_family('sans serif')

title = ax.set_title('Run 2', fontproperties=font, fontsize=16, fontweight='bold', pad=12)
title.set_position((0.485, 0.90))

ax.bar(df['Start'], df['p95']/1000.0, width=df['Width'], align='edge', color='#D16437', zorder=5)

label = []
start = []
end = []
for index in range(7):
    start.append(df_0['Start'][index])
    end.append(df_0['End'][index])
    label.append(df_0['Job'][index])
    #ax.plot(start, 1.9 - index / 10, marker='o', markersize=9, color=colors[index], zorder=10, clip_on=False, markeredgecolor='black')
    #ax.plot(end, 1.9 - index / 10, marker='X', markersize=9, color=colors[index], zorder=11, clip_on=False, markeredgecolor='black')
    ax.hlines(xmin=start[index] - 0.15, xmax=end[index] + 0.15, y=1.9 - index / 10, color=colors[index], linewidth=15, zorder=10)
    ax.plot([start[index], start[index]], [0, 1.9 - index / 10], color=colors[index], linewidth=2, linestyle='--', zorder=10)
    ax.plot([end[index], end[index]], [0, 1.9 - index / 10], color=colors[index], linewidth=2, linestyle='--', zorder=10)

ax.set_ylabel('[ms]', fontname='sans serif', fontsize=16, rotation='horizontal')
ax.set_ylim(0, 2)  # y limits from 0 to 1
ax.axhline(y=0.75, color='black', linestyle='-', clip_on=False, linewidth=0.5, zorder=1)
ax.axhline(y=0.25, color='black', linestyle='-', linewidth=0.5, zorder=1)
ax.axhline(y=0.5, color='black', linestyle='-', clip_on=False, linewidth=0.5, zorder=1)
for i in range (7):
    ax.axhline(y=1.9 - i / 10, color='black', linestyle='-', linewidth=0.5, zorder=1)
    plt.text(math.ceil(start[i]) + 0.5 , 1.9 - i /10 - 0.005, label[i], color='white', fontsize=13, ha='left', va='center', zorder=11, fontweight='bold')


ticks = list(range(0, 170, 5))
ax.set_xticks(ticks)

# Add a red line at 1
ax.axhline(y=1, color='red', linestyle='-')
ax.yaxis.set_label_coords(-0.03, 0.53)
ax.set_xlim(0, 162.3)
ticks = [0.00, 0.25, 0.50, 0.75, 1.00, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9]
ax.set_yticks(ticks)

ax.set_yticklabels([f'{tick:.2f}' if tick >= 0 and tick <= 1 else "" if tick >= 1 and tick < 2 else int(tick) for tick in ax.get_yticks()])
ax.annotate('node-a-2core', xy=(-1, 1.8), xytext=(-12, 1.8), xycoords='data', annotation_clip=False, 
            fontsize=14, ha='center', va='center',
            arrowprops=dict(arrowstyle='-[, widthB=2, lengthB=0.5, angleB=0', lw=0.5, color='k'))
ax.annotate('node-b-4core', xy=(-1, 1.5525), xytext=(-12, 1.5525), xycoords='data', annotation_clip=False, 
            fontsize=14, ha='center', va='center',
            arrowprops=dict(arrowstyle='-[, widthB=1, lengthB=0.5, angleB=0', lw=0.5, color='k'))
ax.annotate('node-c-8core', xy=(-1, 1.35), xytext=(-12, 1.35), xycoords='data', annotation_clip=False, 
            fontsize=14, ha='center', va='center',
            arrowprops=dict(arrowstyle='-[, widthB=1, lengthB=0.5, angleB=0', lw=0.5, color='k'))

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_linewidth(2)
ax.tick_params(axis='y', length=0, pad=10, labelsize=14)
ax.tick_params(axis='x', pad=6, width=2, length=5, labelsize=11)

ax.set_facecolor('#f3f3f3')


ax2 = ax.twinx()
ax2.set_ylabel('[Node name]', fontname='sans serif', fontsize=14, rotation='horizontal')
ax2.yaxis.set_label_coords(-0.07, 1.005)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax2.spines['bottom'].set_linewidth(2)
ax2.tick_params(axis='y', length=0, pad=10, labelsize=14)
ax2.tick_params(axis='x', pad=6, width=2, length=5, labelsize=14)
ax2.set_yticklabels(["" for tick in ax.get_yticks()])


fig.subplots_adjust(left=0.12, right=0.98, top=0.92, bottom=0.07)

# Show the plot
plt.show()
fig.savefig('./Plot_Images/plot3_run_2.svg', format='svg')
