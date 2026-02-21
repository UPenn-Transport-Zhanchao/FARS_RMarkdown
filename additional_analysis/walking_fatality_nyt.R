# ── NYT-Style Walking Fatality Scatter ────────────────────────────────
# Drop this in after your existing data prep (line ~242 of motorcycle.R)
# Assumes `children_adults` data frame exists with columns:
#   walk_children (child ped fatality rate), rate (total ped fatality rate), cbsa_name.x

library(tidyverse)
library(ggrepel)

# ── Define regional groupings ──────────────────────────────────────────
florida_metros <- c("Tampa", "Jacksonville", "Orlando", "Miami")
sun_belt_metros <- c("Phoenix", "San Antonio", "Atlanta", "Houston", "Dallas",
                     "Las Vegas", "McAllen", "Riverside")
midwest_metros <- c("Minneapolis", "Chicago", "Milwaukee", "Columbus",
                    "Detroit", "Indianapolis", "St. Louis")
northeast_metros <- c("New York", "Philadelphia", "Washington")
# Everything else → "West"

children_adults <- children_adults %>%
  mutate(
    short_name = str_extract(cbsa_name.x, "^[^-,]+"),
    region = case_when(
      str_detect(cbsa_name.x, paste(florida_metros, collapse = "|")) &
        str_detect(cbsa_name.x, "FL") ~ "Florida",
      str_detect(cbsa_name.x, paste(sun_belt_metros, collapse = "|")) ~ "Sun Belt",
      str_detect(cbsa_name.x, paste(midwest_metros, collapse = "|")) ~ "Midwest",
      str_detect(cbsa_name.x, paste(northeast_metros, collapse = "|")) ~ "Northeast",
      TRUE ~ "West"
    ),
    # Flag which metros to label (the story-critical ones)
    highlight = str_detect(cbsa_name.x, paste(c(
      "Bakersfield", "Fresno",
      "Tampa", "Jacksonville", "Orlando", "Miami",
      "Minneapolis", "Chicago", "New York",
      "Phoenix", "Philadelphia", "McAllen",
      "Las Vegas", "Seattle"
    ), collapse = "|"))
  )

# ── Color palette ──────────────────────────────────────────────────────
region_colors <- c(
  "Florida"   = "#c44536",
  "Sun Belt"  = "#d4730e",
  "West"      = "#1b6087",
  "Northeast" = "#555555",
  "Midwest"   = "#6a994e"
)

# ── Build the plot ─────────────────────────────────────────────────────
p <- ggplot(children_adults, aes(x = walk_children, y = rate)) +

  # Regression line (subtle gray)
  geom_smooth(method = "lm", se = FALSE, color = "#cccccc",
              linewidth = 1.2, linetype = "solid") +

  # Non-highlighted points (gray)
  geom_point(
    data = filter(children_adults, !highlight),
    color = "#c8c8c8", size = 2.8
  ) +

  # Highlighted points (colored by region)
  geom_point(
    data = filter(children_adults, highlight),
    aes(color = region), size = 3.2
  ) +

  # Labels for highlighted metros only
  geom_text_repel(
    data = filter(children_adults, highlight),
    aes(label = short_name, color = region),
    size = 3.2, fontface = "bold", family = "serif",
    box.padding = 0.5, point.padding = 0.3,
    segment.color = "#cccccc", segment.size = 0.3,
    max.overlaps = 20, seed = 42,
    show.legend = FALSE
  ) +

  # ── Annotation: Florida cluster ──
  annotate(
    "text", x = 0.14, y = 4.15,
    label = "Florida metros dominate\nthe most dangerous quadrant",
    family = "serif", fontface = "italic",
    size = 3.3, color = "#c44536", hjust = 0, lineheight = 0.9
  ) +
  annotate(
    "segment", x = 0.42, xend = 0.50, y = 4.10, yend = 3.75,
    color = "#c44536", linewidth = 0.4
  ) +

  # ── Annotation: Safe northern metros ──
  annotate(
    "text", x = 0.36, y = 0.55,
    label = "Northern metros have the lowest\nfatality rates for both groups",
    family = "serif", fontface = "italic",
    size = 3.1, color = "#6a994e", hjust = 0, lineheight = 0.9
  ) +
  annotate(
    "segment", x = 0.35, xend = 0.24, y = 0.62, yend = 0.78,
    color = "#6a994e", linewidth = 0.4
  ) +

  # ── Scales ──
  scale_color_manual(values = region_colors, guide = "none") +
  scale_x_continuous(
    expand = expansion(mult = c(0.02, 0.04))
  ) +
  scale_y_continuous(
    expand = expansion(mult = c(0.05, 0.05))
  ) +

  # ── Labels ──
  labs(
    title    = "Where Children Walk in Danger,\nEveryone Does",
    subtitle = str_wrap(paste(
      "Pedestrian fatality rates for children vs. the total population",
      "across the 30 largest U.S. metro areas, 2017–2022.",
      "Metros dangerous for child pedestrians tend to be dangerous",
      "for everyone — but some Sun Belt outliers break the pattern."
    ), width = 80),
    x = "Children pedestrian fatality rate (per 100,000 children) →",
    y = "Total pedestrian fatality rate (per 100,000) →",
    caption = "Source: FARS 2017–2022; ACS population estimates  |  Top 30 metro areas by population  |  Gray dots: unlabeled metros"
  ) +

  # ── NYT theme ──
  theme_minimal(base_family = "serif", base_size = 12) +
  theme(
    legend.position = "none",

    plot.title = element_text(
      face = "bold", size = 18, lineheight = 1.1,
      margin = margin(b = 4), color = "#1a1a1a"
    ),
    plot.subtitle = element_text(
      size = 10.5, color = "#666666", lineheight = 1.25,
      margin = margin(b = 14)
    ),
    plot.caption = element_text(
      size = 7.5, color = "#999999", hjust = 0,
      margin = margin(t = 12)
    ),

    axis.title.x = element_text(size = 10, color = "#333333", margin = margin(t = 8)),
    axis.title.y = element_text(size = 10, color = "#333333", margin = margin(r = 8)),
    axis.text = element_text(size = 9, color = "#555555"),
    axis.ticks = element_blank(),

    panel.grid.major = element_line(color = "#ececec", linewidth = 0.3),
    panel.grid.minor = element_blank(),

    plot.margin = margin(t = 20, r = 15, b = 10, l = 10),
    plot.title.position = "plot",
    plot.caption.position = "plot"
  )

# ── Add a small manual region legend in top-right ──────────────────────
# (Using annotation since we suppressed the ggplot legend)
legend_data <- tibble(
  region = names(region_colors),
  color = unname(region_colors),
  x = 0.68,
  y = seq(4.5, by = -0.15, length.out = 5)
)

p <- p +
  geom_point(data = legend_data, aes(x = x, y = y), color = legend_data$color, size = 2.5) +
  geom_text(data = legend_data, aes(x = x + 0.015, y = y, label = region),
            color = legend_data$color, hjust = 0, size = 3, family = "serif", fontface = "bold")
p

# ── Save ───────────────────────────────────────────────────────────────
ggsave("walking_fatality_nyt.png", plot = p, width = 10, height = 8, dpi = 300, bg = "white")
message("✓ Saved: walking_fatality_nyt.png")
