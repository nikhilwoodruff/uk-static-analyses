from openfisca_uk.tools.simulation import model, entity_df
from openfisca_uk.reforms.basic_income.reform_4 import reform_4
import numpy as np
import pandas as pd
from plotly import express as px

baseline = model()
period = "2020-10-15"
reform = model(reform_4)

df = pd.DataFrame()
df["household_income"] = baseline.calculate("household_income", period) * 52
df["baseline_net_income"] = (
    baseline.calculate("household_net_income_bhc", period) * 52
)
df["reform_net_income"] = (
    reform.calculate("household_net_income_bhc", period) * 52
)
df["net_gain"] = df["reform_net_income"] - df["baseline_net_income"]
df["weight"] = baseline.calculate("household_weight", period) / 10000
df["num_children"] = baseline.calculate("children_in_household", period)

hover_cols = [
    "baseline_net_income",
    "reform_net_income",
    "reform_net_income",
    "net_gain",
]

px.scatter(
    data_frame=df,
    x="household_income",
    y="net_gain",
    hover_data=hover_cols,
    size="weight",
    color="num_children",
    opacity=0.1,
).show()
px.histogram(df["net_gain"]).show()
px.histogram(
    np.clip(baseline.calculate("household_net_income_ahc", period), 0, 1200)
).show()
