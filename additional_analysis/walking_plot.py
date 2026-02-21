import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from matplotlib.patches import FancyArrowPatch

# ── Data extracted from the original chart ─────────────────────────────
# (children_walking_rate, total_walking_rate, MSA short name, state)
data = [
    (0.68, 4.35, "Bakersfield", "CA", "West"),
    (0.72, 4.10, "Fresno", "CA", "West"),
    (0.60, 3.70, "Tampa–St. Petersburg", "FL", "Florida"),
    (0.52, 3.45, "Jacksonville", "FL", "Florida"),
    (0.64, 3.40, "Riverside–San Bernardino", "CA", "West"),
    (0.44, 3.30, "Orlando–Kissimmee", "FL", "Florida"),
    (0.60, 3.25, "Phoenix–Mesa", "AZ", "Sun Belt"),
    (0.45, 3.05, "Miami–Fort Lauderdale", "FL", "Florida"),
    (0.38, 2.85, "San Antonio", "TX", "Sun Belt"),
    (0.27, 2.80, "San Diego", "CA", "West"),
    (0.42, 2.75, "Atlanta", "GA", "Sun Belt"),
    (0.36, 2.70, "Los Angeles", "CA", "West"),
    (0.62, 2.70, "Las Vegas", "NV", "Sun Belt"),
    (0.24, 2.50, "Houston", "TX", "Sun Belt"),
    (0.40, 2.35, "Philadelphia", "PA", "Northeast"),
    (0.20, 2.05, "San Jose", "CA", "West"),
    (0.34, 2.00, "Dallas–Fort Worth", "TX", "Sun Belt"),
    (0.30, 1.90, "Indianapolis", "IN", "Midwest"),
    (0.42, 1.85, "Detroit", "MI", "Midwest"),
    (0.52, 1.90, "St. Louis", "MO", "Midwest"),
    (0.16, 1.72, "San Francisco", "CA", "West"),
    (0.22, 1.70, "Washington, D.C.", "DC", "Northeast"),
    (0.10, 1.60, "Seattle", "WA", "West"),
    (0.18, 1.60, "New York", "NY", "Northeast"),
    (0.40, 1.58, "Salt Lake City", "UT", "West"),
    (0.58, 1.55, "McAllen–Edinburg", "TX", "Sun Belt"),
    (0.12, 1.48, "Milwaukee", "WI", "Midwest"),
    (0.32, 1.40, "Columbus", "OH", "Midwest"),
    (0.28, 1.20, "Chicago", "IL", "Midwest"),
    (0.22, 0.80, "Minneapolis–St. Paul", "MN", "Midwest"),
]

names = [d[2] for d in data]
states = [d[3] for d in data]
regions = [d[4] for d in data]
x = np.array([d[0] for d in data])
y = np.array([d[1] for d in data])

# ── Regression line ────────────────────────────────────────────────────
m, b = np.polyfit(x, y, 1)
x_line = np.linspace(0.05, 0.78, 100)
y_line = m * x_line + b

# ── Define which MSAs to highlight with labels ─────────────────────────
# Story-critical: the extremes, Florida cluster, and notable safe/dangerous outliers
highlight = {
    "Bakersfield", "Fresno",                          # worst overall
    "Tampa–St. Petersburg", "Orlando–Kissimmee", "Jacksonville", "Miami–Fort Lauderdale",  # Florida cluster
    "Minneapolis–St. Paul", "Chicago", "New York",    # safest
    "Phoenix–Mesa",                                    # Sun Belt
    "Philadelphia",                                    # mid-Atlantic reference
    "McAllen–Edinburg",                                # outlier: high child, low total
    "Las Vegas",                                       # outlier
    "Seattle",                                         # safest corner
}

# ── Regional colors ────────────────────────────────────────────────────
region_colors = {
    "Florida":   "#c44536",
    "Sun Belt":  "#d4730e",
    "West":      "#1b6087",
    "Northeast": "#555555",
    "Midwest":   "#6a994e",
}

point_colors = [region_colors[r] for r in regions]

# ── Figure ─────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 8))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

# Regression line — subtle
ax.plot(x_line, y_line, color="#cccccc", linewidth=1.5, zorder=1, linestyle="-")

# Non-highlighted points (gray, quiet)
for i in range(len(names)):
    if names[i] not in highlight:
        ax.scatter(x[i], y[i], color="#c8c8c8", s=40, zorder=2, edgecolors="none")

# Highlighted points (colored by region)
for i in range(len(names)):
    if names[i] in highlight:
        ax.scatter(x[i], y[i], color=point_colors[i], s=55, zorder=3, edgecolors="none")

# ── Labels for highlighted MSAs only ───────────────────────────────────
label_offsets = {
    "Bakersfield":           (8, 8),
    "Fresno":                (8, -2),
    "Tampa–St. Petersburg":  (-12, 8),
    "Jacksonville":          (-12, 8),
    "Orlando–Kissimmee":     (-12, 8),
    "Miami–Fort Lauderdale": (-12, -14),
    "Phoenix–Mesa":          (-12, -14),
    "Minneapolis–St. Paul":  (8, -8),
    "Chicago":               (-8, -14),
    "New York":              (8, 8),
    "Philadelphia":          (-12, -14),
    "McAllen–Edinburg":      (8, -4),
    "Las Vegas":             (8, -10),
    "Seattle":               (8, 6),
}

