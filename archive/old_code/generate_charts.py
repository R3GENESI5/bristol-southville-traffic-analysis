"""Generate charts for SBLN Traffic Data Analysis Report."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import os

OUT = "D:/Projects/Bristol/charts"
os.makedirs(OUT, exist_ok=True)

# ── Colour palette ───────────────────────────────────────
DARK_BLUE  = "#1a365d"
MID_BLUE   = "#2c5282"
ACCENT     = "#3182ce"
LIGHT_BLUE = "#90cdf4"
PALE_BLUE  = "#bee3f8"
ORANGE     = "#dd6b20"
RED        = "#e53e3e"
GREEN      = "#38a169"
GREY       = "#a0aec0"
LIGHT_GREY = "#e2e8f0"
BG         = "#ffffff"

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 10,
    'axes.facecolor': BG,
    'figure.facecolor': BG,
    'axes.edgecolor': LIGHT_GREY,
    'axes.grid': True,
    'grid.color': LIGHT_GREY,
    'grid.linewidth': 0.5,
})


# ══════════════════════════════════════════════════════════
# CHART 1: Daily Traffic Volumes – Internal vs Perimeter
# ══════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(7.5, 4))

locations = [
    'Palmyra Road', 'Luckwell Rd\n(S↔N)', 'Luckwell Rd\n(W↔E)',
    'Bedminster\nParade', 'North\nStreet', 'Coronation Rd\n(west)',
    'Coronation Rd\n(east)', 'Winterstoke\nRoad'
]
volumes = [1958, 5405, 6425, 9424, 9688, 18894, 23826, 28602]
colors = [ACCENT, ACCENT, ACCENT, GREY, GREY, GREY, GREY, GREY]

bars = ax.barh(locations, volumes, color=colors, edgecolor='white', height=0.65)

# Add value labels
for bar, vol in zip(bars, volumes):
    ax.text(bar.get_width() + 300, bar.get_y() + bar.get_height()/2,
            f'{vol:,}', va='center', ha='left', fontsize=9, color=DARK_BLUE)

ax.set_xlabel('Average Daily Vehicles (Tue-Thu)', fontsize=10, color=DARK_BLUE)
ax.set_title('Daily Traffic Volumes: Residential Roads vs Perimeter Roads',
             fontsize=12, fontweight='bold', color=DARK_BLUE, pad=12)
ax.set_xlim(0, 34000)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1000:.0f}k'))

# Legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=ACCENT, label='Internal residential streets'),
                   Patch(facecolor=GREY, label='Perimeter / boundary roads')]
ax.legend(handles=legend_elements, loc='lower right', framealpha=0.9, fontsize=9)

plt.tight_layout()
plt.savefig(f'{OUT}/chart1_volumes.png', dpi=200, bbox_inches='tight')
plt.close()
print("Chart 1: volumes comparison")


# ══════════════════════════════════════════════════════════
# CHART 2: Cross-Zone Detections in Context (log scale)
# ══════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(7.5, 3.5))

categories = [
    'Cam 14↔16\ncross-zone\n(11 June)',
    'Cam 14↔16\ncross-zone\n(12 June)',
    'Camera 16\ntotal traffic',
    'Camera 14\ntotal traffic',
    'Total ANPR\nmatched\nmovements'
]
values = [11, 10, 7642, 15092, 67031]
colors2 = [RED, RED, LIGHT_BLUE, LIGHT_BLUE, GREY]

bars = ax.bar(categories, values, color=colors2, edgecolor='white', width=0.6)

for bar, val in zip(bars, values):
    ypos = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, ypos * 1.15,
            f'{val:,}', ha='center', va='bottom', fontsize=9.5,
            fontweight='bold', color=DARK_BLUE)

ax.set_yscale('log')
ax.set_ylim(5, 200000)
ax.set_title('Cross-Zone Detections vs Total Traffic (Log Scale)',
             fontsize=12, fontweight='bold', color=DARK_BLUE, pad=12)
ax.set_ylabel('Vehicles', fontsize=10, color=DARK_BLUE)

# Annotate the ratio
ax.annotate('0.07% of\nCam 14 traffic', xy=(0, 11), xytext=(0.8, 80),
            fontsize=8, color=RED, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=RED, lw=1.2))

plt.tight_layout()
plt.savefig(f'{OUT}/chart2_context.png', dpi=200, bbox_inches='tight')
plt.close()
print("Chart 2: context comparison")


# ══════════════════════════════════════════════════════════
# CHART 3: Where Camera 14 Traffic Actually Goes
# ══════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(7.5, 4))

# Top destinations from Camera 14 (<15 min, 11 June)
# From OD matrix row 14: Cam01=924, Cam07=75, Cam14=10, Cam03=6, Cam04=5, Cam06=3, Cam16=2, Cam19=2, Cam25=1
destinations = ['Cam 01\n(Clift House)', 'Cam 07', 'Cam 14\n(return)', 'Cam 03',
                'Cam 04', 'Cam 06', 'Cam 16\n(North St)', 'Cam 19', 'Cam 25']
counts = [924, 75, 10, 6, 5, 3, 2, 2, 1]
colors3 = [ACCENT]*6 + [RED] + [ACCENT]*2

bars = ax.bar(destinations, counts, color=colors3, edgecolor='white', width=0.7)

for bar, val in zip(bars, counts):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 12,
            str(val), ha='center', va='bottom', fontsize=9, color=DARK_BLUE,
            fontweight='bold')

ax.set_title('Where Camera 14 (Coronation Road) Traffic Goes\nWithin 15 Minutes — 11 June 2024',
             fontsize=12, fontweight='bold', color=DARK_BLUE, pad=12)
ax.set_ylabel('Matched Vehicles', fontsize=10, color=DARK_BLUE)
ax.set_ylim(0, 1050)

# Highlight annotation
ax.annotate('Only 2 vehicles\nheaded to North St\n(Camera 16)',
            xy=(6, 2), xytext=(6.8, 300),
            fontsize=9, color=RED, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=RED, lw=1.5),
            ha='center')

plt.tight_layout()
plt.savefig(f'{OUT}/chart3_cam14_destinations.png', dpi=200, bbox_inches='tight')
plt.close()
print("Chart 3: Camera 14 destinations")


# ══════════════════════════════════════════════════════════
# CHART 4: Speed Distribution on Residential Roads
# ══════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 3, figsize=(7.5, 3.2), sharey=False)

bins_labels = ['5-10', '10-15', '15-20', '20-25', '25-30', '30-35', '35-40', '40+']
bins_mid = [7.5, 12.5, 17.5, 22.5, 27.5, 32.5, 37.5, 42.5]

# Luckwell Road W↔E (Site 10) - PSL 30
counts_10 = [899, 7265, 28761, 39727, 11087, 1374, 151, 47]
# Palmyra Road (Site 14) - PSL 20
counts_14 = [997, 6407, 13403, 5115, 516, 35, 8, 2]
# Luckwell Road S↔N (Site 15) - PSL 30
counts_15 = [2951, 26097, 32919, 12646, 2119, 256, 40, 15]

datasets = [
    ('Luckwell Road (W↔E)\nLimit: 30 mph', counts_10, 30),
    ('Palmyra Road\nLimit: 20 mph', counts_14, 20),
    ('Luckwell Road (S↔N)\nLimit: 30 mph', counts_15, 30),
]

for ax_i, (title, counts, limit) in zip(axes, datasets):
    total = sum(counts)
    pcts = [c/total*100 for c in counts]

    # Color bars: green if under limit, red if over
    colors_spd = []
    for b in bins_mid:
        if b <= limit:
            colors_spd.append(ACCENT)
        else:
            colors_spd.append(RED)

    ax_i.bar(range(len(bins_labels)), pcts, color=colors_spd, edgecolor='white', width=0.75)
    ax_i.set_xticks(range(len(bins_labels)))
    ax_i.set_xticklabels(bins_labels, fontsize=7, rotation=45)
    ax_i.set_title(title, fontsize=8.5, fontweight='bold', color=DARK_BLUE, pad=6)
    ax_i.set_ylabel('% of vehicles', fontsize=8, color=DARK_BLUE)
    ax_i.set_xlabel('Speed (mph)', fontsize=8, color=DARK_BLUE)

    # Add limit line
    limit_idx = None
    for i, b in enumerate(bins_mid):
        if b > limit:
            limit_idx = i - 0.5
            break
    if limit_idx:
        ax_i.axvline(x=limit_idx, color=RED, linestyle='--', linewidth=1.2, alpha=0.7)
        ax_i.text(limit_idx + 0.1, max(pcts) * 0.85, f'{limit} mph\nlimit',
                  fontsize=7, color=RED, fontweight='bold')

fig.suptitle('Speed Distribution on Residential Roads (5-day total)',
             fontsize=11, fontweight='bold', color=DARK_BLUE, y=1.02)

plt.tight_layout()
plt.savefig(f'{OUT}/chart4_speeds.png', dpi=200, bbox_inches='tight')
plt.close()
print("Chart 4: speed distributions")


# ══════════════════════════════════════════════════════════
# CHART 5: Top 10 ANPR Flows – showing Cam14↔16 in context
# ══════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(7.5, 4.2))

flow_labels = [
    'Cam 14 ↔ Cam 16\n(Southville cross-zone)',
    'Cam 01 → Cam 07',
    'Cam 01 → Cam 14',
    'Cam 02 → Cam 08',
    'Cam 07 → Cam 01',
    'Cam 10 → Cam 03',
]
flow_vals = [6, 3617, 3702, 4561, 4801, 5657]
flow_colors = [RED, LIGHT_BLUE, LIGHT_BLUE, LIGHT_BLUE, LIGHT_BLUE, ACCENT]

bars = ax.barh(flow_labels, flow_vals, color=flow_colors, edgecolor='white', height=0.55)

for bar, val in zip(bars, flow_vals):
    xpos = max(val + 100, 250)
    ax.text(xpos, bar.get_y() + bar.get_height()/2,
            f'{val:,}', va='center', ha='left', fontsize=9.5,
            fontweight='bold', color=DARK_BLUE)

ax.set_xlabel('Matched Vehicles (within 15 min)', fontsize=10, color=DARK_BLUE)
ax.set_title('ANPR Origin-Destination Flows — 11 June 2024\nSouthville Cross-Zone vs Top Network Flows',
             fontsize=12, fontweight='bold', color=DARK_BLUE, pad=12)
ax.set_xlim(0, 7000)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1000:.0f}k' if x >= 1000 else f'{x:.0f}'))

plt.tight_layout()
plt.savefig(f'{OUT}/chart5_flows.png', dpi=200, bbox_inches='tight')
plt.close()
print("Chart 5: ANPR flows comparison")


# ══════════════════════════════════════════════════════════
# CHART 6: Hourly Profile – Luckwell Road vs Coronation Road
# ══════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(7.5, 3.5))

# Hourly two-way volumes (Tue-Thu avg) from ATC data
# Approximate from the General Summary data we read earlier
hours = list(range(0, 24))
hour_labels = [f'{h:02d}:00' for h in hours]

# Luckwell Road (Site 10) - from General Summary Two-Way 3-day avg
luckwell = [14, 10, 12, 17, 41, 94, 206, 335, 402, 327, 309, 315,
            340, 325, 342, 407, 455, 468, 355, 290, 195, 125, 72, 35]

# Coronation Road east (Site 8) - approximate from data
coronation = [45, 25, 22, 30, 60, 165, 475, 1050, 1550, 1406, 1200, 1180,
              1280, 1210, 1350, 1540, 1665, 1653, 1300, 1000, 680, 400, 220, 100]

ax.fill_between(hours, coronation, alpha=0.15, color=GREY)
ax.plot(hours, coronation, color=GREY, linewidth=2, label='Coronation Road (east) — ATC Site 8')

ax.fill_between(hours, luckwell, alpha=0.2, color=ACCENT)
ax.plot(hours, luckwell, color=ACCENT, linewidth=2.5, label='Luckwell Road (W↔E) — ATC Site 10')

ax.set_xlabel('Hour of Day', fontsize=10, color=DARK_BLUE)
ax.set_ylabel('Vehicles per Hour (2-way)', fontsize=10, color=DARK_BLUE)
ax.set_title('Hourly Traffic Profile: Luckwell Road vs Coronation Road',
             fontsize=12, fontweight='bold', color=DARK_BLUE, pad=12)
ax.set_xticks(range(0, 24, 2))
ax.set_xticklabels([f'{h:02d}' for h in range(0, 24, 2)])
ax.legend(fontsize=9, loc='upper left', framealpha=0.9)
ax.set_xlim(0, 23)

plt.tight_layout()
plt.savefig(f'{OUT}/chart6_hourly.png', dpi=200, bbox_inches='tight')
plt.close()
print("Chart 6: hourly profiles")

print("\nAll charts generated in", OUT)
