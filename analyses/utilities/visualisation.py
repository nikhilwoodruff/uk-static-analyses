from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


def banded_lineplot(
    x,
    y,
    num_bins=100,
    color="blue",
    bands=True,
    scatter=False,
    clip_percentiles=[1, 99],
):
    lower, upper = np.percentile(x, clip_percentiles[0]), np.percentile(
        x, clip_percentiles[1]
    )
    y = y[(x > lower) * (x < upper)]
    x = x[(x > lower) * (x < upper)]
    bins = np.linspace(lower, upper, num=num_bins + 1)
    contents = np.array(
        [
            y[np.logical_and(x < bins[i + 1], x >= bins[i])]
            for i in range(num_bins)
        ]
    )
    indices = [i for i in range(len(contents)) if len(contents[i]) > 0]
    x_quantized = bins[indices]
    y_quantized = contents[indices]
    p50 = np.array([np.percentile(t, 50) for t in y_quantized])
    plot = sns.lineplot(x_quantized, p50, ci=None, color=color)
    if not bands:
        return plot
    p5 = np.array([np.percentile(t, 5) for t in y_quantized])
    p33 = np.array([np.percentile(t, 33) for t in y_quantized])
    p67 = np.array([np.percentile(t, 67) for t in y_quantized])
    p95 = np.array([np.percentile(t, 95) for t in y_quantized])
    if scatter:
        sns.scatterplot(x, y, alpha=0.05, s=2, edgecolor="none", color=color)
    plot = sns.lineplot(x_quantized, p50, ci=None, color=color)
    plot.fill_between(x_quantized, p5, p33, alpha=0.2, color=color)
    plot.fill_between(x_quantized, p33, p67, alpha=0.4, color=color)
    plot.fill_between(x_quantized, p67, p95, alpha=0.2, color=color)
    return plot
