import seaborn as sns

def set_plot_style():
    sns.set_theme(
        style="whitegrid",
        palette="muted",
        font_scale=1.3,   # Larger fonts
        rc={
            "grid.linewidth": 0.5,   # Thinner gridlines
            "figure.figsize": (10, 6),  # Set default figure size (width, height) in inches
            "axes.titlesize": 16,  # Larger title
            "axes.labelsize": 14,  # Larger axis labels
            "xtick.labelsize": 12,  # Bigger tick labels
            "ytick.labelsize": 12
        }
    )