"""Generate additional charts: weekday/weekend, flow map, JTC turning movements."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import numpy as np
import contextily as ctx

OUT = "D:/Projects/Bristol/charts"

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


# ═══════════════════════════════════════════════════════════
# CHART 10: Weekday vs Weekend daily volumes
# ═══════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(8, 4.5))

dates = ['Fri\n7', 'Sat\n8', 'Sun\n9', 'Mon\n10', 'Tue\n11', 'Wed\n12',
         'Thu\n13', 'Fri\n14', 'Sat\n15', 'Sun\n16', 'Mon\n17', 'Tue\n18',
         'Wed\n19', 'Thu\n20', 'Fri\n21', 'Sat\n22', 'Sun\n23', 'Mon\n24',
         'Tue\n25', 'Wed\n26']

# Site 10 - Luckwell Road W↔E
s10 = [5525, 5970, 5182, 6229, 6352, 6070, 5779, 6566, 5013, 4521,
       5941, 6113, 6579, 6661, 6547, 5750, 5080, 6286, 6515, 6362]

# Site 15 - Luckwell Road S↔N
s15 = [4640, 5596, 5235, 5250, 5281, 5358, 5566, 6023, 4709, 3740,
       5046, 5292, 5401, 5636, 5778, 5140, 5073, 5231, 5432, 5348]

# Site 14 - Palmyra Road
s14 = [1747, 1627, 1475, 1871, 1989, 1560, 1937, 1949, 1450, 1279,
       1699, 1834, 1910, 1667, 1928, 1658, 1197, 1777, 2060, 1925]

x = np.arange(len(dates))

# Weekend shading
for i, d in enumerate(dates):
    if 'Sat' in d or 'Sun' in d:
        ax.axvspan(i - 0.4, i + 0.4, alpha=0.12, color=ORANGE, zorder=0)

ax.plot(x, s10, 'o-', color=ACCENT, linewidth=2, markersize=5, label='Luckwell Rd (W↔E) - Site 10', zorder=5)
ax.plot(x, s15, 's-', color=MID_BLUE, linewidth=2, markersize=5, label='Luckwell Rd (S↔N) - Site 15', zorder=5)
ax.plot(x, s14, '^-', color=GREY, linewidth=2, markersize=5, label='Palmyra Rd - Site 14', zorder=5)

# Weekday averages
ax.axhline(y=6252, color=ACCENT, linestyle='--', linewidth=1, alpha=0.5)
ax.axhline(y=5377, color=MID_BLUE, linestyle='--', linewidth=1, alpha=0.5)
ax.axhline(y=1847, color=GREY, linestyle='--', linewidth=1, alpha=0.5)

ax.text(19.5, 6252 + 100, 'Wkday avg: 6,252', fontsize=7, color=ACCENT, ha='right', fontweight='bold')
ax.text(19.5, 5377 + 100, 'Wkday avg: 5,377', fontsize=7, color=MID_BLUE, ha='right', fontweight='bold')
ax.text(19.5, 1847 + 100, 'Wkday avg: 1,847', fontsize=7, color=GREY, ha='right', fontweight='bold')

# Weekend drop annotations
ax.annotate('Weekend drop:\n-16%', xy=(9, 4521), xytext=(9, 3400),
            fontsize=8, color=ORANGE, fontweight='bold', ha='center',
            arrowprops=dict(arrowstyle='->', color=ORANGE, lw=1.2),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=ORANGE, alpha=0.9))

ax.set_xticks(x)
ax.set_xticklabels(dates, fontsize=7)
ax.set_ylabel('Daily Vehicles (2-way)', fontsize=10, color=DARK_BLUE)
ax.set_title('Daily Traffic Volumes: 3-Week Profile (7-26 June 2024)\nOrange shading = weekends',
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
bars1 = ax.bar(x - w/2, weekday_avg, w, label='Weekday average', color=ACCENT, edgecolor='white')
bars2 = ax.bar(x + w/2, weekend_avg, w, label='Weekend average', color=LIGHT_BLUE, edgecolor='white')

for i, (wk, we, pct) in enumerate(zip(weekday_avg, weekend_avg, pct_drop)):
    ax.text(x[i] - w/2, wk + 100, f'{wk:,}', ha='center', fontsize=9, fontweight='bold', color=DARK_BLUE)
    ax.text(x[i] + w/2, we + 100, f'{we:,}', ha='center', fontsize=9, fontweight='bold', color=DARK_BLUE)
    ax.annotate(f'{pct:.0f}%', xy=(x[i] + w/2, we), xytext=(x[i] + w/2 + 0.25, we + 300),
                fontsize=9, fontweight='bold', color=ORANGE, ha='center',
                arrowprops=dict(arrowstyle='->', color=ORANGE, lw=1))

ax.set_ylabel('Vehicles per Day', fontsize=10, color=DARK_BLUE)
ax.set_title('Weekday vs Weekend Traffic: All Three Residential Roads\nAll roads show reduced weekend volumes',
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
# CHART 12: ANPR Flow Map on OSM tiles
# ═══════════════════════════════════════════════════════════
def to_webmerc(lat, lon):
    x = lon * 20037508.34 / 180.0
    y = np.log(np.tan((90 + lat) * np.pi / 360.0)) / (np.pi / 180.0)
    y = y * 20037508.34 / 180.0
    return x, y

# Camera approximate positions (lat, lon) and road names
cameras = {
    1:  (51.4496, -2.6170, 'Clift House Rd'),
    2:  (51.4520, -2.5750, 'Feeder Rd'),
    3:  (51.4337, -2.6083, 'Parson St'),
    5:  (51.4420, -2.5870, 'East St'),
    7:  (51.4449, -2.5924, 'Bedminster Pde'),
    8:  (51.4456, -2.5850, 'Bath Rd'),
    9:  (51.4460, -2.6106, 'Coronation Rd W'),
    10: (51.4340, -2.5960, 'Wells Rd'),
    13: (51.4290, -2.5870, 'Hartcliffe Way'),
    14: (51.4452, -2.6070, 'Coronation Rd'),
    16: (51.4402, -2.6055, 'North St'),
    17: (51.4310, -2.5920, 'Airport Rd'),
}

# Top flows (origin, dest, count) - bidirectional pairs combined
top_flows = [
    (1,  7,  3617, 4801),   # Clift House <-> Bedminster Parade
    (1,  14, 3702, 924),    # Clift House <-> Coronation Rd
    (2,  8,  4561, 0),      # Feeder Rd -> Bath Rd
    (10, 3,  5657, 0),      # Wells Rd -> Parson St
    (5,  9,  2953, 1262),   # East St <-> Coronation Rd W
    (9,  13, 2278, 1388),   # Coronation Rd W <-> Hartcliffe Way
    (2,  3,  2391, 0),      # Feeder Rd -> Parson St
    (2,  10, 2135, 0),      # Feeder Rd -> Wells Rd
    (9,  17, 1479, 1419),   # Coronation Rd W <-> Airport Rd
    (14, 16, 2, 4),         # Coronation Rd <-> North St (THE CUT-THROUGH)
]

fig, ax = plt.subplots(figsize=(10, 9))

# Draw flows as arrows
for orig, dest, fwd, rev in top_flows:
    if orig not in cameras or dest not in cameras:
        continue
    x1, y1 = to_webmerc(cameras[orig][0], cameras[orig][1])
    x2, y2 = to_webmerc(cameras[dest][0], cameras[dest][1])

    total = fwd + rev
    is_cutthrough = (orig == 14 and dest == 16)

    if is_cutthrough:
        color = RED
        lw = 2.5
        alpha = 1.0
    else:
        color = ACCENT
        lw = max(1.5, min(total / 1200, 6))
        alpha = 0.6

    # Draw arrow from midpoint-offset to show both directions
    dx, dy = x2 - x1, y2 - y1
    # Shorten arrows so they don't overlap camera dots
    shrink = 0.12
    sx1 = x1 + dx * shrink
    sy1 = y1 + dy * shrink
    sx2 = x1 + dx * (1 - shrink)
    sy2 = y1 + dy * (1 - shrink)

    ax.annotate('', xy=(sx2, sy2), xytext=(sx1, sy1),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw, alpha=alpha,
                                connectionstyle='arc3,rad=0.05'))

    # Label on the arrow
    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2
    # Offset label perpendicular to arrow
    length = np.sqrt(dx**2 + dy**2)
    if length > 0:
        nx, ny = -dy / length * 80, dx / length * 80
    else:
        nx, ny = 0, 80

    if is_cutthrough:
        label = f'{total} vehicles\n(0.07%)'
        fontsize = 8.5
        fw = 'bold'
    else:
        label = f'{total:,}'
        fontsize = 7
        fw = 'normal'

    ax.text(mx + nx, my + ny, label, fontsize=fontsize, color=color,
            fontweight=fw, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor='none', alpha=0.85),
            zorder=10)

# Draw camera positions
for cam_id, (lat, lon, name) in cameras.items():
    x, y = to_webmerc(lat, lon)
    ax.scatter(x, y, c=DARK_BLUE, s=60, zorder=12, edgecolors='white', linewidth=1.2)
    ax.text(x, y + 70, f'{cam_id}', fontsize=7, color=DARK_BLUE, fontweight='bold',
            ha='center', va='bottom', zorder=13,
            bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor=DARK_BLUE,
                      alpha=0.85, linewidth=0.5))

# Highlight cam 14 and 16
for cam_id in [14, 16]:
    lat, lon, name = cameras[cam_id]
    x, y = to_webmerc(lat, lon)
    ax.scatter(x, y, c=RED, s=120, zorder=12, edgecolors='white', linewidth=1.8, marker='D')

# Set extent - wider to show all cameras
x_min, y_min = to_webmerc(51.4250, -2.6300)
x_max, y_max = to_webmerc(51.4560, -2.5700)
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)

ctx.add_basemap(ax, crs='EPSG:3857', source=ctx.providers.OpenStreetMap.Mapnik,
                zoom=15, alpha=0.5)

legend_elements = [
    plt.scatter([], [], c=DARK_BLUE, s=40, edgecolors='white', label='ANPR Camera'),
    plt.scatter([], [], c=RED, s=60, marker='D', edgecolors='white', label='Southville boundary cameras'),
    mpatches.FancyArrow(0, 0, 0.01, 0, color=ACCENT, width=0.003, label='Major traffic flow'),
    mpatches.FancyArrow(0, 0, 0.01, 0, color=RED, width=0.003, label='Cross-zone flow (6 vehicles)'),
]
ax.legend(handles=legend_elements, loc='upper right', fontsize=8, framealpha=0.95)

ax.set_title('ANPR Traffic Flows — 11 June 2024 (within 15 min)\n'
             'Arrow thickness proportional to volume. Cross-zone flow (red) is negligible.',
             fontsize=11, fontweight='bold', color=DARK_BLUE, pad=12)
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

plt.tight_layout()
plt.savefig(f'{OUT}/chart12_flow_map.png', dpi=200, bbox_inches='tight')
plt.close()
print("Chart 12: ANPR flow map")


# ═══════════════════════════════════════════════════════════
# CHART 13: JTC Turning Movements at Site 11 & Site 6
# ═══════════════════════════════════════════════════════════
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4.5))

# Site 11: Raleigh Rd / North Street crossroads
movements_11 = [
    'North St\nthrough (W)',
    'North St\nthrough (E)',
    'Raleigh→\nNorth St (E)',
    'Raleigh→\nNorth St (W)',
    'North St→\nRaleigh (NE)',
    'North St→\nRaleigh (SW)',
]
values_11 = [3413, 2930, 581, 467, 492 + 391, 480 + 256]  # combined turns
colors_11 = [ACCENT, ACCENT, LIGHT_BLUE, LIGHT_BLUE, ORANGE, ORANGE]

bars = ax1.barh(movements_11, values_11, color=colors_11, edgecolor='white', height=0.55)
for bar, val in zip(bars, values_11):
    ax1.text(bar.get_width() + 50, bar.get_y() + bar.get_height()/2,
             f'{val:,}', va='center', fontsize=8, fontweight='bold', color=DARK_BLUE)

ax1.set_xlabel('Vehicles (12hr)', fontsize=9, color=DARK_BLUE)
ax1.set_title('Site 11: Raleigh Rd / North St\n(crossroads)', fontsize=10,
              fontweight='bold', color=DARK_BLUE, pad=8)
ax1.set_xlim(0, 4500)

# Site 6: Dean Lane / Cannon St / North St roundabout
movements_6 = [
    'Cannon St→\nDean Lane',
    'Cannon St→\nNorth St (W)',
    'North St→\nCannon St',
    'North St→\nDean Lane',
    'Dean Lane→\nNorth St',
    'Dean Lane→\nCannon St',
]
values_6 = [3844, 2703, 2456, 2284, 1541, 1377]
colors_6 = [ACCENT, ACCENT, MID_BLUE, MID_BLUE, LIGHT_BLUE, LIGHT_BLUE]

bars = ax2.barh(movements_6, values_6, color=colors_6, edgecolor='white', height=0.55)
for bar, val in zip(bars, values_6):
    ax2.text(bar.get_width() + 50, bar.get_y() + bar.get_height()/2,
             f'{val:,}', va='center', fontsize=8, fontweight='bold', color=DARK_BLUE)

ax2.set_xlabel('Vehicles (12hr)', fontsize=9, color=DARK_BLUE)
ax2.set_title('Site 6: Dean Lane / North St\n(roundabout, ~200m E of Luckwell)',
              fontsize=10, fontweight='bold', color=DARK_BLUE, pad=8)
ax2.set_xlim(0, 4800)

fig.suptitle('Junction Turning Movements — 11 June 2024\nNorth Street through-traffic dominates; residential turns are secondary',
             fontsize=11, fontweight='bold', color=DARK_BLUE, y=1.04)
plt.tight_layout()
plt.savefig(f'{OUT}/chart13_jtc.png', dpi=200, bbox_inches='tight')
plt.close()
print("Chart 13: JTC turning movements")


print("\nAll new charts generated.")
