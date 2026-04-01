"""Generate map of all 25 ANPR camera locations + ATC sites relative to Southville Zone."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Polygon
import numpy as np
import contextily as ctx

OUT = "D:/Projects/Bristol/charts"

DARK_BLUE  = "#1a365d"
MID_BLUE   = "#2c5282"
ACCENT     = "#3182ce"
RED        = "#e53e3e"
ORANGE     = "#dd6b20"
GREY       = "#a0aec0"
LIGHT_GREY = "#e2e8f0"
ZONE_FILL  = "#fef3c7"
ZONE_EDGE  = "#d69e2e"

plt.rcParams.update({
    'font.family': 'sans-serif', 'font.size': 10,
    'figure.facecolor': '#ffffff',
})

def to_webmerc(lat, lon):
    x = lon * 20037508.34 / 180.0
    y = np.log(np.tan((90 + lat) * np.pi / 360.0)) / (np.pi / 180.0)
    y = y * 20037508.34 / 180.0
    return x, y

fig, ax = plt.subplots(figsize=(12, 10))

# ── Southville Zone polygon ─────────────────────────────
zone_coords = [(51.4462, -2.6160), (51.4462, -2.5930),
               (51.4398, -2.5930), (51.4398, -2.6160)]
zone_xy = [to_webmerc(lat, lon) for lat, lon in zone_coords]
zone_patch = Polygon(zone_xy, closed=True, facecolor=ZONE_FILL, edgecolor=ZONE_EDGE,
                     linewidth=2.5, linestyle='--', alpha=0.25, zorder=3)
ax.add_patch(zone_patch)
cx, cy = to_webmerc(51.4430, -2.6045)
ax.text(cx, cy, 'SOUTHVILLE\nZONE', ha='center', va='center',
        fontsize=13, fontweight='bold', color=ZONE_EDGE, alpha=0.7,
        style='italic', zorder=4)
ax.text(cx, cy - 140, '(no sensors inside)', ha='center', va='center',
        fontsize=10, color=ZONE_EDGE, alpha=0.6, style='italic', zorder=4)

# ── All 25 ANPR cameras from official KML ───────────────
ANPR_CAMERAS = {
    1:  ('Clift House Rd',      51.4443174, -2.6191869),
    2:  ('Bedminster Down Rd',  51.4323444, -2.6114178),
    3:  ('Parson St',           51.4332465, -2.6076636),
    4:  ('East St / A38',       51.4372250, -2.5994402),
    5:  ('Wells Rd',            51.4416539, -2.5787095),
    6:  ('Bedminster Parade S', 51.4448701, -2.5924720),
    7:  ('Coronation Rd E',     51.4456491, -2.5927366),
    8:  ('Winterstoke Rd',      51.4356402, -2.6195379),
    9:  ("St John's Lane",      51.4355985, -2.5966396),
    10: ('Winterstoke Rd N',    51.4402961, -2.6242030),
    11: ('Brook Gate',          51.4292802, -2.6341290),
    12: ('East St / B3120',     51.4395410, -2.6015495),
    13: ("St John's Lane E",    51.4360173, -2.5812466),
    14: ('Coronation Rd',       51.4459365, -2.6104158),
    15: ('Luckwell Rd area',    51.4365873, -2.6124624),
    16: ('North St',            51.4403222, -2.6094279),
    17: ('Malago Rd',           51.4364071, -2.5906095),
    18: ('Parson St S',         51.4350233, -2.6078966),
    19: ('North St / Luckwell', 51.4402263, -2.6108650),
    20: ("St John's Lane S",    51.4360413, -2.5933188),
    21: ('Wells Rd S',          51.4371644, -2.5777601),
    22: ('Windmill Hill',       51.4427126, -2.5840744),
    23: ('Wells Rd N',          51.4427252, -2.5763573),
    24: ('Bedminster Down S',   51.4331887, -2.6116578),
    25: ('Windmill Hill S',     51.4399084, -2.5949870),
}

# Cameras on the Southville boundary (highlighted)
BOUNDARY_CAMS = {14, 16}

# Label offsets: (ox, oy) in points — hand-tuned to avoid overlaps
# Positive ox = right, negative = left; positive oy = up, negative = down
LABEL_OFFSETS = {
    1:  (-60, 25),   2:  (-70, -15),  3:  (40, -20),   4:  (40, 15),
    5:  (40, 20),    6:  (40, -25),   7:  (40, 25),     8:  (-60, -15),
    9:  (-55, -20),  10: (-65, 15),   11: (-60, -15),   12: (40, 20),
    13: (45, -15),   14: (40, 25),    15: (-60, -25),   16: (45, -25),
    17: (40, -20),   18: (-55, -25),  19: (-65, 20),    20: (40, -25),
    21: (45, 15),    22: (40, 20),    23: (45, -15),    24: (45, -15),
    25: (-55, -20),
}

for cam_id, (road, lat, lon) in ANPR_CAMERAS.items():
    x, y = to_webmerc(lat, lon)
    is_boundary = cam_id in BOUNDARY_CAMS

    if is_boundary:
        ax.scatter(x, y, c=RED, s=130, zorder=8, edgecolors='white',
                   linewidth=1.8, marker='D')
        color = RED
        fw = 'bold'
    else:
        ax.scatter(x, y, c=MID_BLUE, s=70, zorder=7, edgecolors='white',
                   linewidth=1.2, marker='D')
        color = MID_BLUE
        fw = 'normal'

    ox, oy = LABEL_OFFSETS.get(cam_id, (40, 15))
    ax.annotate(f'{cam_id}', (x, y),
                textcoords="offset points", xytext=(ox, oy), fontsize=7.5,
                fontweight='bold', color=color, zorder=9,
                arrowprops=dict(arrowstyle='-', color=color, lw=0.5, alpha=0.5),
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                          edgecolor=color, alpha=0.85, linewidth=0.5))

# ── ATC sites (circles) ────────────────────────────────
atc_sites = [
    (51.445638, -2.592375, '8',  'Coronation Rd (E)',     35, -30, 'main'),
    (51.445985, -2.610599, '9',  'Coronation Rd (W)',    -55, 30,  'main'),
    (51.436500, -2.612421, '10', 'Luckwell Rd (W\u2194E)', -70, -10, 'res'),
    (51.435270, -2.608491, '14', 'Palmyra Rd',            -65, -20, 'res'),
    (51.440167, -2.611083, '15', 'Luckwell Rd (S\u2194N)', -65, -30, 'res'),
]
for lat, lon, num, road, ox, oy, kind in atc_sites:
    x, y = to_webmerc(lat, lon)
    c = ACCENT if kind == 'res' else MID_BLUE
    ax.scatter(x, y, c=c, s=80, zorder=7, edgecolors='white', linewidth=1.2, marker='o')
    ax.annotate(f'ATC {num}\n{road}', (x, y),
                textcoords="offset points", xytext=(ox, oy), fontsize=7,
                color=c, fontweight='bold' if kind == 'res' else 'normal', zorder=9,
                arrowprops=dict(arrowstyle='-', color=c, lw=0.5, alpha=0.5),
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                          edgecolor='none', alpha=0.8))

# ── "OUTSIDE ZONE" callout ──────────────────────────────
ax.annotate('Luckwell Rd & Palmyra Rd\nare OUTSIDE the\nSouthville Zone',
            xy=to_webmerc(51.4370, -2.611), xytext=to_webmerc(51.4320, -2.596),
            fontsize=8.5, color=ORANGE, fontweight='bold', ha='center', zorder=9,
            arrowprops=dict(arrowstyle='->', color=ORANGE, lw=1.8),
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                      edgecolor=ORANGE, alpha=0.95))

# ── Set map extent — wider to include all 25 cameras ────
x_min, y_min = to_webmerc(51.4230, -2.6400)
x_max, y_max = to_webmerc(51.4540, -2.5700)
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)

# ── Add basemap ─────────────────────────────────────────
ctx.add_basemap(ax, crs='EPSG:3857', source=ctx.providers.CartoDB.Positron,
                zoom=15, alpha=0.7)

# ── Legend ───────────────────────────────────────────────
legend_elements = [
    plt.scatter([], [], c=RED, s=80, marker='D', edgecolors='white',
                label='ANPR Camera (boundary)'),
    plt.scatter([], [], c=MID_BLUE, s=50, marker='D', edgecolors='white',
                label='ANPR Camera'),
    plt.scatter([], [], c=MID_BLUE, s=50, marker='o', edgecolors='white',
                label='ATC (main road)'),
    plt.scatter([], [], c=ACCENT, s=50, marker='o', edgecolors='white',
                label='ATC (residential road)'),
    mpatches.Patch(facecolor=ZONE_FILL, edgecolor=ZONE_EDGE, linestyle='--',
                   label='Southville Zone (approx.)'),
]
ax.legend(handles=legend_elements, loc='upper right', fontsize=8,
          framealpha=0.95, fancybox=True, edgecolor=LIGHT_GREY)

ax.set_title('All 25 ANPR Camera Locations & ATC Sensors\n'
             'Relative to the Southville Zone',
             fontsize=12, fontweight='bold', color=DARK_BLUE, pad=12)

ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

plt.tight_layout()
plt.savefig(f'{OUT}/chart_map.png', dpi=200, bbox_inches='tight')
plt.close()
print("Map chart generated — all 25 ANPR cameras + ATC sites")
