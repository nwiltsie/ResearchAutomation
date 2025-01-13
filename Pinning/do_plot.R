png(
    paste0("../", as.character(packageVersion("ggplot2")), ".png"),
    width = 1200,
    height = 800,
    res = 200
)

library(ggplot2)

# Create a simple dataset
data <- data.frame(
  x = 1:10,
  y1 = sin(1:10),
  y2 = cos(1:10)
)

# Create the plot
ggplot(data, aes(x)) +
  geom_line(aes(y = y1, color = "sin(x)"), linewidth = 8) +
  geom_line(aes(y = y2, color = "cos(x)"), linewidth = 8) +
  labs(
    title = "Line Plot Example",
    x = "X-axis",
    y = "Y-axis",
    color = "Function"
  ) +
  theme_minimal()
