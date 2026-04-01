"""Generate comprehensive traffic analysis map showing all data layers:
- All 25 ANPR cameras with road-routed flows
- All 22 ATC sites with daily volumes
- Southville Zone boundary
- ANPR flow arrows (road-routed via OSRM)
- Cross-zone flow highlighted
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Polygon
import numpy as np
import contextily as ctx
import requests
import time

OUT = "D:/Projects/Bristol/charts"

DARK_BLUE  = "#1a365d"
MID_BLUE   = "#2c5282"
ACCENT     = "#3182ce"
LIGHT_BLUE = "#90cdf4"
RED        = "#e53e3e"
ORANGE     = "#dd6b20"
GREEN      = "#38a169"
GREY       = "#a0aec0"
LIGHT_GREY = "#e2e8f0"
ZONE_FILL  = "#fef3c7"
ZONE_EDGE  = "#d69e2e"
ATC_COLOR  = "#805ad5"  # Purple for ATC sites

plt.rcParams.update({
    'font.family': 'sans-serif', 'font.size': 10,
    'figure.facecolor': '#ffffff',
})

def to_webmerc(lat, lon):
    x = lon * 20037508.34 / 180.0
    y = np.log(np.tan((90 + lat) * np.pi / 360.0)) / (np.pi / 180.0)
    y = y * 20037508.34 / 180.0
    return x, y

def get_route(lon1, lat1, lon2, lat2):
    url = f"https://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}"
    params = {'overview': 'full', 'geometries': 'geojson'}
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        if data['code'] == 'Ok':
            coords = data['routes'][0]['geometry']['coordinates']
            return [to_webmerc(c[1], c[0]) for c in coords]
    except Exception as e:
        print(f"  Route failed: {e}")
    return None

# ── All 25 ANPR cameras from KML ────────────────────────
ANPR = {
    1:  ('Clift House Rd',      51.4443174, -2.6191869),
    2:  ('Bedminster Down Rd',  51.4323444, -2.6114178),
    3:  ('Parson St',           51.4332465, -2.6076636),
    4:  ('East St / A38',       51.4372250, -2.5994402),
    5:  ('Wells Rd',            51.4416539, -2.5787095),
    6:  ('Bedminster Pde S',    51.4448701, -2.5924720),
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

# ── All 22 ATC sites from spreadsheets ──────────────────
ATC = {
    1:  ('Brook Gate',           51.429228, -2.634057),
    3:  ('Parson St',            51.433140, -2.607436),
    4:  ('West St (A38)',        51.439550, -2.601300),
    5:  ('Redcatch Rd',          51.435745, -2.580764),
    6:  ("St John's Lane N",     51.441047, -2.580085),
    7:  ('Bedminster Pde',       51.444889, -2.592389),
    8:  ('Coronation Rd (E)',    51.445638, -2.592375),
    9:  ('Coronation Rd (W)',    51.445985, -2.610599),
    10: ('Luckwell Rd (W-E)',    51.436500, -2.612421),
    11: ('North St (B3120)',     51.440160, -2.608831),
    12: ('Winterstoke Rd',       51.435923, -2.619850),
    13: ("St John's Lane",       51.436325, -2.591641),
    14: ('Palmyra Rd',           51.435270, -2.608491),
    15: ('Luckwell Rd (S-N)',    51.440167, -2.611083),
    16: ('Littleton Rd',         51.435887, -2.593258),
    17: ('Sylvia Ave',           51.437528, -2.576745),
    18: ("St Luke's Rd",         51.442659, -2.584057),
    19: ('Angers Rd',            51.442538, -2.576932),
    20: ('South Liberty Ln',     51.433006, -2.611927),
    21: ('Windmill Hill',        51.439876, -2.595009),
    22: ("St John's Lane S",     51.435530, -2.596647),
}

# ── ANPR flows ──────────────────────────────────────────
flows = [
    (10, 3,  5657),
    (7,  1,  4801),
    (2,  8,  4561),
    (5,  9,  4215),
    (1,  14, 3702),
    (1,  7,  3617),
    (9,  13, 3666),
    (9,  17, 2898),
    (2,  3,  2391),
    (2,  10, 2135),
    (14, 16, 6),
]

# Fetch routes
print("Fetching routes from OSRM...")
routes = {}
for orig, dest, vol in flows:
    lat1, lon1 = ANPR[orig][1], ANPR[orig][2]
    lat2, lon2 = ANPR[dest][1], ANPR[dest][2]
    key = (orig, dest)
    print(f"  ANPR {orig} -> ANPR {dest} ({vol:,})...", end=" ")
    route = get_route(lon1, lat1, lon2, lat2)
    if route:
        routes[key] = route
        print(f"OK ({len(route)} pts)")
    else:
        print("FAILED - straight line")
        routes[key] = [to_webmerc(lat1, lon1), to_webmerc(lat2, lon2)]
    time.sleep(0.5)

print(f"\nGenerating comprehensive analysis map...")

fig, ax = plt.subplots(figsize=(16, 13))

# ── Southville Zone ─────────────────────────────────────
zone_coords = [(51.4462, -2.6160), (51.4462, -2.5930),
               (51.4398, -2.5930), (51.4398, -2.6160)]
zone_xy = [to_webmerc(lat, lon) for lat, lon in zone_coords]
zone_patch = Polygon(zone_xy, closed=True, facecolor=ZONE_FILL,
                     edgecolor=ZONE_EDGE, linewidth=2.5, linestyle='--',
                     alpha=0.25, zorder=3)
ax.add_patch(zone_patch)
zcx, zcy = to_webmerc(51.4430, -2.6045)
ax.text(zcx, zcy, 'SOUTHVILLE\nZONE', ha='center', va='center',
        fontsize=12, fontweight='bold', color=ZONE_EDGE, alpha=0.5,
        style='italic', zorder=4)

# ── Draw flow routes ────────────────────────────────────
for (orig, dest), route_pts in routes.items():
    vol = next(v for o, d, v in flows if o == orig and d == dest)
    xs = [p[0] for p in route_pts]
    ys = [p[1] for p in route_pts]

    is_cutthrough = (orig == 14 and dest == 16)

    if is_cutthrough:
        color = RED
        lw = 4.5
        alpha = 1.0
        zorder = 8
    else:
        lw = max(2.0, min(vol / 700, 9))
        color = ACCENT
        alpha = 0.5
        zorder = 5

    ax.plot(xs, ys, color=color, linewidth=lw, alpha=alpha, zorder=zorder,
            solid_capstyle='round')

    # Arrowhead
    n = len(route_pts)
    if n > 3:
        idx = int(n * 0.7)
        x1, y1 = route_pts[idx - 1]
        x2, y2 = route_pts[idx]
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color=color,
                                    lw=min(lw, 3.5),
                                    alpha=min(alpha + 0.2, 1.0)),
                    zorder=zorder + 1)

    # Volume label
    mid_idx = n // 2
    mx, my = route_pts[mid_idx]
    if mid_idx > 0 and mid_idx < n - 1:
        dx = route_pts[mid_idx + 1][0] - route_pts[mid_idx - 1][0]
        dy = route_pts[mid_idx + 1][1] - route_pts[mid_idx - 1][1]
        length = np.sqrt(dx**2 + dy**2)
        if length > 0:
            offset = 70 if not is_cutthrough else 90
            nx, ny = -dy / length * offset, dx / length * offset
            mx += nx
            my += ny

    if is_cutthrough:
        label = '6 vehicles\n(0.07%)'
        fontsize = 10
        fc = RED
    else:
        label = f'{vol:,}'
        fontsize = 8
        fc = DARK_BLUE

    ax.text(mx, my, label, fontsize=fontsize, color=fc, fontweight='bold',
            ha='center', va='center', zorder=11,
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                      edgecolor='none', alpha=0.88))

# ── Draw ATC sites (purple squares with volume labels) ──
# Daily volumes for key ATC sites (Tue-Thu average)
ATC_VOLUMES = {
    7:  9424,   8:  23826,  9:  18894,  10: 6425,
    11: 9688,   12: 28602,  14: 1958,   15: 5405,
}

for atc_id, (road, lat, lon) in ATC.items():
    x, y = to_webmerc(lat, lon)
    ax.scatter(x, y, c=ATC_COLOR, s=55, zorder=9, edgecolors='white',
               linewidth=1, marker='s', alpha=0.85)

    # Show volume label for key sites
    if atc_id in ATC_VOLUMES:
        vol = ATC_VOLUMES[atc_id]
        vol_str = f'{vol:,}/d'
        ax.text(x, y - 90, vol_str, fontsize=6.5, color=ATC_COLOR,
                fontweight='bold', ha='center', va='top', zorder=10,
                bbox=dict(boxstyle='round,pad=0.15', facecolor='white',
                          edgecolor=ATC_COLOR, alpha=0.8, linewidth=0.4))

    # ATC number label
    ax.text(x + 50, y + 50, f'A{atc_id}', fontsize=6, color=ATC_COLOR,
            fontweight='bold', ha='left', va='bottom', zorder=10, alpha=0.8)

# ── Draw ANPR cameras ───────────────────────────────────
BOUNDARY_CAMS = {14, 16}
flow_cams = set()
for o, d, _ in flows:
    flow_cams.add(o)
    flow_cams.add(d)

for cam_id, (road, lat, lon) in ANPR.items():
    x, y = to_webmerc(lat, lon)
    is_boundary = cam_id in BOUNDARY_CAMS
    in_flow = cam_id in flow_cams

    if is_boundary:
        ax.scatter(x, y, c=RED, s=130, zorder=12, edgecolors='white',
                   linewidth=2, marker='D')
    elif in_flow:
        ax.scatter(x, y, c=DARK_BLUE, s=65, zorder=12, edgecolors='white',
                   linewidth=1.2)
    else:
        ax.scatter(x, y, c=DARK_BLUE, s=35, zorder=10, edgecolors='white',
                   linewidth=0.8, alpha=0.6)

    label_color = RED if is_boundary else DARK_BLUE
    alpha = 1.0 if (is_boundary or in_flow) else 0.6
    ax.text(x, y + 80, f'{cam_id}', fontsize=7,
            color=label_color, fontweight='bold', alpha=alpha,
            ha='center', va='bottom', zorder=13,
            bbox=dict(boxstyle='round,pad=0.12', facecolor='white',
                      edgecolor=label_color, alpha=0.85 * alpha,
                      linewidth=0.5))

# ── Map extent — wide enough for all sensors ────────────
x_min, y_min = to_webmerc(51.4230, -2.6400)
x_max, y_max = to_webmerc(51.4540, -2.5700)
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)

ctx.add_basemap(ax, crs='EPSG:3857', source=ctx.providers.CartoDB.Positron,
                zoom=15, alpha=0.65)

# ── Legend ──────────────────────────────────────────────
legend_elements = [
    plt.scatter([], [], c=RED, s=80, marker='D', edgecolors='white',
                label='ANPR boundary cameras (14, 16)'),
    plt.scatter([], [], c=DARK_BLUE, s=50, edgecolors='white',
                label='ANPR Camera'),
    plt.scatter([], [], c=ATC_COLOR, s=40, marker='s', edgecolors='white',
                label='ATC Sensor'),
    mpatches.FancyArrow(0, 0, 0.01, 0, color=ACCENT, width=0.003,
                        label='Major ANPR flow (road-routed)'),
    mpatches.FancyArrow(0, 0, 0.01, 0, color=RED, width=0.003,
                        label='Cross-zone flow (6 vehicles)'),
    mpatches.Patch(facecolor=ZONE_FILL, edgecolor=ZONE_EDGE, linestyle='--',
                   alpha=0.4, label='Southville Zone'),
]
ax.legend(handles=legend_elements, loc='upper right', fontsize=9,
          framealpha=0.95, fancybox=True, edgecolor=LIGHT_GREY)

ax.set_title('Comprehensive Traffic Analysis Map \u2014 SBLN 2024 Survey\n'
             '25 ANPR cameras, 22 ATC sensors, major ANPR flows (road-routed), '
             'and the Southville Zone',
             fontsize=13, fontweight='bold', color=DARK_BLUE, pad=14)
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

plt.tight_layout()
plt.savefig(f'{OUT}/chart_analysis_map.png', dpi=200, bbox_inches='tight')
plt.close()
print("Comprehensive analysis map saved.")
