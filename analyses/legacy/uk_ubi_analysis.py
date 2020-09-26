from utilities.simulation import model
from openfisca_uk.reforms.basic_income.simple_reform import simple_bi_reform
import numpy as np
import pandas as pd
from rdbl import num, gbp
import microdf as mdf
from matplotlib import pyplot as plt

baseline = model(data_dir="inputs")
reformed = model(simple_bi_reform, data_dir="inputs")
period = "2020-09-12"

base_family_df = pd.DataFrame()
base_family_df["family_net_income"] = (
    baseline.calculate("family_net_income", period) * 52
)
base_family_df["family_weight"] = baseline.calculate("family_weight", period)
base_family_df["is_lone_parent"] = baseline.calculate("is_lone_parent", period)
base_adult_df = pd.DataFrame()
base_adult_df["effective_tax_rate"] = baseline.calculate(
    "effective_tax_rate", period
)
base_adult_df["adult_weight"] = baseline.calculate("adult_weight", period)

reform_family_df = pd.DataFrame()
reform_family_df["family_net_income"] = (
    reformed.calculate("family_net_income", period) * 52
)
reform_family_df["family_weight"] = reformed.calculate("family_weight", period)
reform_family_df["is_lone_parent"] = reformed.calculate(
    "is_lone_parent", period
)
reform_adult_df = pd.DataFrame()
reform_adult_df["effective_tax_rate"] = reformed.calculate(
    "effective_tax_rate", period
)
reform_adult_df["adult_weight"] = reformed.calculate("adult_weight", period)

gini_baseline = mdf.gini(
    base_family_df, "family_net_income", w="family_weight"
)
gini_reform = mdf.gini(
    reform_family_df, "family_net_income", w="family_weight"
)
difference = (gini_reform - gini_baseline) / gini_baseline
print(f"Gini reduction: {difference * 100}%")

mdf.quantile_chg_plot(
    df1=base_family_df,
    df2=reform_family_df,
    col1="family_net_income",
    col2="family_net_income",
    w1="family_weight",
    w2="family_weight",
)
plt.show()
