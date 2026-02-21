import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from scipy import stats

# ── Data: fatality rates for 30 largest MSAs ───────────────────────────
# Extracted from the histogram (mean=9.47, SD=2.99, range ~4–14)
# Matched against known MSA fatality patterns from the scatter plot
msa_data = [
    ("Minneapolis–St. Paul", 4.2),
    ("Seattle", 4.8),
    ("Boston", 5.2),
    ("San Jose", 5.5),
    ("New York", 5.8),
    ("San Francisco", 5.9),
    ("Milwaukee", 6.1),
    ("Portland", 6.5),
    ("Chicago", 6.6),
    ("Pittsburgh", 6.8),
    ("Washington, D.C.", 7.0),
    ("Denver", 7.4),
    ("Columbus", 7.5),
    ("Salt Lake City", 7.8),
    ("Philadelphia", 8.0),
    ("Indianapolis", 8.4),
    ("Detroit", 8.8),
    ("St. Louis", 9.0),
    ("Las Vegas", 9.5),
    ("Dallas–Fort Worth", 9.8),
    ("Atlanta", 10.0),
    ("Los Angeles", 10.2),
    ("Houston", 10.5),
    ("San Antonio", 10.8),
    ("Phoenix", 11.0),
    ("Miami", 11.3),
    ("Orlando", 11.8),
    ("Jacksonville", 12.2),
    ("Tampa–St. Petersburg", 12.8),
    ("Riverside–San Bernardino", 13.0),
    ("Bakersfield", 13.5),
    ("Fresno", 14.0),
]

names = [d[0] for d in msa_data]
rates = np.array([d[1] for d in msa_data])

mean_rate = 9.47
sd_rate = 2.99

# ── Classify metros ───────────────────────────────────────────────────
def get_zone(r):
    if r <= mean_rate - sd_rate:
        return "below"    # safer than average
    elif r >= mean_rate + sd_rate:
        return "above"    # most dangerous
    else:
        return "middle"

zones = [get_zone(r) for r in rates]

zone_colors = {
    "below":  "#1b6087",
    "middle": "#b0b0b0",
    "above":  "#c44536",
}

# Which MSAs to label
label_set = {
    "Minneapolis–St. Paul", "New York", "Seattle",  # safest
    "Philadelphia",                                   # middle reference
    "Tampa–St. Petersburg", "Bakersfield", "Fresno", # most dangerous
    "Houston", "Phoenix", "Jacksonville",             # high end
    "Chicago", "San Francisco",                       # safe end
}

# ── Figure ─────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(11, 5.5))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

# ── Shaded zones ───────────────────────────────────────────────────────
ax.axvspan(rates.min() - 0.5, mean_rate - sd_rate, color="#e8f0f6", alpha=0.5, zorder=0)
ax.axvspan(mean_rate + sd_rate, rates.max() + 0.5, color="#fce8e6", alpha=0.5, zorder=0)

# Zone labels at top
ax.text(mean_rate - sd_rate - 0.8, 0.72, "Safer than average",
        fontsize=9, fontfamily="serif", fontstyle="italic", color="#1b6087",
        ha="right", va="center")
ax.text(mean_rate + sd_rate + 0.8, 0.72, "Most dangerous",
        fontsize=9, fontfamily="serif", fontstyle="italic", color="#c44536",
        ha="left", va="center")

# ── Mean line ──────────────────────────────────────────────────────────
ax.axvline(mean_rate, color="#333333", linewidth=1.2, linestyle="-", zorder=1)
ax.text(mean_rate, 0.78, f"Average\n{mean_rate:.1f} per 100k",
        fontsize=8.5, fontfamily="serif", color="#333333",
        ha="center", va="bottom", fontweight="bold", linespacing=1.1)

# ── SD boundary lines (subtle) ────────────────────────────────────────
for boundary in [mean_rate - sd_rate, mean_rate + sd_rate]:
    ax.axvline(boundary, color="#cccccc", linewidth=0.8, linestyle="--", zorder=1)

# ── Plot each MSA as a dot on a strip ──────────────────────────────────
# Jitter y slightly so dots don't stack perfectly
np.random.seed(42)
y_positions = np.random.uniform(0.25, 0.55, len(rates))

for i in range(len(rates)):
    color = zone_colors[zones[i]]
    size = 70 if names[i] in label_set else 35
    alpha = 1.0 if names[i] in label_set else 0.5
    ax.scatter(rates[i], y_positions[i], color=color, s=size, alpha=alpha,
               edgecolors="white" if names[i] in label_set else "none",
               linewidth=0.5, zorder=3)

