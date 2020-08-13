from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def points_to_line(x, y, num_bins=100):
    lower, upper = x.min(), x.max()
    bin_size = (upper - lower) / num_bins

    # TODO: Add function to transform coordinates to percentile lines using bins.