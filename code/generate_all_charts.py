"""Master chart generation script using correct KML camera data.
Regenerates all charts from scratch with verified coordinates and road names."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import numpy as np

OUT = "D:/Projects/Bristol/charts"

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

plt.rcParams.update({
    'font.family': 'sans-serif', 'font.size': 10,
    'axes.facecolor': '#ffffff', 'figure.facecolor': '#ffffff',
    'axes.edgecolor': LIGHT_GREY, 'axes.grid': True,
    'grid.color': LIGHT_GREY, 'grid.linewidth': 0.5,
})

# ── ANPR Camera reference from official KML ──────────────
ANPR_CAMERAS = {
    1:  ('Clift House Rd',      51.4443174, -2.6191869),
    2:  ('Bedminster Down Rd',  51.4323444, -2.6114178),
    3:  ('Parson St',           51.4332465, -2.6076636),
    4:  ('East St / A38',       51.4372250, -2.5994402),
    5:  ('Wells Rd',            51.4416539, -2.5787095),
    6:  ('Bedminster Parade S', 51.4448701, -2.5924720),
    7:  ('Coronation Rd E',     51.4456491, -2.5927366),
    8:  ('Winterstoke Rd',      51.4356402, -2.6195379),
    9:  ('St John\'s Lane',     51.4355985, -2.5966396),
    10: ('Winterstoke Rd N',    51.4402961, -2.6242030),
    11: ('Brook Gate',          51.4292802, -2.6341290),
    12: ('East St / B3120',     51.4395410, -2.6015495),
    13: ('St John\'s Lane E',   51.4360173, -2.5812466),
    14: ('Coronation Rd',       51.4459365, -2.6104158),
    15: ('Luckwell Rd area',    51.4365873, -2.6124624),
    16: ('North St',            51.4403222, -2.6094279),
    17: ('Malago Rd',           51.4364071, -2.5906095),
    18: ('Parson St S',         51.4350233, -2.6078966),
    19: ('North St / Luckwell', 51.4402263, -2.6108650),
    20: ('St John\'s Lane S',   51.4360413, -2.5933188),
    21: ('Wells Rd S',          51.4371644, -2.5777601),
    22: ('Windmill Hill',       51.4427126, -2.5840744),
    23: ('Wells Rd N',          51.4427252, -2.5763573),
    24: ('Bedminster Down S',   51.4331887, -2.6116578),
    25: ('Windmill Hill S',     51.4399084, -2.5949870),
}


# ═══════════════════════════════════════════════════════════
# CHART 1: Daily traffic volumes - horizontal bars
# ═══════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(7.5, 4.5))

labels = ['Palmyra Road', 'Luckwell Road (S↔N)', 'Luckwell Road (W↔E)',
          'Bedminster Parade', 'North Street', 'Coronation Rd (west)',
          'Coronation Rd (east)', 'Winterstoke Road']
volumes = [1958, 5405, 6425, 9424, 9688, 18894, 23826, 28602]
colors = [ACCENT, ACCENT, ACCENT, GREY, GREY, GREY, GREY, GREY]

bars = ax.barh(labels, volumes, color=colors, edgecolor='white', height=0.6)
for bar, vol in zip(bars, volumes):
    ax.text(bar.get_width() + 300, bar.get_y() + bar.get_height()/2,
            f'{vol:,}', va='center', ha='left', fontsize=9, color=DARK_BLUE)

ax.set_xlabel('Average Daily Vehicles (Tue-Thu)', fontsize=10, color=DARK_BLUE)
ax.set_title('Daily Traffic Volumes: Residential Roads vs Main Roads',
             fontsize=12, fontweight='bold', color=DARK_BLUE, pad=12)
ax.set_xlim(0, 34000)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1000:.0f}k'))

# Legend
legend_elements = [
    mpatches.Patch(facecolor=ACCENT, label='Residential Roads'),
    mpatches.Patch(facecolor=GREY, label='Main Roads'),
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=9, framealpha=0.95)
plt.tight_layout()
plt.savefig(f'{OUT}/chart1_volumes.png', dpi=200, bbox_inches='tight')
plt.close()
print("Chart 1: volumes comparison")


# ═══════════════════════════════════════════════════════════
# CHART 2: Pie charts showing cross-zone as fraction of total
# ═══════════════════════════════════════════════════════════
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))

cam14_total = 15092
cam16_total = 7642
cross_zone_14 = 6   # Cam 14 → Cam 16
cross_zone_16 = 5   # Cam 16 → Cam 14

# Camera 14 pie
sizes_14 = [cam14_total - cross_zone_14, cross_zone_14]
colors_14 = [ACCENT, RED]
explode_14 = (0, 0.15)
wedges1, texts1, autotexts1 = ax1.pie(sizes_14, explode=explode_14, colors=colors_14,
    autopct=lambda p: f'{p:.2f}%' if p < 1 else f'{p:.1f}%',
    startangle=90, pctdistance=0.75,
    wedgeprops=dict(edgecolor='white', linewidth=2))
autotexts1[0].set_fontsize(10)
autotexts1[0].set_fontweight('bold')
autotexts1[0].set_color(DARK_BLUE)
autotexts1[1].set_fontsize(9)
autotexts1[1].set_fontweight('bold')
autotexts1[1].set_color(RED)
ax1.set_title(f'Camera 14 (Coronation Rd)\n{cam14_total:,} total vehicles',
              fontsize=10, fontweight='bold', color=DARK_BLUE, pad=10)

# Add annotation pointing to tiny red slice
ax1.annotate(f'{cross_zone_14} vehicles\nto Cam 16',
             xy=(0.02, -0.15), xytext=(0.7, -0.9),
             fontsize=9, fontweight='bold', color=RED, ha='center',
             arrowprops=dict(arrowstyle='->', color=RED, lw=1.5),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                       edgecolor=RED, alpha=0.9))

# Camera 16 pie
sizes_16 = [cam16_total - cross_zone_16, cross_zone_16]
colors_16 = [MID_BLUE, RED]
explode_16 = (0, 0.15)
wedges2, texts2, autotexts2 = ax2.pie(sizes_16, explode=explode_16, colors=colors_16,
    autopct=lambda p: f'{p:.2f}%' if p < 1 else f'{p:.1f}%',
    startangle=90, pctdistance=0.75,
    wedgeprops=dict(edgecolor='white', linewidth=2))
autotexts2[0].set_fontsize(10)
autotexts2[0].set_fontweight('bold')
autotexts2[0].set_color(DARK_BLUE)
autotexts2[1].set_fontsize(9)
autotexts2[1].set_fontweight('bold')
autotexts2[1].set_color(RED)
ax2.set_title(f'Camera 16 (North St)\n{cam16_total:,} total vehicles',
              fontsize=10, fontweight='bold', color=DARK_BLUE, pad=10)

ax2.annotate(f'{cross_zone_16} vehicles\nto Cam 14',
             xy=(0.02, -0.15), xytext=(0.7, -0.9),
             fontsize=9, fontweight='bold', color=RED, ha='center',
             arrowprops=dict(arrowstyle='->', color=RED, lw=1.5),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                       edgecolor=RED, alpha=0.9))

fig.suptitle('Cross-Zone Detections as a Fraction of Total Camera Traffic\n'
             '11 June 2024 — the red slices are so small they are barely visible',
             fontsize=11, fontweight='bold', color=DARK_BLUE, y=1.02)
plt.tight_layout()
plt.savefig(f'{OUT}/chart2_context.png', dpi=200, bbox_inches='tight')
plt.close()
print("Chart 2: pie chart context comparison")


# ═══════════════════════════════════════════════════════════
# CHART 3: Camera 14 destinations (bar chart)
# ═══════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(7.5, 4))

cam14_dests = {1: 924, 7: 75, 16: 2, 4: 5, 15: 0, 6: 3, 19: 2, 12: 0}
labels_14 = []
vals_14 = []
colors_14 = []
# Sort by value descending, include top destinations
cam14_full = [(1, 924, 'Clift House Rd'), (7, 75, 'Coronation Rd E'),
              (14, 10, 'Coronation Rd (self)'), (4, 5, 'East St / A38'),
              (6, 3, 'Bedminster Pde S'), (16, 2, 'North St'),
              (19, 2, 'North St / Luckwell'), (25, 1, 'Windmill Hill S')]
for cam, count, road in cam14_full:
    labels_14.append(f'Cam {cam} ({road})')
    vals_14.append(count)
    colors_14.append(RED if cam == 16 else ACCENT)

bars = ax.barh(labels_14, vals_14, color=colors_14, edgecolor='white', height=0.55)
for bar, val in zip(bars, vals_14):
    xpos = max(bar.get_width() + 10, 20)
    ax.text(xpos, bar.get_y() + bar.get_height()/2,
            f'{val}', va='center', ha='left', fontsize=9, fontweight='bold', color=DARK_BLUE)

ax.set_xlabel('Matched Vehicles (within 15 min)', fontsize=10, color=DARK_BLUE)
ax.set_title('Where Camera 14 (Coronation Rd) Traffic Goes\n'
             'Only 2 of 1,028 matched vehicles were next seen at Camera 16 (North St)',
             fontsize=11, fontweight='bold', color=DARK_BLUE, pad=12)
ax.set_xlim(0, 1100)
plt.tight_layout()
plt.savefig(f'{OUT}/chart3_cam14_destinations.png', dpi=200, bbox_inches='tight')
plt.close()
print("Chart 3: Camera 14 destinations")


# ═══════════════════════════════════════════════════════════
# CHART 3b: Camera 16 destinations (NEW)
# ═══════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(7.5, 5.5))

cam16_full = [
    (1,  629, 'Clift House Rd'),
    (4,  187, 'East St / A38'),
    (7,  112, 'Coronation Rd E'),
    (19, 110, 'North St / Luckwell'),
    (3,  108, 'Parson St'),
    (10,  99, 'Winterstoke Rd N'),
    (16,  48, 'North St (self)'),
    (8,   43, 'Winterstoke Rd'),
    (6,   24, 'Bedminster Pde S'),
    (15,  15, 'Luckwell Rd area'),
    (12,   9, 'East St / B3120'),
    (24,   7, 'Bedminster Down S'),
    (14,   4, 'Coronation Rd'),
]
labels_16 = []
vals_16 = []
colors_16 = []
for cam, count, road in cam16_full:
    labels_16.append(f'Cam {cam} ({road})')
    vals_16.append(count)
    colors_16.append(RED if cam == 14 else (ORANGE if cam == 1 else ACCENT))

bars = ax.barh(labels_16, vals_16, color=colors_16, edgecolor='white', height=0.6)
for bar, val in zip(bars, vals_16):
    xpos = max(bar.get_width() + 8, 15)
    ax.text(xpos, bar.get_y() + bar.get_height()/2,
            f'{val}', va='center', ha='left', fontsize=8.5, fontweight='bold', color=DARK_BLUE)

ax.set_xlabel('Matched Vehicles (within 15 min)', fontsize=10, color=DARK_BLUE)
ax.set_title('Where Camera 16 (North St) Traffic Goes\n'
             '45% went to Clift House Rd — along the perimeter, not through Southville',
             fontsize=11, fontweight='bold', color=DARK_BLUE, pad=12)
ax.set_xlim(0, 750)
plt.tight_layout()
plt.savefig(f'{OUT}/chart3b_cam16_destinations.png', dpi=200, bbox_inches='tight')
plt.close()
print("Chart 3b: Camera 16 destinations (NEW)")


# ═══════════════════════════════════════════════════════════
# CHART 4: Speed distributions on residential roads
# ═══════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 3, figsize=(7.5, 3.2), sharey=False)

bins_labels = ['5-10', '10-15', '15-20', '20-25', '25-30', '30-35', '35-40', '40+']
bins_mid = [7.5, 12.5, 17.5, 22.5, 27.5, 32.5, 37.5, 42.5]

counts_10 = [899, 7265, 28761, 39727, 11087, 1374, 151, 47]
counts_14 = [997, 6407, 13403, 5115, 516, 35, 8, 2]
counts_15 = [2951, 26097, 32919, 12646, 2119, 256, 40, 15]

datasets = [
    ('Luckwell Road (W↔E)\nLimit: 30 mph', counts_10, 30),
    ('Palmyra Road\nLimit: 20 mph', counts_14, 20),
    ('Luckwell Road (S↔N)\nLimit: 30 mph', counts_15, 30),
]

for ax_i, (title, counts, limit) in zip(axes, datasets):
    total = sum(counts)
    pcts = [c/total*100 for c in counts]
    colors_spd = [ACCENT if b <= limit else RED for b in bins_mid]
    ax_i.bar(range(len(bins_labels)), pcts, color=colors_spd, edgecolor='white', width=0.75)
    ax_i.set_xticks(range(len(bins_labels)))
    ax_i.set_xticklabels(bins_labels, fontsize=7, rotation=45)
    ax_i.set_title(title, fontsize=8.5, fontweight='bold', color=DARK_BLUE, pad=6)
    ax_i.set_ylabel('% of vehicles', fontsize=8, color=DARK_BLUE)
    ax_i.set_xlabel('Speed (mph)', fontsize=8, color=DARK_BLUE)
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


# ═══════════════════════════════════════════════════════════
# CHART 5: Top ANPR flows with correct road names from KML
# ═══════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(7.5, 4.5))

flow_labels = [
    'Cam 14 ↔ Cam 16\n(Coronation Rd ↔ North St)',
    'Cam 01 → Cam 07\n(Clift House → Coronation Rd E)',
    'Cam 01 → Cam 14\n(Clift House → Coronation Rd)',
    'Cam 02 → Cam 08\n(Bedminster Down → Winterstoke Rd)',
    'Cam 07 → Cam 01\n(Coronation Rd E → Clift House)',
    'Cam 10 → Cam 03\n(Winterstoke Rd N → Parson St)',
]
flow_vals = [6, 3617, 3702, 4561, 4801, 5657]
flow_colors = [RED, LIGHT_BLUE, LIGHT_BLUE, LIGHT_BLUE, LIGHT_BLUE, ACCENT]

bars = ax.barh(flow_labels, flow_vals, color=flow_colors, edgecolor='white', height=0.55)
for bar, val in zip(bars, flow_vals):
    xpos = max(val + 100, 300)
    ax.text(xpos, bar.get_y() + bar.get_height()/2,
            f'{val:,}', va='center', ha='left', fontsize=9.5, fontweight='bold', color=DARK_BLUE)

ax.set_xlabel('Matched Vehicles (within 15 min)', fontsize=10, color=DARK_BLUE)
ax.set_title('ANPR Origin-Destination Flows — 11 June 2024\nSouthville Cross-Zone vs Top Network Flows',
             fontsize=12, fontweight='bold', color=DARK_BLUE, pad=12)
ax.set_xlim(0, 7000)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1000:.0f}k' if x >= 1000 else f'{x:.0f}'))
plt.tight_layout()
plt.savefig(f'{OUT}/chart5_flows.png', dpi=200, bbox_inches='tight')
plt.close()
print("Chart 5: ANPR flows with correct road names")


# ═══════════════════════════════════════════════════════════
# CHART 6: Hourly traffic profiles
# ═══════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(7.5, 4))

hours = list(range(24))
luckwell_hourly = [63,24,14,12,13,52,211,473,601,440,368,367,375,375,371,408,519,600,436,278,176,125,93,71]
coronation_hourly = [97,54,37,32,43,121,555,1226,1478,1222,1099,1118,1141,1161,1152,1315,1659,1659,1169,756,459,301,175,118]

ax.plot(hours, coronation_hourly, '-', color=GREY, linewidth=2.5, label='Coronation Rd (east) - ATC 8', alpha=0.8)
ax.plot(hours, luckwell_hourly, '-', color=ACCENT, linewidth=2.5, label='Luckwell Rd (W↔E) - ATC 10')
ax.fill_between(hours, luckwell_hourly, alpha=0.15, color=ACCENT)

ax.set_xlabel('Hour of Day', fontsize=10, color=DARK_BLUE)
ax.set_ylabel('Vehicles', fontsize=10, color=DARK_BLUE)
ax.set_title('Hourly Traffic Profile: Luckwell Road vs Coronation Road\nBoth show similar commuter-style AM/PM peaks',
             fontsize=11, fontweight='bold', color=DARK_BLUE, pad=12)
ax.set_xticks([0, 3, 6, 9, 12, 15, 18, 21])
ax.set_xticklabels(['00', '03', '06', '09', '12', '15', '18', '21'])
ax.legend(fontsize=9, loc='upper right', framealpha=0.95)
plt.tight_layout()
plt.savefig(f'{OUT}/chart6_hourly.png', dpi=200, bbox_inches='tight')
plt.close()
print("Chart 6: hourly profiles")


# ═══════════════════════════════════════════════════════════
# CHART 7: Trip generation model (FULL version only)
# ═══════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(7.5, 4.5))

scenarios = ['Conservative\n4.0/dw/day', 'Mid-range\n5.0/dw/day',
             'Standard TRICS\n5.7/dw/day', 'High estimate\n6.5/dw/day']
generated = [5040, 6300, 7182, 8190]
via_luckwell = [3480, 4350, 4980, 5655]

x = np.arange(len(scenarios))
w = 0.35
ax.bar(x - w/2, generated, w, label='Total generated', color=PALE_BLUE, edgecolor='white')
ax.bar(x + w/2, via_luckwell, w, label='Via Luckwell Rd (70%)', color=ACCENT, edgecolor='white')

for i, (g, v) in enumerate(zip(generated, via_luckwell)):
    ax.text(x[i] - w/2, g + 120, f'{g:,}', ha='center', fontsize=8, fontweight='bold', color=DARK_BLUE)
    ax.text(x[i] + w/2, v + 120, f'{v:,}', ha='center', fontsize=8, fontweight='bold', color=DARK_BLUE)

ax.axhline(y=6425, color=RED, linestyle='--', linewidth=2, label='Observed: 6,425/day')
ax.text(3.5, 6600, '← Observed: 6,425', fontsize=9, color=RED, fontweight='bold', ha='right')

ax.set_ylabel('Vehicles per Day', fontsize=10, color=DARK_BLUE)
ax.set_title('Residential Trip Generation vs Observed Luckwell Road Traffic',
             fontsize=11, fontweight='bold', color=DARK_BLUE, pad=12)
ax.set_xticks(x)
ax.set_xticklabels(scenarios, fontsize=9)
ax.set_ylim(0, 9000)
ax.legend(fontsize=8.5, loc='upper left', framealpha=0.95)
plt.tight_layout()
plt.savefig(f'{OUT}/chart7_trip_generation.png', dpi=200, bbox_inches='tight')
plt.close()
print("Chart 7: trip generation model")


# ═══════════════════════════════════════════════════════════
# CHART 8: Combined ward car ownership
# ═══════════════════════════════════════════════════════════
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.5, 3.5))

# Pie: combined ward car ownership
car_own = [70, 30]
ax1.pie(car_own, labels=['Car-owning\nhouseholds\n~70%', 'No car\n~30%'],
        colors=[ACCENT, LIGHT_GREY], autopct='', startangle=90,
        wedgeprops=dict(edgecolor='white', linewidth=1.5))
ax1.set_title('Combined Ward\nCar Ownership', fontsize=10, fontweight='bold', color=DARK_BLUE)

# Funnel: households to catchment
funnel_labels = ['Combined ward\nhouseholds', 'Luckwell Rd\ncatchment', 'Car-owning\ncatchment']
funnel_vals = [11554, 1800, 1260]
bars = ax2.bar(funnel_labels, funnel_vals, color=[PALE_BLUE, LIGHT_BLUE, ACCENT], edgecolor='white', width=0.6)
for bar, val in zip(bars, funnel_vals):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 200,
             f'{val:,}', ha='center', fontsize=9, fontweight='bold', color=DARK_BLUE)
ax2.set_ylabel('Households', fontsize=9, color=DARK_BLUE)
ax2.set_title('Household Funnel\n(Bedminster + Southville)', fontsize=10, fontweight='bold', color=DARK_BLUE)
ax2.set_ylim(0, 13500)

plt.tight_layout()
plt.savefig(f'{OUT}/chart8_car_ownership.png', dpi=200, bbox_inches='tight')
plt.close()
print("Chart 8: car ownership")


# ═══════════════════════════════════════════════════════════
# CHART 9: Waterfall - traffic source breakdown
# ═══════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(7.5, 4))

categories = ['Residential\ntrips', 'School\ntraffic', 'Deliveries &\nservices',
              'Visitors &\ncommercial', 'Total\nexplained', 'Observed']
values = [4350, 400, 800, 500, 6050, 6425]
colors_wf = [ACCENT, LIGHT_BLUE, LIGHT_BLUE, LIGHT_BLUE, GREEN, RED]

bars = ax.bar(categories, values, color=colors_wf, edgecolor='white', width=0.6)
for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100,
            f'{val:,}', ha='center', fontsize=9, fontweight='bold', color=DARK_BLUE)

ax.axhline(y=6425, color=RED, linestyle='--', linewidth=1.5, alpha=0.5)

gap = 6425 - 6050
ax.annotate(f'Gap: {gap} vehicles\n(~6% — within\nestimation uncertainty)',
            xy=(4, 6050), xytext=(4.5, 5200),
            fontsize=8.5, color=ORANGE, fontweight='bold', ha='center',
            arrowprops=dict(arrowstyle='->', color=ORANGE, lw=1.2),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=ORANGE, alpha=0.9))

ax.set_ylabel('Vehicles per Day', fontsize=10, color=DARK_BLUE)
ax.set_title('Estimated Sources of Luckwell Road Traffic\nLocal demand can plausibly account for ~94% of observed volume',
             fontsize=11, fontweight='bold', color=DARK_BLUE, pad=12)
ax.set_ylim(0, 7500)
plt.tight_layout()
plt.savefig(f'{OUT}/chart9_waterfall.png', dpi=200, bbox_inches='tight')
plt.close()
print("Chart 9: waterfall breakdown")


# ═══════════════════════════════════════════════════════════
# CHART 10: Weekday vs Weekend 3-week profile
# ═══════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(8, 4.5))

dates = ['Fri\n7', 'Sat\n8', 'Sun\n9', 'Mon\n10', 'Tue\n11', 'Wed\n12',
         'Thu\n13', 'Fri\n14', 'Sat\n15', 'Sun\n16', 'Mon\n17', 'Tue\n18',
         'Wed\n19', 'Thu\n20', 'Fri\n21', 'Sat\n22', 'Sun\n23', 'Mon\n24',
         'Tue\n25', 'Wed\n26']

s10 = [5525, 5970, 5182, 6229, 6352, 6070, 5779, 6566, 5013, 4521,
       5941, 6113, 6579, 6661, 6547, 5750, 5080, 6286, 6515, 6362]
s15 = [4640, 5596, 5235, 5250, 5281, 5358, 5566, 6023, 4709, 3740,
       5046, 5292, 5401, 5636, 5778, 5140, 5073, 5231, 5432, 5348]
s14 = [1747, 1627, 1475, 1871, 1989, 1560, 1937, 1949, 1450, 1279,
       1699, 1834, 1910, 1667, 1928, 1658, 1197, 1777, 2060, 1925]

x = np.arange(len(dates))
for i, d in enumerate(dates):
    if 'Sat' in d or 'Sun' in d:
        ax.axvspan(i - 0.4, i + 0.4, alpha=0.12, color=ORANGE, zorder=0)

ax.plot(x, s10, 'o-', color=ACCENT, linewidth=2, markersize=5, label='Luckwell Rd (W↔E) - Site 10', zorder=5)
ax.plot(x, s15, 's-', color=MID_BLUE, linewidth=2, markersize=5, label='Luckwell Rd (S↔N) - Site 15', zorder=5)
ax.plot(x, s14, '^-', color=GREY, linewidth=2, markersize=5, label='Palmyra Rd - Site 14', zorder=5)

ax.axhline(y=6252, color=ACCENT, linestyle='--', linewidth=1, alpha=0.5)
ax.axhline(y=5377, color=MID_BLUE, linestyle='--', linewidth=1, alpha=0.5)
ax.axhline(y=1847, color=GREY, linestyle='--', linewidth=1, alpha=0.5)
ax.text(19.5, 6400, 'Wkday avg: 6,252', fontsize=7, color=ACCENT, ha='right', fontweight='bold')
ax.text(19.5, 5520, 'Wkday avg: 5,377', fontsize=7, color=MID_BLUE, ha='right', fontweight='bold')
ax.text(19.5, 2000, 'Wkday avg: 1,847', fontsize=7, color=GREY, ha='right', fontweight='bold')

ax.annotate('Weekend drop:\n−16%', xy=(9, 4521), xytext=(9, 3400),
            fontsize=8, color=ORANGE, fontweight='bold', ha='center',
            arrowprops=dict(arrowstyle='->', color=ORANGE, lw=1.2),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=ORANGE, alpha=0.9))

ax.set_xticks(x)
ax.set_xticklabels(dates, fontsize=7)
ax.set_ylabel('Daily Vehicles (2-way)', fontsize=10, color=DARK_BLUE)
ax.set_title('Daily Traffic Volumes: 3-Week Profile (7–26 June 2024)\nOrange shading = weekends',
             fontsize=11, fontweight='bold', color=DARK_BLUE, pad=12)
ax.set_ylim(0, 7500)
ax.legend(fontsize=8, loc='upper left', framealpha=0.95)
plt.tight_layout()
plt.savefig(f'{OUT}/chart10_weekly.png', dpi=200, bbox_inches='tight')
plt.close()
print("Chart 10: weekday vs weekend profile")


# ═══════════════════════════════════════════════════════════
# CHART 11: Weekday vs Weekend summary bars
# ═══════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(7, 4))

sites = ['Luckwell Rd\n(W↔E)', 'Luckwell Rd\n(S↔N)', 'Palmyra Rd']
weekday_avg = [6252, 5377, 1847]
weekend_avg = [5253, 4916, 1448]
pct_drop = [-16.0, -8.6, -21.6]

x = np.arange(len(sites))
w = 0.3
ax.bar(x - w/2, weekday_avg, w, label='Weekday average', color=ACCENT, edgecolor='white')
ax.bar(x + w/2, weekend_avg, w, label='Weekend average', color=LIGHT_BLUE, edgecolor='white')

for i, (wk, we, pct) in enumerate(zip(weekday_avg, weekend_avg, pct_drop)):
    ax.text(x[i] - w/2, wk + 100, f'{wk:,}', ha='center', fontsize=9, fontweight='bold', color=DARK_BLUE)
    ax.text(x[i] + w/2, we + 100, f'{we:,}', ha='center', fontsize=9, fontweight='bold', color=DARK_BLUE)
    ax.annotate(f'{pct:.0f}%', xy=(x[i] + w/2, we), xytext=(x[i] + w/2 + 0.25, we + 300),
                fontsize=9, fontweight='bold', color=ORANGE, ha='center',
                arrowprops=dict(arrowstyle='->', color=ORANGE, lw=1))

ax.set_ylabel('Vehicles per Day', fontsize=10, color=DARK_BLUE)
ax.set_title('Weekday vs Weekend Traffic: All Three Residential Roads',
             fontsize=11, fontweight='bold', color=DARK_BLUE, pad=12)
ax.set_xticks(x)
ax.set_xticklabels(sites, fontsize=9)
ax.set_ylim(0, 7500)
ax.legend(fontsize=9, loc='upper right', framealpha=0.95)
plt.tight_layout()
plt.savefig(f'{OUT}/chart11_weekday_weekend.png', dpi=200, bbox_inches='tight')
plt.close()
print("Chart 11: weekday vs weekend comparison")


# ═══════════════════════════════════════════════════════════
# CHART 13: JTC Turning Movements (Site 6 first, then Site 11)
# ═══════════════════════════════════════════════════════════
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4.5))

# Site 6 FIRST: Dean Lane / Cannon St / North St roundabout
movements_6 = [
    'Dean Lane→\nCannon St',
    'Dean Lane→\nNorth St',
    'North St→\nDean Lane',
    'North St→\nCannon St',
    'Cannon St→\nNorth St (W)',
    'Cannon St→\nDean Lane',
]
values_6 = [1377, 1541, 2284, 2456, 2703, 3844]
colors_6 = [LIGHT_BLUE, LIGHT_BLUE, MID_BLUE, MID_BLUE, ACCENT, ACCENT]

bars = ax1.barh(movements_6, values_6, color=colors_6, edgecolor='white', height=0.55)
for bar, val in zip(bars, values_6):
    ax1.text(bar.get_width() + 50, bar.get_y() + bar.get_height()/2,
             f'{val:,}', va='center', fontsize=8, fontweight='bold', color=DARK_BLUE)

ax1.set_xlabel('Vehicles (12hr)', fontsize=9, color=DARK_BLUE)
ax1.set_title('Site 6: Dean Lane / North St\n(roundabout — all perimeter roads)',
              fontsize=10, fontweight='bold', color=DARK_BLUE, pad=8)
ax1.set_xlim(0, 4800)

# Site 11: Raleigh Rd / North Street crossroads
movements_11 = [
    'North St→\nRaleigh (SW)',
    'North St→\nRaleigh (NE)',
    'Raleigh→\nNorth St (W)',
    'Raleigh→\nNorth St (E)',
    'North St\nthrough (E)',
    'North St\nthrough (W)',
]
values_11 = [736, 883, 467, 581, 2930, 3413]
colors_11 = [ORANGE, ORANGE, LIGHT_BLUE, LIGHT_BLUE, ACCENT, ACCENT]

bars = ax2.barh(movements_11, values_11, color=colors_11, edgecolor='white', height=0.55)
for bar, val in zip(bars, values_11):
    ax2.text(bar.get_width() + 50, bar.get_y() + bar.get_height()/2,
             f'{val:,}', va='center', fontsize=8, fontweight='bold', color=DARK_BLUE)

ax2.set_xlabel('Vehicles (12hr)', fontsize=9, color=DARK_BLUE)
ax2.set_title('Site 11: Raleigh Rd / North St\n(crossroads — Raleigh enters zone)',
              fontsize=10, fontweight='bold', color=DARK_BLUE, pad=8)
ax2.set_xlim(0, 4500)

fig.suptitle('Junction Turning Movements — 11 June 2024',
             fontsize=11, fontweight='bold', color=DARK_BLUE, y=1.02)
plt.tight_layout()
plt.savefig(f'{OUT}/chart13_jtc.png', dpi=200, bbox_inches='tight')
plt.close()
print("Chart 13: JTC turning movements (Site 6 first)")


print(f"\nAll charts generated in {OUT}")
