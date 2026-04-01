"""Generate charts for bus stop boarding/alighting and cyclist data."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

OUT = "D:/Projects/Bristol/charts"

DARK_BLUE  = "#1a365d"
MID_BLUE   = "#2c5282"
ACCENT     = "#3182ce"
ORANGE     = "#dd6b20"
RED        = "#e53e3e"
GREEN      = "#38a169"
PURPLE     = "#805ad5"
GREY       = "#a0aec0"
LIGHT_GREY = "#e2e8f0"

plt.rcParams.update({
    'font.family': 'sans-serif', 'font.size': 10,
    'axes.facecolor': '#ffffff', 'figure.facecolor': '#ffffff',
    'axes.edgecolor': LIGHT_GREY, 'axes.grid': True,
    'grid.color': LIGHT_GREY, 'grid.linewidth': 0.5,
})

# ═══════════════════════════════════════════════════════════
# CHART: Bus stop passenger volumes (2-day total)
# ═══════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(8, 5))

bus_data = [
    ('5a - Bedminster Pde NB', 5380),
    ('5b - Bedminster Pde SB', 4246),
    ('1a - North St EB', 1090),
    ('3a - North St EB (mid)', 842),
    ('1b - North St WB', 822),
    ('9b - West St SB', 746),
    ('3b - North St WB (mid)', 538),
    ('2b - North St WB (east)', 438),
    ('6a - St John\'s Rd SB', 372),
    ('2a - North St EB (east)', 364),
    ('4b - Duckmoor Rd NB', 230),
    ('4a - Duckmoor Rd SB', 214),
    ('7a - St John\'s Lane EB', 170),
    ('10a - Winterstoke Rd SB', 42),
    ('10b - Winterstoke Rd NB', 40),
    ('8b - Sheene Rd NB', 6),
    ('8a - Sheene Rd SB', 2),
]

labels = [d[0] for d in bus_data]
values = [d[1] for d in bus_data]
colors = []
for l in labels:
    if 'North St' in l:
        colors.append(ACCENT)
    elif 'Bedminster' in l:
        colors.append(ORANGE)
    else:
        colors.append(GREY)

bars = ax.barh(labels, values, color=colors, edgecolor='white', height=0.6)
for bar, val in zip(bars, values):
    if val > 50:
        ax.text(bar.get_width() + 30, bar.get_y() + bar.get_height()/2,
                f'{val:,}', va='center', ha='left', fontsize=8, fontweight='bold',
                color=DARK_BLUE)

ax.set_xlabel('Total Passenger Movements (2 days)', fontsize=10, color=DARK_BLUE)
ax.set_title('Bus Stop Passenger Activity — 11-12 June 2024\n'
             'Bedminster Parade dominates; North Street shows significant bus usage',
             fontsize=11, fontweight='bold', color=DARK_BLUE, pad=12)
ax.invert_yaxis()
ax.set_xlim(0, 6200)

# Legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor=ORANGE, label='Bedminster Parade'),
    Patch(facecolor=ACCENT, label='North Street'),
    Patch(facecolor=GREY, label='Other roads'),
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=8)

plt.tight_layout()
plt.savefig(f'{OUT}/chart_bus_stops.png', dpi=200, bbox_inches='tight')
plt.close()
print("Chart: Bus stop passenger volumes")

# ═══════════════════════════════════════════════════════════
# CHART: North Street bus vs car comparison
# ═══════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(7, 4))

# North Street: ~2,050 bus passengers/day vs 9,688 vehicles/day
categories = ['Vehicles on\nNorth Street\n(ATC Site 11)', 'Bus Passengers\non North Street\n(Sites 1-3)']
values = [9688, 2050]
colors = [ACCENT, ORANGE]

bars = ax.bar(categories, values, color=colors, width=0.5, edgecolor='white', linewidth=2)
for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 150,
            f'{val:,}/day', ha='center', fontsize=12, fontweight='bold', color=DARK_BLUE)

ax.set_ylabel('Daily Count', fontsize=10, color=DARK_BLUE)
ax.set_title('North Street: Vehicle Traffic vs Bus Passenger Activity\n'
             'Significant bus usage indicates a well-served public transport corridor',
             fontsize=11, fontweight='bold', color=DARK_BLUE, pad=12)
ax.set_ylim(0, 12000)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig(f'{OUT}/chart_bus_vs_cars.png', dpi=200, bbox_inches='tight')
plt.close()
print("Chart: Bus vs car comparison on North Street")

# ═══════════════════════════════════════════════════════════
# CHART: Cyclist data - weekday vs weekend pattern
# ═══════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(8, 4))

dates = ['08\nSat', '09\nSun', '10\nMon', '11\nTue', '12\nWed',
         '13\nThu', '14\nFri', '15\nSat', '16\nSun', '17\nMon',
         '18\nTue', '19\nWed', '20\nThu', '21\nFri']
cycles = [489, 560, 355, 350, 385, 255, 188, 140, 475, 320, 380, 389, 340, 220]

# Color weekends differently
bar_colors = []
for d in dates:
    if 'Sat' in d or 'Sun' in d:
        bar_colors.append(ORANGE)
    else:
        bar_colors.append(GREEN)

bars = ax.bar(range(len(dates)), cycles, color=bar_colors, edgecolor='white', width=0.7)
ax.set_xticks(range(len(dates)))
ax.set_xticklabels(dates, fontsize=8)

for i, (bar, val) in enumerate(zip(bars, cycles)):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 8,
            str(val), ha='center', fontsize=7, fontweight='bold', color=DARK_BLUE)

ax.set_ylabel('Total Cyclists (2-way)', fontsize=10, color=DARK_BLUE)
ax.set_xlabel('June 2024', fontsize=10, color=DARK_BLUE)
ax.set_title('Cyclist Volumes on Winterstoke Road (MCC Site 1)\n'
             '14-day count showing weekday/weekend patterns',
             fontsize=11, fontweight='bold', color=DARK_BLUE, pad=12)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Weekday/weekend averages
weekday_avg = np.mean([c for c, d in zip(cycles, dates) if 'Sat' not in d and 'Sun' not in d])
weekend_avg = np.mean([c for c, d in zip(cycles, dates) if 'Sat' in d or 'Sun' in d])
ax.axhline(weekday_avg, color=GREEN, linestyle='--', alpha=0.5, linewidth=1.5)
ax.axhline(weekend_avg, color=ORANGE, linestyle='--', alpha=0.5, linewidth=1.5)
ax.text(13.5, weekday_avg + 10, f'Weekday avg: {weekday_avg:.0f}', fontsize=8,
        color=GREEN, ha='right', fontweight='bold')
ax.text(13.5, weekend_avg + 10, f'Weekend avg: {weekend_avg:.0f}', fontsize=8,
        color=ORANGE, ha='right', fontweight='bold')

from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor=GREEN, label='Weekday'),
    Patch(facecolor=ORANGE, label='Weekend'),
]
ax.legend(handles=legend_elements, loc='upper right', fontsize=8)

plt.tight_layout()
plt.savefig(f'{OUT}/chart_cyclists.png', dpi=200, bbox_inches='tight')
plt.close()
print("Chart: Cyclist volumes on Winterstoke Road")

print("\nAll additional charts generated.")
