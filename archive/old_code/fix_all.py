"""Fix all charts and rebuild PDF with Matt's corrections."""
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
# CHART 2 FIX: Cross-Zone Detections - move annotation
# ═══════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(7.5, 4.0))
categories = ['Cam 14\u2194 16\ncross-zone\n(11 June)', 'Cam 14\u2194 16\ncross-zone\n(12 June)',
              'Camera 16\ntotal traffic', 'Camera 14\ntotal traffic', 'Total ANPR\nmatched\nmovements']
values = [11, 10, 7642, 15092, 67031]
colors2 = [RED, RED, LIGHT_BLUE, LIGHT_BLUE, GREY]
bars = ax.bar(categories, values, color=colors2, edgecolor='white', width=0.6)
for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() * 1.3,
            f'{val:,}', ha='center', va='bottom', fontsize=9.5, fontweight='bold', color=DARK_BLUE)
ax.set_yscale('log')
ax.set_ylim(5, 250000)
ax.set_title('Cross-Zone Detections vs Total Traffic (Log Scale)',
             fontsize=12, fontweight='bold', color=DARK_BLUE, pad=12)
ax.set_ylabel('Vehicles', fontsize=10, color=DARK_BLUE)
ax.annotate('0.07% of\nCam 14 traffic', xy=(0.15, 16), xytext=(1.6, 250),
            fontsize=8.5, color=RED, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=RED, lw=1.2), ha='center')
plt.tight_layout()
plt.savefig(f'{OUT}/chart2_context.png', dpi=200, bbox_inches='tight')
plt.close()
print("Chart 2 fixed")


# ═══════════════════════════════════════════════════════════
# CHART 5 FIX: Add road names to ANPR flows
# ═══════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(7.5, 4.5))

flow_labels = [
    'Cam 14 \u2194 Cam 16\n(Coronation Rd \u2194 North St)',
    'Cam 01 \u2192 Cam 07\n(Clift House \u2192 Coronation Rd)',
    'Cam 01 \u2192 Cam 14\n(Clift House \u2192 Coronation Rd)',
    'Cam 02 \u2192 Cam 08\n(Bedminster Down \u2192 Winterstoke Rd)',
    'Cam 07 \u2192 Cam 01\n(Coronation Rd \u2192 Clift House)',
    'Cam 10 \u2192 Cam 03\n(Winterstoke Rd \u2192 Parson St)',
]
flow_vals = [6, 3617, 3702, 4561, 4801, 5657]
flow_colors = [RED, LIGHT_BLUE, LIGHT_BLUE, LIGHT_BLUE, LIGHT_BLUE, ACCENT]

bars = ax.barh(flow_labels, flow_vals, color=flow_colors, edgecolor='white', height=0.55)
for bar, val in zip(bars, flow_vals):
    xpos = max(val + 100, 300)
    ax.text(xpos, bar.get_y() + bar.get_height()/2,
            f'{val:,}', va='center', ha='left', fontsize=9.5, fontweight='bold', color=DARK_BLUE)

ax.set_xlabel('Matched Vehicles (within 15 min)', fontsize=10, color=DARK_BLUE)
ax.set_title('ANPR Origin-Destination Flows \u2014 11 June 2024\nSouthville Cross-Zone vs Top Network Flows',
             fontsize=12, fontweight='bold', color=DARK_BLUE, pad=12)
ax.set_xlim(0, 7000)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1000:.0f}k' if x >= 1000 else f'{x:.0f}'))
plt.tight_layout()
plt.savefig(f'{OUT}/chart5_flows.png', dpi=200, bbox_inches='tight')
plt.close()
print("Chart 5 fixed (road names added)")


# ═══════════════════════════════════════════════════════════
# CHART 7 FIX: Trip generation - clear labels, updated title
# ═══════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(7.5, 5.0))
scenarios = ['Conservative\n(4.0 trips/dwelling)', 'Mid-range\n(5.0 trips/dwelling)',
             'Standard TRICS\n(5.7 trips/dwelling)', 'High\n(6.5 trips/dwelling)']
