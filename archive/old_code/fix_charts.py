"""Fix charts with overlapping text."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

OUT = "D:/Projects/Bristol/charts"

DARK_BLUE  = "#1a365d"
MID_BLUE   = "#2c5282"
ACCENT     = "#3182ce"
LIGHT_BLUE = "#90cdf4"
ORANGE     = "#dd6b20"
RED        = "#e53e3e"
GREEN      = "#38a169"
GREY       = "#a0aec0"
LIGHT_GREY = "#e2e8f0"

plt.rcParams.update({
    'font.family': 'sans-serif', 'font.size': 10,
    'axes.facecolor': '#ffffff', 'figure.facecolor': '#ffffff',
    'axes.edgecolor': LIGHT_GREY, 'axes.grid': True,
    'grid.color': LIGHT_GREY, 'grid.linewidth': 0.5,
})

# ═══════════════════════════════════════════════════════════
# CHART 2 FIX: Cross-Zone Detections in Context
# ═══════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(7.5, 4.0))

categories = [
    'Cam 14\u2194 16\ncross-zone\n(11 June)',
    'Cam 14\u2194 16\ncross-zone\n(12 June)',
    'Camera 16\ntotal traffic',
    'Camera 14\ntotal traffic',
    'Total ANPR\nmatched\nmovements'
]
values = [11, 10, 7642, 15092, 67031]
colors2 = [RED, RED, LIGHT_BLUE, LIGHT_BLUE, GREY]

bars = ax.bar(categories, values, color=colors2, edgecolor='white', width=0.6)

for bar, val in zip(bars, values):
    ypos = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, ypos * 1.25,
            f'{val:,}', ha='center', va='bottom', fontsize=9.5,
            fontweight='bold', color=DARK_BLUE)

ax.set_yscale('log')
ax.set_ylim(5, 250000)
ax.set_title('Cross-Zone Detections vs Total Traffic (Log Scale)',
             fontsize=12, fontweight='bold', color=DARK_BLUE, pad=12)
ax.set_ylabel('Vehicles', fontsize=10, color=DARK_BLUE)

# Move annotation higher and to the right to avoid overlap
ax.annotate('0.07% of\nCam 14 traffic', xy=(0, 15), xytext=(1.5, 200),
            fontsize=8.5, color=RED, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=RED, lw=1.2),
            ha='center')

plt.tight_layout()
plt.savefig(f'{OUT}/chart2_context.png', dpi=200, bbox_inches='tight')
plt.close()
print("Chart 2 fixed")


# ═══════════════════════════════════════════════════════════
# CHART 7 FIX: Trip Generation Model
# ═══════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(7.5, 5.0))

scenarios = ['Conservative\n(4.0 trips/dwelling)', 'Mid-range\n(5.0 trips/dwelling)',
             'Standard TRICS\n(5.7 trips/dwelling)', 'High\n(6.5 trips/dwelling)']

residential = [3419, 4274, 4893, 5556]
additional = [1200, 1200, 1200, 1200]

x = np.arange(len(scenarios))
w = 0.5

bars1 = ax.bar(x, residential, w, label='Residential trip generation\n(catchment households)', color=ACCENT)
bars2 = ax.bar(x, additional, w, bottom=residential, label='Schools, deliveries, visitors,\nbusinesses (estimated)', color=LIGHT_BLUE)

# Observed line
ax.axhline(y=6425, color=RED, linestyle='--', linewidth=2, label='Observed: 6,425 vehicles/day')

# Labels INSIDE the bars to avoid overlap with the line
for i, (r, a) in enumerate(zip(residential, additional)):
    # Residential count inside the dark bar
    ax.text(x[i], r/2, f'{r:,}', ha='center', va='center', fontsize=9,
            fontweight='bold', color='white')
    # Additional count inside the light bar
    ax.text(x[i], r + a/2, f'+{a:,}', ha='center', va='center', fontsize=8,
            color=DARK_BLUE)

# Totals ABOVE the bars, offset enough to clear the red line
for i, (r, a) in enumerate(zip(residential, additional)):
    total = r + a
    # Place total above bar, but if close to red line, go higher
    label_y = max(total + 150, 6600) if total > 5800 else total + 150
    ax.text(x[i], label_y, f'Total: {total:,}', ha='center', va='bottom',
            fontsize=8.5, fontweight='bold', color=DARK_BLUE)

ax.set_ylabel('Vehicles per Day', fontsize=10, color=DARK_BLUE)
ax.set_title('Can Local Demand Explain Luckwell Road Traffic?\nResidential Trip Generation Model vs Observed Volumes',
             fontsize=12, fontweight='bold', color=DARK_BLUE, pad=12)
ax.set_xticks(x)
ax.set_xticklabels(scenarios, fontsize=9)
ax.set_ylim(0, 9000)
ax.legend(fontsize=8.5, loc='upper left', framealpha=0.95)

plt.tight_layout()
plt.savefig(f'{OUT}/chart7_trip_generation.png', dpi=200, bbox_inches='tight')
plt.close()
print("Chart 7 fixed")


# ═══════════════════════════════════════════════════════════
# CHART 9 FIX: Waterfall explanation
# ═══════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(7.5, 4.5))

categories = ['Residents\n(TRICS 5.0)', 'School\ntrips', 'Deliveries\n& services', 'North St\nshops/pubs',
              'Visitors &\ntradespeople', 'Total\nexplained', 'Observed\ntraffic']
values = [4274, 450, 500, 400, 350, 5974, 6425]
colors_w = [ACCENT, LIGHT_BLUE, LIGHT_BLUE, LIGHT_BLUE, LIGHT_BLUE, GREEN, RED]

bars = ax.bar(categories, values, color=colors_w, edgecolor='white', width=0.6)

# Labels above each bar, well spaced
for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 120,
            f'{val:,}', ha='center', fontsize=9, fontweight='bold', color=DARK_BLUE)

# Gap annotation - use a bracket between the two tall bars
ax.annotate('', xy=(4.7, 5974), xytext=(4.7, 6425),
            arrowprops=dict(arrowstyle='<->', color=ORANGE, lw=2))
ax.text(4.7, 7200, 'Gap: 451 (7%)', fontsize=9.5, ha='center',
        color=ORANGE, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=ORANGE, alpha=0.9))

ax.set_title('Explaining Luckwell Road Traffic: Local Sources\nMid-range Trip Generation Model (5.0 trips/dwelling, 70% via Luckwell)',
             fontsize=11, fontweight='bold', color=DARK_BLUE, pad=12)
ax.set_ylabel('Vehicles per Day', fontsize=10, color=DARK_BLUE)
ax.set_ylim(0, 8000)

plt.tight_layout()
plt.savefig(f'{OUT}/chart9_waterfall.png', dpi=200, bbox_inches='tight')
plt.close()
print("Chart 9 fixed")

print("\nAll overlapping charts fixed.")
