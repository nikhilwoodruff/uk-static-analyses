import numpy as np
import pandas as pd
from utilities.simulation import model
from utilities.visualisation import banded_lineplot
import seaborn as sns
from matplotlib import pyplot as plt
from tqdm import tqdm

test_months = ["2017-09", "2018-10", "2019-07", "2020-08"]
tax_amounts = pd.DataFrame()
data = pd.read_csv("datasets/frs/frs.csv")
colors = iter(sns.color_palette("OrRd", len(test_months)))

for month in tqdm(test_months, desc="Calcuating net incomes"):
    system = model(period=month)
    tax_amounts[month] = system.calculate("net_income", month)
    plot = banded_lineplot(
        data["total_income"],
        tax_amounts[month],
        color=next(colors),
        bands=False,
    )

plot.set(xlim=[0, 12500])
plot.set(ylim=[0, 12500])
plt.legend(labels=test_months)
plot.set_title("NI tax due by income")
plt.show()