# Updated values using combined ward data (see PDF generator)
residential = [3480, 4350, 4980, 5655]
additional = [1200, 1200, 1200, 1200]
x = np.arange(len(scenarios))
w = 0.5
bars1 = ax.bar(x, residential, w, label='Residential trip generation\n(catchment households)', color=ACCENT)
bars2 = ax.bar(x, additional, w, bottom=residential, label='Schools, deliveries, visitors,\nbusinesses (estimated)', color=LIGHT_BLUE)
ax.axhline(y=6425, color=RED, linestyle='--', linewidth=2, label='Observed: 6,425 vehicles/day')
for i, (r, a) in enumerate(zip(residential, additional)):
    ax.text(x[i], r/2, f'{r:,}', ha='center', va='center', fontsize=9, fontweight='bold', color='white')
    ax.text(x[i], r + a/2, f'+{a:,}', ha='center', va='center', fontsize=8, color=DARK_BLUE)
for i, (r, a) in enumerate(zip(residential, additional)):
    total = r + a
    label_y = max(total + 150, 6700) if total > 5800 else total + 150
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
# CHART 8 FIX: Updated for combined wards
# ═══════════════════════════════════════════════════════════
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.5, 3.5))

# Blended car ownership (Bedminster + Southville average)
labels = ['No car\n(~30%)', '1 car\n(~49%)', '2 cars\n(~17%)', '3+ cars\n(~4%)']
sizes = [30, 49, 17, 4]
colors_pie = [GREY, ACCENT, MID_BLUE, DARK_BLUE]
explode = (0.03, 0, 0, 0)
wedges, texts = ax1.pie(sizes, labels=labels, colors=colors_pie, explode=explode,
                         startangle=90, textprops={'fontsize': 8.5})
ax1.set_title('Combined Ward\nCar Ownership (est.)', fontsize=10,
              fontweight='bold', color=DARK_BLUE, pad=8)

categories = ['Combined\nward hh', 'With car\naccess', 'Luckwell\ncatchment', 'Catchment\nwith car']
values = [11554, 8088, 1800, 1260]
colors_bar = [LIGHT_BLUE, ACCENT, LIGHT_BLUE, ACCENT]
bars = ax2.bar(categories, values, color=colors_bar, edgecolor='white', width=0.6)
for bar, val in zip(bars, values):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 150,
             f'{val:,}', ha='center', fontsize=9, fontweight='bold', color=DARK_BLUE)
ax2.set_title('Household Funnel:\nCombined Wards to Catchment', fontsize=10,
              fontweight='bold', color=DARK_BLUE, pad=8)
ax2.set_ylabel('Households', fontsize=9, color=DARK_BLUE)
ax2.set_ylim(0, 13500)
plt.tight_layout()
plt.savefig(f'{OUT}/chart8_car_ownership.png', dpi=200, bbox_inches='tight')
plt.close()
print("Chart 8 fixed (combined wards)")


# ═══════════════════════════════════════════════════════════
# CHART 9 FIX: Waterfall - clear spacing
# ═══════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(7.5, 4.5))
categories = ['Residents\n(TRICS 5.0)', 'School\ntrips', 'Deliveries\n& services', 'North St\nshops/pubs',
              'Visitors &\ntradespeople', 'Total\nexplained', 'Observed\ntraffic']
values = [4350, 450, 500, 400, 350, 6050, 6425]
colors_w = [ACCENT, LIGHT_BLUE, LIGHT_BLUE, LIGHT_BLUE, LIGHT_BLUE, GREEN, RED]
bars = ax.bar(categories, values, color=colors_w, edgecolor='white', width=0.6)
for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 120,
            f'{val:,}', ha='center', fontsize=9, fontweight='bold', color=DARK_BLUE)
ax.annotate('', xy=(4.7, 6050), xytext=(4.7, 6425),
            arrowprops=dict(arrowstyle='<->', color=ORANGE, lw=2))
ax.text(4.7, 7200, 'Gap: 375 (6%)', fontsize=9.5, ha='center',
        color=ORANGE, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=ORANGE, alpha=0.9))
ax.set_title('Explaining Luckwell Road Traffic: Local Sources\nMid-range Trip Generation Model (5.0 trips/dwelling, 70% via Luckwell)',
             fontsize=11, fontweight='bold', color=DARK_BLUE, pad=12)
ax.set_ylabel('Vehicles per Day', fontsize=10, color=DARK_BLUE)
ax.set_ylim(0, 8200)
plt.tight_layout()
plt.savefig(f'{OUT}/chart9_waterfall.png', dpi=200, bbox_inches='tight')
plt.close()
print("Chart 9 fixed")

print("\nAll charts regenerated.")
