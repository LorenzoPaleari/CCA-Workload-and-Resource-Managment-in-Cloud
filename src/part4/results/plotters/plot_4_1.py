import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.font_manager import FontProperties

# Read the CSV data
df_0 = pd.read_csv('../part1/data_0.csv')
df_1 = pd.read_csv('../part1/data_1.csv')
df_2 = pd.read_csv('../part1/data_2.csv')
df_3 = pd.read_csv('../part1/data_3.csv')

# Set dimension
fig, ax = plt.subplots(figsize=(14, 9))

plt.rc('font', family='sans serif', size=12)
font = FontProperties()
font.set_family('sans serif')

# Set Title
title = ax.set_title('Memcached 95th Percentile Latency', fontproperties=font, fontsize=16, fontweight='bold', pad=12, ha='center')
title.set_position((0.5, 1))


# Create the line plot
ax.plot(df_0['x'], df_0['Core_1_Thread_1'], color='#000000', linewidth=1.5, marker="o", markersize=8, label='1 Core 1 Thread',
        markeredgecolor='white', zorder=20, clip_on=False)
ax.plot(df_1['x'], df_1['Core_1_Thread_2'], color='#FF1493', linewidth=1.5, marker="o", markersize=8, label='1 Core 2 Threads',
        markeredgecolor='white', zorder=12, clip_on=False)
ax.plot(df_2['x'], df_2['Core_2_Thread_1'], color='#87CEEB', linewidth=1.5, marker="o", markersize=8, label='2 Cores 1 Thread',
        markeredgecolor='white', zorder=18, clip_on=False)
ax.plot(df_3['x'], df_3['Core_2_Thread_2'], color='#FF8C00', linewidth=1.5, marker="o", markersize=8, label='2 Cores 2 Threads',
        markeredgecolor='white', zorder=10, clip_on=False)

# Error bars
ax.errorbar(df_1['x'], df_1['Core_1_Thread_2'], yerr=(df_1['y_err_lo'], df_1['y_err_hi']), xerr=df_1['x_err'], fmt='-', capsize=4, color='#FF1493', zorder=11)
ax.errorbar(df_3['x'], df_3['Core_2_Thread_2'], yerr=df_3['y_err_lo'], xerr=df_3['y_err_hi'], fmt='-', capsize=4, color='#FF8C00',zorder=9)
ax.errorbar(df_0['x'], df_0['Core_1_Thread_1'], yerr=df_0['y_err_lo'], xerr=df_0['y_err_hi'], fmt='-', capsize=4, color='#000000',zorder=19)
ax.errorbar(df_2['x'], df_2['Core_2_Thread_1'], yerr=df_2['y_err_lo'], xerr=df_2['y_err_hi'], fmt='-', capsize=4, color='#87CEEB',zorder=17)

ax.axhline(y=1, color='red', linestyle='-', linewidth=2, zorder=6)
ax.axhline(y=1, color='#e5e5e5', linestyle='-', linewidth=2, zorder=5)


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
ax.yaxis.grid(True, linewidth=2, c="white")
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
ax.legend(loc='upper right', bbox_to_anchor=(1, 1), facecolor='white')


# Set the background color to grey
ax.set_facecolor('#e5e5e5')
fig.subplots_adjust(left=0.05, right=0.98, top=0.93, bottom=0.07)

# Show the plot
plt.show()
fig.savefig('../Plot_images/plot3_1.svg', format='svg')

