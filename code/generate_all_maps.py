"""
Generate all maps for the Bristol Southville traffic analysis reports.

Produces:
    chart_map_anpr.png      – 25 ANPR camera locations
    chart_map_atc.png       – 22 ATC sensor locations
    chart_map_jtc.png       – 11 JTC junction locations
    chart_map_all_sensors.png – Combined (ANPR + ATC + JTC)
    chart_map_bus_stops.png – Bus stop locations

All saved to D:/Projects/Bristol/charts/
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import contextily as ctx
from shapely.geometry import Polygon, Point
from pyproj import Transformer

# ── Output ───────────────────────────────────────────────────────────
OUT_DIR = r"D:\Projects\Bristol\charts"
os.makedirs(OUT_DIR, exist_ok=True)

# ── Coordinate helpers ───────────────────────────────────────────────
_to_wm = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)

def to_webmerc(lat, lon):
    """Convert (lat, lon) → (x, y) in Web Mercator."""
    x, y = _to_wm.transform(lon, lat)
    return x, y

# ── Map extent (EPSG:3857) ───────────────────────────────────────────
x_min, y_min = to_webmerc(51.4230, -2.6400)
x_max, y_max = to_webmerc(51.4540, -2.5700)

# ── Southville Zone boundary ────────────────────────────────────────
zone_coords_ll = [
    (51.4462, -2.6160), (51.4462, -2.5930),
    (51.4398, -2.5930), (51.4398, -2.6160),
]
zone_coords_wm = [to_webmerc(lat, lon) for lat, lon in zone_coords_ll]
zone_poly = Polygon(zone_coords_wm)

# ── Sensor datasets ─────────────────────────────────────────────────
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

JTC = {
    1:  ("St Luke's Rd / St John's Lane", 51.440666, -2.581421),
    2:  ('Hendre Rd / Winterstoke Rd',    51.435048, -2.618615),
    3:  ('Parson St / Bedminster Down',   51.433718, -2.608254),
    4:  ('Bedminster Down / Winterstoke', 51.433096, -2.610332),
    5:  ('East St / Delby Ave',           51.442335, -2.595779),
    6:  ('Dean Lane / North St',          51.441430, -2.601555),
    7:  ('Wells Rd / St John\'s Lane',    51.441841, -2.578055),
    8:  ('East St / Sheene Rd',           51.439761, -2.600885),
    9:  ('Sheene Rd / Malago Rd',         51.437720, -2.600067),
    10: ("St John's Lane / Redcatch",     51.437465, -2.584305),
    11: ('Raleigh Rd / North St',         51.442149, -2.613461),
}

BUS_STOPS = {
    '1a':  ('North St EB',          51.4415, -2.6070),
    '1b':  ('North St WB',          51.4415, -2.6075),
    '2a':  ('North St EB (east)',   51.4418, -2.6010),
    '2b':  ('North St WB (east)',   51.4418, -2.6015),
    '3a':  ('North St EB (mid)',    51.4413, -2.6040),
    '3b':  ('North St WB (mid)',    51.4413, -2.6045),
    '4a':  ('Duckmoor Rd SB',       51.4380, -2.6150),
    '4b':  ('Duckmoor Rd NB',       51.4380, -2.6155),
    '5a':  ('Bedminster Pde NB',    51.4440, -2.5920),
    '5b':  ('Bedminster Pde SB',    51.4438, -2.5918),
    '6a':  ("St John's Rd SB",      51.4395, -2.5935),
    '6b':  ("St John's Rd NB",      51.4395, -2.5940),
    '7a':  ("St John's Lane EB",    51.4365, -2.5920),
    '7b':  ("St John's Lane WB",    51.4365, -2.5925),
    '8a':  ('Sheene Rd SB',         51.4380, -2.5990),
    '8b':  ('Sheene Rd NB',         51.4380, -2.5995),
    '9b':  ('West St SB',           51.4398, -2.6000),
    '10a': ('Winterstoke Rd SB',    51.4355, -2.6200),
    '10b': ('Winterstoke Rd NB',    51.4355, -2.6195),
}

# ── Annotation offsets to reduce label overlaps ──────────────────────
# Format:  sensor_id → (dx, dy) in points for the annotation offset.
# Positive dx = right, positive dy = up.  Default is (8, 4).
DEFAULT_OFFSET = (8, 4)

ANPR_OFFSETS = {
    6:  (8, -10),   7:  (8, 8),
    14: (-30, 4),  16: (-30, -8),  19: (8, -10),
    3:  (8, -10),  18: (-30, 4),
    2:  (8, -10),  24: (-30, 4),
    9:  (-30, 4),  20: (8, -10),
    15: (-30, 4),  17: (8, -10),
    21: (-30, 4),  5:  (8, -10),
    22: (8, -10),  23: (8, 8),
}

ATC_OFFSETS = {
    7:  (8, -10),   8:  (8, 8),
    10: (-30, 4),  15: (8, -10),  11: (-30, -8),
    3:  (8, -10),  20: (-30, 4),  14: (8, -10),
    13: (-30, 4),  16: (8, -10),  22: (8, 8),
    5:  (8, -10),  17: (-30, 4),
    6:  (8, 8),    18: (-30, 4),  19: (8, -10),
}

JTC_OFFSETS = {
    3: (8, -10),   4: (-35, 4),
    5: (8, -10),   6: (-35, 4),
    8: (8, -10),   9: (-35, 4),
    1: (8, -10),   7: (-35, 4),
}

BUS_OFFSETS = {
    '1a': (8, 4),   '1b': (-30, -8),
    '2a': (8, 4),   '2b': (-30, -8),
    '3a': (8, 4),   '3b': (-30, -8),
    '4a': (8, 4),   '4b': (-30, -8),
    '5a': (8, 4),   '5b': (-30, -8),
    '6a': (8, 4),   '6b': (-30, -8),
    '7a': (8, 4),   '7b': (-30, -8),
    '8a': (8, 4),   '8b': (-30, -8),
    '10a': (8, 4),  '10b': (-30, -8),
}

# ── Drawing helpers ──────────────────────────────────────────────────

def _setup_ax(ax, title):
    """Common axis setup: extent, tiles, zone, title."""
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron, zoom=15, alpha=0.7)

    # Southville Zone boundary
    zx, zy = zone_poly.exterior.xy
    ax.fill(zx, zy, facecolor='yellow', alpha=0.08, edgecolor='yellow',
            linewidth=2, linestyle='--', label='Southville Zone')

    ax.set_title(title, fontsize=14, fontweight='bold', pad=12)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel('')
    ax.set_ylabel('')
    for spine in ax.spines.values():
        spine.set_visible(False)


def _plot_sensors(ax, data, marker, color, size, label, offsets=None,
                  highlight_ids=None, highlight_color='red',
                  fontsize=7, zorder=5):
    """
    Plot a sensor dict on *ax*.

    Parameters
    ----------
    data : dict  {id: (name, lat, lon)}
    marker, color, size : marker style
    label : legend label
    offsets : dict {id: (dx, dy)} annotation offsets
    highlight_ids : set of ids to draw with highlight_color border
    """
    if offsets is None:
        offsets = {}
    if highlight_ids is None:
        highlight_ids = set()

    xs, ys = [], []
    for sid, (name, lat, lon) in data.items():
        px, py = to_webmerc(lat, lon)
        xs.append(px)
        ys.append(py)

        # Draw the marker
        ec = highlight_color if sid in highlight_ids else 'white'
        lw = 1.8 if sid in highlight_ids else 0.6
        ax.plot(px, py, marker=marker, markersize=size, color=color,
                markeredgecolor=ec, markeredgewidth=lw, zorder=zorder)

        # Label
        dx, dy = offsets.get(sid, DEFAULT_OFFSET)
        ax.annotate(str(sid), (px, py), fontsize=fontsize, fontweight='bold',
                    color='#333333',
                    xytext=(dx, dy), textcoords='offset points',
                    bbox=dict(boxstyle='round,pad=0.15', fc='white', alpha=0.75,
                              edgecolor='none'),
                    zorder=zorder + 1)


def _check_inside_zone(data):
    """Return set of sensor ids that fall inside the Southville Zone."""
    inside = set()
    for sid, (name, lat, lon) in data.items():
        px, py = to_webmerc(lat, lon)
        if zone_poly.contains(Point(px, py)):
            inside.add(sid)
    return inside


def _add_zone_note(ax, data):
    """If no sensors are inside the zone, add an annotation."""
    inside = _check_inside_zone(data)
    if not inside:
        cx, cy = zone_poly.centroid.x, zone_poly.centroid.y
        ax.annotate('No sensors within\nthe Southville Zone',
                    (cx, cy), fontsize=9, fontstyle='italic',
                    ha='center', va='center', color='#666666',
                    bbox=dict(boxstyle='round,pad=0.4', fc='white', alpha=0.85,
                              edgecolor='#cccccc'))


def _save(fig, filename):
    path = os.path.join(OUT_DIR, filename)
    fig.savefig(path, dpi=180, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  Saved  {path}")


# ── 1. ANPR map ─────────────────────────────────────────────────────
def make_anpr_map():
    print("[1/5] Generating ANPR camera map …")
    fig, ax = plt.subplots(figsize=(12, 10))
    _setup_ax(ax, 'ANPR Camera Locations — Southville Traffic Study')

    _plot_sensors(ax, ANPR, marker='D', color='red', size=8,
                  label='ANPR Camera', offsets=ANPR_OFFSETS,
                  highlight_ids={14, 16}, highlight_color='blue')

    _add_zone_note(ax, ANPR)

    legend_elements = [
        Line2D([0], [0], marker='D', color='w', markerfacecolor='red',
               markeredgecolor='white', markersize=8, label='ANPR Camera'),
        Line2D([0], [0], marker='D', color='w', markerfacecolor='red',
               markeredgecolor='blue', markeredgewidth=1.8, markersize=8,
               label='Boundary Camera (14, 16)'),
        mpatches.Patch(facecolor='yellow', alpha=0.25, edgecolor='yellow',
                       linestyle='--', linewidth=1.5, label='Southville Zone'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=9,
              framealpha=0.9, edgecolor='#cccccc')
    _save(fig, 'chart_map_anpr.png')


# ── 2. ATC map ──────────────────────────────────────────────────────
def make_atc_map():
    print("[2/5] Generating ATC sensor map …")
    fig, ax = plt.subplots(figsize=(12, 10))
    _setup_ax(ax, 'ATC Sensor Locations — Southville Traffic Study')

    _plot_sensors(ax, ATC, marker='s', color='purple', size=8,
                  label='ATC Sensor', offsets=ATC_OFFSETS)

    _add_zone_note(ax, ATC)

    legend_elements = [
        Line2D([0], [0], marker='s', color='w', markerfacecolor='purple',
               markeredgecolor='white', markersize=8, label='ATC Sensor'),
        mpatches.Patch(facecolor='yellow', alpha=0.25, edgecolor='yellow',
                       linestyle='--', linewidth=1.5, label='Southville Zone'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=9,
              framealpha=0.9, edgecolor='#cccccc')
    _save(fig, 'chart_map_atc.png')


# ── 3. JTC map ──────────────────────────────────────────────────────
def make_jtc_map():
    print("[3/5] Generating JTC junction map …")
    fig, ax = plt.subplots(figsize=(12, 10))
    _setup_ax(ax, 'JTC Junction Locations — Southville Traffic Study')

    _plot_sensors(ax, JTC, marker='^', color='green', size=9,
                  label='JTC Junction', offsets=JTC_OFFSETS)

    _add_zone_note(ax, JTC)

    legend_elements = [
        Line2D([0], [0], marker='^', color='w', markerfacecolor='green',
               markeredgecolor='white', markersize=9, label='JTC Junction'),
        mpatches.Patch(facecolor='yellow', alpha=0.25, edgecolor='yellow',
                       linestyle='--', linewidth=1.5, label='Southville Zone'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=9,
              framealpha=0.9, edgecolor='#cccccc')
    _save(fig, 'chart_map_jtc.png')


# ── 4. Combined map ─────────────────────────────────────────────────
def make_combined_map():
    print("[4/5] Generating combined sensor map …")
    fig, ax = plt.subplots(figsize=(12, 10))
    _setup_ax(ax, 'All Sensor Locations — Southville Traffic Study')

    _plot_sensors(ax, ANPR, marker='D', color='red', size=7,
                  label='ANPR', offsets=ANPR_OFFSETS, fontsize=6, zorder=5)
    _plot_sensors(ax, ATC, marker='s', color='purple', size=7,
                  label='ATC', offsets=ATC_OFFSETS, fontsize=6, zorder=6)
    _plot_sensors(ax, JTC, marker='^', color='green', size=8,
                  label='JTC', offsets=JTC_OFFSETS, fontsize=6, zorder=7)

    legend_elements = [
        Line2D([0], [0], marker='D', color='w', markerfacecolor='red',
               markeredgecolor='white', markersize=7, label='ANPR Camera (25)'),
        Line2D([0], [0], marker='s', color='w', markerfacecolor='purple',
               markeredgecolor='white', markersize=7, label='ATC Sensor (22)'),
        Line2D([0], [0], marker='^', color='w', markerfacecolor='green',
               markeredgecolor='white', markersize=8, label='JTC Junction (11)'),
        mpatches.Patch(facecolor='yellow', alpha=0.25, edgecolor='yellow',
                       linestyle='--', linewidth=1.5, label='Southville Zone'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=9,
              framealpha=0.9, edgecolor='#cccccc')
    _save(fig, 'chart_map_all_sensors.png')


# ── 5. Bus stops map ────────────────────────────────────────────────
def make_bus_stops_map():
    print("[5/5] Generating bus stops map …")
    fig, ax = plt.subplots(figsize=(12, 10))
    _setup_ax(ax, 'Bus Stop Locations — Southville Traffic Study')

    _plot_sensors(ax, BUS_STOPS, marker='o', color='orange', size=8,
                  label='Bus Stop', offsets=BUS_OFFSETS, fontsize=6)

    _add_zone_note(ax, BUS_STOPS)

    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='orange',
               markeredgecolor='white', markersize=8, label='Bus Stop'),
        mpatches.Patch(facecolor='yellow', alpha=0.25, edgecolor='yellow',
                       linestyle='--', linewidth=1.5, label='Southville Zone'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=9,
              framealpha=0.9, edgecolor='#cccccc')
    _save(fig, 'chart_map_bus_stops.png')


# ── Main ─────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("=" * 60)
    print("Bristol Southville — Map Generation")
    print("=" * 60)
    make_anpr_map()
    make_atc_map()
    make_jtc_map()
    make_combined_map()
    make_bus_stops_map()
    print("=" * 60)
    print("All maps generated successfully.")
    print("=" * 60)
