from openfisca_uk.tools.simulation import model, entity_df
from openfisca_uk.reforms.basic_income.reform_3 import reform_3
import numpy as np
import pandas as pd
from plotly import express as px

baseline = model()
period = "2020-10-15"
reform = model(reform_3)

df = pd.DataFrame()
df["earned_income"] = (
    baseline.calculate("household_earned_income", period) * 52
)
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
    x="earned_income",
    y="net_gain",
    hover_data=hover_cols,
    size="weight",
    color="num_children",
).show()
px.histogram(df["net_gain"]).show()
