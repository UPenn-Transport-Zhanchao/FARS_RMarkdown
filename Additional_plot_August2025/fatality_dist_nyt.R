# ── NYT-Style Strip/Dot Plot for Fatality Rate Distribution ───────────
# Drop this in after your existing data prep.
# Assumes `msa` data frame with columns: rate_overall, cbsa_name (or similar)

library(tidyverse)

# ── Prep ───────────────────────────────────────────────────────────────
mean_rate <- mean(msa$rate_overall, na.rm = TRUE)
sd_rate   <- sd(msa$rate_overall, na.rm = TRUE)

# Create short names and classify zones
msa_plot <- msa %>%
  mutate(
    short_name = str_extract(name, "^[^-,]+"),
    zone = case_when(
      rate_overall <= mean_rate - sd_rate ~ "below",
      rate_overall >= mean_rate + sd_rate ~ "above",
      TRUE ~ "middle"
    )
  )

# Define which MSAs to label — adjust to your story
highlight_names <- c(
  "Minneapolis", "Seattle", "New York", "San Francisco", "Chicago",  # safe end
  "Philadelphia",                                                      # middle
  "Houston", "Phoenix", "Jacksonville",                                # high
  "Tampa", "Bakersfield", "Fresno"                                     # most dangerous
)

msa_plot <- msa_plot %>%
  mutate(
    highlight = str_detect(short_name, paste(highlight_names, collapse = "|"))
  )

zone_colors <- c("below" = "#1b6087", "middle" = "#b0b0b0", "above" = "#c44536")

# Random y-jitter for strip layout
set.seed(42)
msa_plot$y_pos <- runif(nrow(msa_plot), 0.25, 0.55)

# ── Build the plot ─────────────────────────────────────────────────────
p <- ggplot(msa_plot, aes(x = rate_overall, y = y_pos)) +

  # Shaded zones
  annotate("rect",
    xmin = -Inf, xmax = mean_rate - sd_rate,
    ymin = -Inf, ymax = Inf,
    fill = "#e8f0f6", alpha = 0.5
  ) +
  annotate("rect",
    xmin = mean_rate + sd_rate, xmax = Inf,
    ymin = -Inf, ymax = Inf,
    fill = "#fce8e6", alpha = 0.5
  ) +

  # Mean line
  geom_vline(xintercept = mean_rate, color = "#333333", linewidth = 0.5) +

  # SD boundaries (subtle)
  geom_vline(xintercept = mean_rate - sd_rate, color = "#cccccc",
             linewidth = 0.6, linetype = "dashed") +
  geom_vline(xintercept = mean_rate + sd_rate, color = "#cccccc",
             linewidth = 0.6, linetype = "dashed") +

  # Non-highlighted dots (gray, smaller)
  geom_point(
    data = filter(msa_plot, !highlight),
    aes(color = zone), size = 2.5, alpha = 0.5
  ) +

  # Highlighted dots (larger, vivid)
  geom_point(
    data = filter(msa_plot, highlight),
    aes(color = zone), size = 3.5
  ) +

  # Labels
  ggrepel::geom_text_repel(
    data = filter(msa_plot, highlight),
    aes(label = short_name, color = zone),
    size = 2.0, fontface = "bold", family = "serif",
    direction = "y", nudge_y = 0.1,
    segment.color = "#dddddd", segment.size = 0.2,
    box.padding = 0.3, show.legend = FALSE, seed = 42
  ) +

  # Zone labels
  annotate("text",
    x = mean_rate - sd_rate - 0.3, y = 0.75,
    label = "Safer than average", family = "serif", fontface = "italic",
    size = 3.2, color = "#1b6087", hjust = 1
  ) +
  annotate("text",
    x = mean_rate + sd_rate + 0.3, y = 0.75,
    label = "Most dangerous", family = "serif", fontface = "italic",
    size = 3.2, color = "#c44536", hjust = 0
  ) +

  # Mean label
  annotate("text",
    x = mean_rate, y = 0.82,
    label = paste0("Average\n", round(mean_rate, 1), " per 100k"),
    family = "serif", fontface = "bold", size = 3, color = "#333333",
    hjust = 0.5, lineheight = 0.9
  ) +

  # Bottom annotation: the spread
  annotate("text",
    x = mean_rate, y = -0.08,
    label = "The most dangerous metro has 3× the fatality rate of the safest",
    family = "serif", fontface = "italic", size = 3.2, color = "#555555"
  ) +
  annotate("segment",
    x = min(msa_plot$rate_overall) - 0.2, xend = max(msa_plot$rate_overall) + 0.2,
    y = -0.02, yend = -0.02,
    color = "#999999", linewidth = 0.4,
    arrow = arrow(ends = "both", length = unit(0.08, "cm"), type = "closed")
  ) +

  # Scales
  scale_color_manual(values = zone_colors, guide = "none") +
  scale_x_continuous(breaks = seq(4, 14, 1)) +
  scale_y_continuous(limits = c(-0.15, 0.9)) +
  coord_cartesian(clip = "off") +

  # Labels
  labs(
    title = "A Three-Fold Gap in Traffic Deaths\nAcross America's Largest Metros",
    subtitle = str_wrap(paste(
      "Overall traffic fatality rates per 100,000 across the 30 largest U.S. metro areas,",
      "2017–2022. Sun Belt and Florida metros cluster on the dangerous end,",
      "while northern and coastal cities are consistently safer."
    ), width = 85),
    x = "Total traffic fatality rate per 100,000 population →",
    y = NULL,
    caption = "Source: FARS 2017–2022; ACS population estimates  |  Top 30 metro areas by population"
  ) +

  # NYT theme
  theme_minimal(base_family = "serif", base_size = 12) +
  theme(
    legend.position = "none",

    plot.title = element_text(
      face = "bold", size = 17, lineheight = 1.1,
      margin = margin(b = 4), color = "#1a1a1a"
    ),
    plot.subtitle = element_text(
      size = 10, color = "#666666", lineheight = 1.25,
      margin = margin(b = 14)
    ),
    plot.caption = element_text(
      size = 7.5, color = "#999999", hjust = 0, margin = margin(t = 10)
    ),

    axis.title.x = element_text(size = 10, color = "#333333", margin = margin(t = 8)),
    axis.text.x = element_text(size = 9, color = "#555555"),
    axis.text.y = element_blank(),
    axis.ticks = element_blank(),

    panel.grid.major.x = element_blank(),
    panel.grid.major.y = element_blank(),
    panel.grid.minor = element_blank(),

    plot.margin = margin(t = 20, r = 15, b = 10, l = 10),
    plot.title.position = "plot",
    plot.caption.position = "plot"
  )
p
ggsave("fatality_distribution_v1.png", plot = p,
       width = 11, height = 5.5, dpi = 300, bg = "white")

