import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.font_manager import FontProperties

# Read the CSV data
df_0 = pd.read_csv('part_1/data_0.csv')
df_1 = pd.read_csv('part_1/data_1.csv')
df_2 = pd.read_csv('part_1/data_2.csv')
df_3 = pd.read_csv('part_1/data_3.csv')
df_4 = pd.read_csv('part_1/data_4.csv')
df_5 = pd.read_csv('part_1/data_5.csv')
df_6 = pd.read_csv('part_1/data_6.csv')

# Set dimension
fig, ax = plt.subplots(figsize=(14, 9))

plt.rc('font', family='sans serif', size=12)
font = FontProperties()
font.set_family('sans serif')

# Set Title
title = ax.set_title('Memcached 95th Percentile Latency', fontproperties=font, fontsize=16, fontweight='bold', pad=32)
title.set_position((0.1485, 1))


# Create the line plot
ax.plot(df_0['x'], df_0['clean'], color='#000000', linewidth=1.5, marker="o", markersize=8, label='no_interference',
        markeredgecolor='white', zorder=20, clip_on=False)
ax.plot(df_1['x'], df_1['cpu'], color='#FF1493', linewidth=1.5, marker="o", markersize=8, label='cpu',
        markeredgecolor='white', zorder=4, clip_on=False)
ax.plot(df_2['x'], df_2['l1d'], color='#A9A9A9', linewidth=1.5, marker="o", markersize=8, label='l1d',
        markeredgecolor='white', zorder=18, clip_on=False)
ax.plot(df_3['x'], df_3['l1i'], color='#006400', linewidth=1.5, marker="o", markersize=8, label='l1i',
        markeredgecolor='white', zorder=3, clip_on=False)
ax.plot(df_4['x'], df_4['l2'], color='#FF8C00', linewidth=1.5, marker="o", markersize=8, label='l2',
        markeredgecolor='white', zorder=16, clip_on=False)
ax.plot(df_5['x'], df_5['llc'], color='#87CEEB', linewidth=1.5, marker="o", markersize=8, label='llc',
        markeredgecolor='white', zorder=14, clip_on=False)
ax.plot(df_6['x'], df_6['membw'], color='#8B0000', linewidth=1.5, marker="o", markersize=8, label='memBw',
        markeredgecolor='white', zorder=12, clip_on=False)

# Error bars
ax.errorbar(df_1['x'], df_1['cpu'], yerr=(df_1['y_err_lo'], df_1['y_err_hi']), xerr=df_1['x_err'], fmt='-', capsize=4, color='#FF1493', zorder=3)
ax.errorbar(df_3['x'], df_3['l1i'], yerr=df_3['y_err_lo'], xerr=df_3['y_err_hi'], fmt='-', capsize=4, color='#006400',zorder=2)
ax.errorbar(df_0['x'], df_0['clean'], yerr=df_0['y_err_lo'], xerr=df_0['y_err_hi'], fmt='-', capsize=4, color='#000000',zorder=19)
ax.errorbar(df_2['x'], df_2['l1d'], yerr=df_2['y_err_lo'], xerr=df_2['y_err_hi'], fmt='-', capsize=4, color='#A9A9A9',zorder=17)
ax.errorbar(df_4['x'], df_4['l2'], yerr=df_4['y_err_lo'], xerr=df_4['y_err_hi'], fmt='-', capsize=4, color='#FF8C00',zorder=15)
ax.errorbar(df_5['x'], df_5['llc'], yerr=df_5['y_err_lo'], xerr=df_5['y_err_hi'], fmt='-', capsize=4, color='#87CEEB',zorder=13)
ax.errorbar(df_6['x'], df_6['membw'], yerr=df_6['y_err_lo'], xerr=df_6['y_err_hi'], fmt='-', capsize=4, color='#8B0000',zorder=11)

# Set x axis label, limits and ticks
ax.set_xlabel('QPS', fontname='sans serif', fontsize=14, labelpad=4)
ax.set_xlim(0, 110000)  # y limits from 0 to 1
ticks = list(range(0, 110001, 10000))
ax.set_xticks(ticks)
ticks_label = []
for tick in ticks:
    ticks_label.append(str(int(tick/1000)) + "K")
ax.set_xticklabels(ticks_label)


# Set y axis label, limits and ticks
ax.set_ylabel('[ms]', fontname='sans serif', fontsize=14, rotation='horizontal')
ax.set_ylim(0, 8)  # y limits from 0 to 1
ax.yaxis.grid(True, linewidth=2, c="white")
ax.yaxis.set_label_coords(-0.005, 1.025)

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
fig.subplots_adjust(left=0.02, right=0.98, top=0.93, bottom=0.07)

# Show the plot
plt.show()
fig.savefig('./Plot_Images/plot1_total.svg', format='svg')

