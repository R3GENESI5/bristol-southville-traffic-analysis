"""Generate ANPR flow map with arrows routed along actual roads using OSRM.
Clean version: only cameras involved in flows, no zone overlay, maximum impact."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import contextily as ctx
import requests
import time

OUT = "D:/Projects/Bristol/media"

DARK_BLUE  = "#1a365d"
MID_BLUE   = "#2c5282"
ACCENT     = "#3182ce"
RED        = "#e53e3e"
GREY       = "#a0aec0"
LIGHT_GREY = "#e2e8f0"

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
    """Get route geometry from OSRM demo server."""
    url = f"https://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}"
    params = {'overview': 'full', 'geometries': 'geojson'}
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        if data['code'] == 'Ok':
            coords = data['routes'][0]['geometry']['coordinates']
            return [to_webmerc(c[1], c[0]) for c in coords]
    except Exception as e:
        print(f"  Route failed ({lon1},{lat1} -> {lon2},{lat2}): {e}")
    return None

# Camera positions from official KML file (lat, lon)
cameras = {
    1:  (51.4443174, -2.6191869, 'Clift House Rd'),
    2:  (51.4323444, -2.6114178, 'Bedminster Down Rd'),
    3:  (51.4332465, -2.6076636, 'Parson St'),
    5:  (51.4416539, -2.5787095, 'Wells Rd'),
    7:  (51.4456491, -2.5927366, 'Coronation Rd E'),
    8:  (51.4356402, -2.6195379, 'Winterstoke Rd'),
    9:  (51.4355985, -2.5966396, "St John's Lane"),
    10: (51.4402961, -2.6242030, 'Winterstoke Rd N'),
    13: (51.4360173, -2.5812466, "St John's Lane E"),
    14: (51.4459365, -2.6104158, 'Coronation Rd'),
    16: (51.4403222, -2.6094279, 'North St'),
    17: (51.4364071, -2.5906095, 'Malago Rd'),
}

# Top flows: (origin, dest, total_vehicles)
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
    (14, 16, 6),     # THE cross-zone flow
]

print("Fetching routes from OSRM...")
routes = {}
for orig, dest, vol in flows:
    lat1, lon1, _ = cameras[orig]
    lat2, lon2, _ = cameras[dest]
    key = (orig, dest)
    print(f"  Cam {orig} -> Cam {dest} ({vol:,} vehicles)...", end=" ")
    route = get_route(lon1, lat1, lon2, lat2)
    if route:
        routes[key] = route
        print(f"OK ({len(route)} points)")
    else:
        print("FAILED - using straight line")
        routes[key] = [to_webmerc(lat1, lon1), to_webmerc(lat2, lon2)]
    time.sleep(0.5)

print(f"\nGot {len(routes)} routes. Generating map...")

fig, ax = plt.subplots(figsize=(14, 11))

# Draw routes
for (orig, dest), route_pts in routes.items():
    vol = next(v for o, d, v in flows if o == orig and d == dest)
    xs = [p[0] for p in route_pts]
    ys = [p[1] for p in route_pts]

    is_cutthrough = (orig == 14 and dest == 16)

    if is_cutthrough:
        color = RED
        lw = 1.5
        alpha = 1.0
        zorder = 8
    else:
        lw = max(2.0, min(vol / 700, 9))
        color = ACCENT
        alpha = 0.6
        zorder = 5

    ax.plot(xs, ys, color=color, linewidth=lw, alpha=alpha, zorder=zorder,
            solid_capstyle='round')

    # Arrowhead at ~70% along the route
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

    # Volume label at midpoint
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
        fontsize = 11
        fw = 'bold'
        fc = RED
    else:
        label = f'{vol:,}'
        fontsize = 9
        fw = 'bold'
        fc = DARK_BLUE

    ax.text(mx, my, label, fontsize=fontsize, color=fc, fontweight=fw,
            ha='center', va='center', zorder=11,
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                      edgecolor='none', alpha=0.88))

# Draw camera positions — only cameras involved in flows
BOUNDARY_CAMS = {14, 16}

for cam_id, (lat, lon, name) in cameras.items():
    x, y = to_webmerc(lat, lon)
    is_boundary = cam_id in BOUNDARY_CAMS

    if is_boundary:
        ax.scatter(x, y, c=RED, s=140, zorder=12, edgecolors='white',
                   linewidth=2, marker='D')
    else:
        ax.scatter(x, y, c=DARK_BLUE, s=70, zorder=12, edgecolors='white',
                   linewidth=1.5)

    label_color = RED if is_boundary else DARK_BLUE
    ax.text(x, y + 85, f'{cam_id}', fontsize=8.5,
            color=label_color, fontweight='bold',
            ha='center', va='bottom', zorder=13,
            bbox=dict(boxstyle='round,pad=0.15', facecolor='white',
                      edgecolor=label_color, alpha=0.88, linewidth=0.6))

# Map extent
x_min, y_min = to_webmerc(51.4250, -2.6300)
x_max, y_max = to_webmerc(51.4560, -2.5700)
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)

ctx.add_basemap(ax, crs='EPSG:3857', source=ctx.providers.CartoDB.Positron,
                zoom=15, alpha=0.7)

# Clean legend — 4 items only
legend_elements = [
    plt.scatter([], [], c=DARK_BLUE, s=50, edgecolors='white', label='ANPR Camera'),
    plt.scatter([], [], c=RED, s=80, marker='D', edgecolors='white',
                label='Southville boundary cameras'),
    mpatches.FancyArrow(0, 0, 0.01, 0, color=ACCENT, width=0.003,
                        label='Major traffic flow (road-routed)'),
    mpatches.FancyArrow(0, 0, 0.01, 0, color=RED, width=0.003,
                        label='Cross-zone flow (6 vehicles)'),
]
ax.legend(handles=legend_elements, loc='upper right', fontsize=10,
          framealpha=0.95, fancybox=True, edgecolor=LIGHT_GREY)

ax.set_title('ANPR Traffic Flows \u2014 11 June 2024 (within 15 min)\n'
             'Routes follow actual roads. Line thickness proportional to volume.',
             fontsize=14, fontweight='bold', color=DARK_BLUE, pad=14)
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

plt.tight_layout()
plt.savefig(f'{OUT}/chart12_flow_map.png', dpi=200, bbox_inches='tight')
plt.close()
print("Routed flow map saved.")