for i in range(len(names)):
    if names[i] in highlight:
        offset = label_offsets.get(names[i], (8, 4))
        ax.annotate(
            names[i],
            xy=(x[i], y[i]),
            xytext=offset,
            textcoords="offset points",
            fontsize=8.3,
            fontfamily="serif",
            color=point_colors[i],
            fontweight="bold",
            ha="left" if offset[0] > 0 else "right",
            va="center",
        )

# ── STORY ANNOTATIONS ─────────────────────────────────────────────────

# Florida cluster callout
ax.annotate(
    "Florida metros dominate\nthe most dangerous quadrant",
    xy=(0.52, 3.50), xytext=(0.12, 4.15),
    fontsize=9.5, fontstyle="italic", color="#c44536", fontfamily="serif",
    ha="left", va="center", linespacing=1.2,
    arrowprops=dict(arrowstyle="-", color="#c44536", lw=0.8, connectionstyle="arc3,rad=-0.15"),
)

# Safe corner callout
ax.annotate(
    "Northern metros tend to have\nthe lowest fatality rates for\nboth children and adults",
    xy=(0.18, 1.15), xytext=(0.36, 0.55),
    fontsize=9, fontstyle="italic", color="#6a994e", fontfamily="serif",
    ha="left", va="center", linespacing=1.2,
    arrowprops=dict(arrowstyle="-", color="#6a994e", lw=0.8, connectionstyle="arc3,rad=0.15"),
)

# McAllen outlier
ax.annotate(
    "High child rate,\nbut low overall",
    xy=(0.58, 1.55), xytext=(0.63, 1.0),
    fontsize=8, fontstyle="italic", color="#d4730e", fontfamily="serif",
    ha="left", va="center", linespacing=1.1,
    arrowprops=dict(arrowstyle="-", color="#d4730e", lw=0.7),
)

# ── Axes ───────────────────────────────────────────────────────────────
ax.set_xlim(0.03, 0.78)
ax.set_ylim(0.4, 4.7)

ax.set_xticks(np.arange(0.1, 0.8, 0.1))
ax.set_xticklabels([f"{v:.1f}" for v in np.arange(0.1, 0.8, 0.1)],
                   fontsize=9, color="#555555", fontfamily="serif")
ax.set_yticks(np.arange(1.0, 4.6, 0.5))
ax.set_yticklabels([f"{v:.1f}" for v in np.arange(1.0, 4.6, 0.5)],
                   fontsize=9, color="#555555", fontfamily="serif")

# Axis labels
ax.set_xlabel("Children pedestrian fatality rate (per 100,000 children) →",
              fontsize=10.5, fontfamily="serif", color="#333333", labelpad=10)
ax.set_ylabel("Total pedestrian fatality rate (per 100,000) →",
              fontsize=10.5, fontfamily="serif", color="#333333", labelpad=10)

# Grid & spines
ax.yaxis.grid(True, color="#ececec", linewidth=0.4, zorder=0)
ax.xaxis.grid(True, color="#ececec", linewidth=0.4, zorder=0)
ax.set_axisbelow(True)
for spine in ax.spines.values():
    spine.set_visible(False)
ax.tick_params(axis="both", length=0)

# ── Title block ────────────────────────────────────────────────────────
fig.text(
    0.08, 0.96,
    "Where Children Walk in Danger,\nEveryone Does",
    fontsize=20, fontweight="bold", fontfamily="serif",
    color="#1a1a1a", va="top", linespacing=1.15
)
fig.text(
    0.08, 0.885,
    "Pedestrian fatality rates for children vs. the total population across the 30 largest\n"
    "U.S. metro areas, 2017–2022. Metros dangerous for child pedestrians tend to be\n"
    "dangerous for everyone — but some Sun Belt outliers break the pattern.",
    fontsize=10, fontfamily="serif",
    color="#666666", va="top", linespacing=1.35
)

# ── Region color key (compact, top-right) ──────────────────────────────
legend_x = 0.90
legend_y = 0.93
for i, (region, color) in enumerate(region_colors.items()):
    fig.text(legend_x, legend_y - i * 0.025, "●  " + region,
             fontsize=8.5, fontfamily="serif", color=color, va="center", ha="right")

# ── Caption ────────────────────────────────────────────────────────────
fig.text(
    0.08, 0.02,
    "Source: FARS 2017–2022; ACS population estimates  |  Top 30 metro areas by population  |  Gray dots: unlabeled metros",
    fontsize=7.5, fontfamily="serif", color="#999999"
)

plt.subplots_adjust(left=0.10, right=0.92, top=0.82, bottom=0.10)
plt.savefig("walking_fatality_nyt.png", dpi=300, bbox_inches="tight",
            facecolor="white", edgecolor="none")
print("Saved: walking_fatality_nyt.png")