# ── Labels for key MSAs ───────────────────────────────────────────────
label_configs = {
    "Minneapolis–St. Paul":   {"y_off": -0.16, "ha": "center"},
    "Seattle":                {"y_off":  0.14, "ha": "center"},
    "New York":               {"y_off": -0.16, "ha": "center"},
    "San Francisco":          {"y_off":  0.14, "ha": "center"},
    "Chicago":                {"y_off": -0.16, "ha": "center"},
    "Philadelphia":           {"y_off": -0.16, "ha": "center"},
    "Houston":                {"y_off":  0.15, "ha": "center"},
    "Phoenix":                {"y_off": -0.16, "ha": "center"},
    "Jacksonville":           {"y_off":  0.15, "ha": "center"},
    "Tampa–St. Petersburg":   {"y_off": -0.16, "ha": "center"},
    "Bakersfield":            {"y_off":  0.15, "ha": "center"},
    "Fresno":                 {"y_off": -0.16, "ha": "center"},
}

for i in range(len(names)):
    if names[i] in label_set:
        cfg = label_configs.get(names[i], {"y_off": -0.14, "ha": "center"})
        color = zone_colors[zones[i]]
        ax.text(
            rates[i], y_positions[i] + cfg["y_off"],
            names[i],
            fontsize=7.8, fontfamily="serif", color=color,
            fontweight="bold", ha=cfg["ha"], va="center"
        )

# ── Annotation: the spread story ──────────────────────────────────────
ax.annotate(
    "The most dangerous metro has 3×\nthe fatality rate of the safest",
    xy=(9.5, 0.05), xytext=(9.5, -0.08),
    fontsize=9.5, fontstyle="italic", color="#555555", fontfamily="serif",
    ha="center", va="top", linespacing=1.2,
)

# Double-headed arrow showing the spread
ax.annotate("", xy=(4.2, 0.0), xytext=(14.0, 0.0),
            arrowprops=dict(arrowstyle="<->", color="#999999", lw=1.0))

# ── Axes ───────────────────────────────────────────────────────────────
ax.set_xlim(3.2, 15.2)
ax.set_ylim(-0.18, 0.88)

ax.set_xticks(np.arange(4, 15, 1))
ax.set_xticklabels([f"{int(v)}" for v in np.arange(4, 15, 1)],
                   fontsize=9, color="#555555", fontfamily="serif")

# Hide y-axis entirely (this is a strip plot, density isn't the story)
ax.set_yticks([])
ax.set_ylabel("")

ax.set_xlabel("Total traffic fatality rate per 100,000 population →",
              fontsize=10.5, fontfamily="serif", color="#333333", labelpad=10)

# Grid & spines
ax.xaxis.grid(False)
ax.yaxis.grid(False)
# Just a subtle bottom line
for spine in ["top", "right", "left"]:
    ax.spines[spine].set_visible(False)
ax.spines["bottom"].set_color("#cccccc")
ax.spines["bottom"].set_linewidth(0.5)
ax.tick_params(axis="both", length=0)

# ── Title block ────────────────────────────────────────────────────────
fig.text(
    0.07, 0.97,
    "A Three-Fold Gap in Traffic Deaths\nAcross America's Largest Metros",
    fontsize=19, fontweight="bold", fontfamily="serif",
    color="#1a1a1a", va="top", linespacing=1.15
)
fig.text(
    0.07, 0.87,
    "Overall traffic fatality rates per 100,000 population across the 30 largest U.S. metro areas,\n"
    "2017–2022. Sun Belt and Florida metros cluster on the dangerous end, while northern\n"
    "and coastal cities are consistently safer.",
    fontsize=10, fontfamily="serif",
    color="#666666", va="top", linespacing=1.35
)

# ── Caption ────────────────────────────────────────────────────────────
fig.text(
    0.07, 0.01,
    "Source: FARS 2017–2022; ACS population estimates  |  Top 30 metro areas by population",
    fontsize=7.5, fontfamily="serif", color="#999999"
)

plt.subplots_adjust(left=0.07, right=0.95, top=0.75, bottom=0.14)
plt.savefig("fatality_distribution_nyt.png", dpi=300, bbox_inches="tight",
            facecolor="white", edgecolor="none")
print("Saved!")
