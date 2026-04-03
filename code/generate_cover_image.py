"""Generate a dramatic full-bleed cover image for the report.
Flow map as background with title overlay — think WEF/Carnegie style."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import contextily as ctx
import requests
import time
from matplotlib.patches import FancyBboxPatch

OUT = "D:/Projects/Bristol/media"

DARK_BLUE  = "#1a365d"
RED        = "#e53e3e"
ACCENT     = "#3182ce"

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
    except:
        pass
    return None

cameras = {
    1:  (51.4443174, -2.6191869), 2:  (51.4323444, -2.6114178),
    3:  (51.4332465, -2.6076636), 5:  (51.4416539, -2.5787095),
    7:  (51.4456491, -2.5927366), 8:  (51.4356402, -2.6195379),
    9:  (51.4355985, -2.5966396), 10: (51.4402961, -2.6242030),
    13: (51.4360173, -2.5812466), 14: (51.4459365, -2.6104158),
    16: (51.4403222, -2.6094279), 17: (51.4364071, -2.5906095),
}

flows = [
    (10, 3, 5657), (7, 1, 4801), (2, 8, 4561), (5, 9, 4215),
    (1, 14, 3702), (1, 7, 3617), (9, 13, 3666), (9, 17, 2898),
    (2, 3, 2391), (2, 10, 2135), (14, 16, 6),
]

print("Fetching routes...")
routes = {}
for orig, dest, vol in flows:
    lat1, lon1 = cameras[orig]
    lat2, lon2 = cameras[dest]
    route = get_route(lon1, lat1, lon2, lat2)
    if route:
        routes[(orig, dest)] = route
    else:
        routes[(orig, dest)] = [to_webmerc(lat1, lon1), to_webmerc(lat2, lon2)]
    time.sleep(0.3)

print("Generating cover image...")

# A4 portrait ratio (210x297mm) for full-page cover
fig, ax = plt.subplots(figsize=(11.7, 16.5))
fig.patch.set_facecolor(DARK_BLUE)

# Draw routes — no labels, no numbers, just the visual impact
for (orig, dest), route_pts in routes.items():
    vol = next(v for o, d, v in flows if o == orig and d == dest)
    xs = [p[0] for p in route_pts]
    ys = [p[1] for p in route_pts]

    is_cutthrough = (orig == 14 and dest == 16)

    if is_cutthrough:
        color = RED
        lw = 1.0
        alpha = 1.0
        zorder = 8
    else:
        lw = max(2.5, min(vol / 600, 10))
        color = ACCENT
        alpha = 0.6
        zorder = 5

    ax.plot(xs, ys, color=color, linewidth=lw, alpha=alpha, zorder=zorder,
            solid_capstyle='round')

# Camera dots — minimal
BOUNDARY = {14, 16}
for cam_id, (lat, lon) in cameras.items():
    x, y = to_webmerc(lat, lon)
    if cam_id in BOUNDARY:
        ax.scatter(x, y, c=RED, s=80, zorder=12, edgecolors='white', linewidth=1.5, marker='D')
    else:
        ax.scatter(x, y, c='white', s=30, zorder=12, edgecolors=ACCENT, linewidth=0.8, alpha=0.8)

# "6 vehicles" label — the punchline
mid_route = routes[(14, 16)]
mx, my = mid_route[len(mid_route)//2]
ax.text(mx - 200, my - 300, '6 vehicles\n(0.07%)', fontsize=13, color=RED,
        fontweight='bold', ha='center', va='center', zorder=15,
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=RED,
                  alpha=0.95, linewidth=1.5))

# Map extent — taller for A4 portrait
x_min, y_min = to_webmerc(51.4200, -2.6300)
x_max, y_max = to_webmerc(51.4600, -2.5700)
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)

ctx.add_basemap(ax, crs='EPSG:3857', source=ctx.providers.CartoDB.DarkMatter,
                zoom=15, alpha=0.85)

ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

# ── Title overlay — bottom of the image ─────────────────
# Semi-transparent dark band at bottom
band_y = y_min + (y_max - y_min) * 0.0
band_h = (y_max - y_min) * 0.15
rect = FancyBboxPatch((x_min, band_y), x_max - x_min, band_h,
                       boxstyle="square,pad=0", facecolor=DARK_BLUE, alpha=0.85,
                       zorder=20)
ax.add_patch(rect)

# Title text
title_x = x_min + (x_max - x_min) * 0.04
title_y = band_y + band_h * 0.65
ax.text(title_x, title_y,
        'Independent Analysis of the\nSouth Bristol Liveable Neighbourhoods\nTraffic Survey Data',
        fontsize=20, fontweight='bold', color='white', fontfamily='sans-serif',
        va='center', zorder=21, linespacing=1.3)

# Subtitle
sub_y = band_y + band_h * 0.15
ax.text(title_x, sub_y,
        'Ali Bin Shahid  |  April 2026  |  Based on SBLN 2024 Traffic Survey Results',
        fontsize=10, color='#90cdf4', fontfamily='sans-serif',
        va='center', zorder=21)

# Key stat — right side
stat_x = x_min + (x_max - x_min) * 0.75
stat_y = band_y + band_h * 0.55
ax.text(stat_x, stat_y, '0.07%', fontsize=42, fontweight='bold',
        color=RED, fontfamily='sans-serif', ha='center', va='center', zorder=21)
ax.text(stat_x, stat_y - band_h * 0.25, 'cross-zone traffic', fontsize=11,
        color='#e2e8f0', fontfamily='sans-serif', ha='center', va='center', zorder=21)

plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
plt.savefig(f'{OUT}/cover.png', dpi=200, bbox_inches='tight', pad_inches=0,
            facecolor=DARK_BLUE)
plt.close()
print("Cover image saved.")
