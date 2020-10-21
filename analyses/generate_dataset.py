from openfisca_uk.tools.simulation import model
from openfisca_uk.reforms.basic_income.reform_1 import reform_1
from openfisca_uk.reforms.basic_income.reform_2 import reform_2
from openfisca_uk.reforms.basic_income.reform_3 import reform_3
from openfisca_uk.reforms.basic_income.reform_4 import reform_4
import numpy as np
import pandas as pd

household = pd.DataFrame()

basic_columns = [
    "household_weight",
    "people_in_household",
    "adults_in_household",
    "children_in_household",
]

reform_columns = [
    "household_net_income_bhc",
    "equiv_household_net_income_bhc",
    "household_net_income_ahc",
    "equiv_household_net_income_ahc",
    "in_poverty_bhc",
    "in_poverty_ahc",
]

reforms = [None, reform_1, reform_2, reform_3, reform_4]
reform_names = ["baseline", "reform_1", "reform_2", "reform_3", "reform_4"]

sim = model()
period = "2020-09"

for column in basic_columns:
    household[column] = sim.calculate(column, period)

for reform, name in zip(reforms, reform_names):
    if reform:
        sim = model(reform)
    for column in reform_columns:
        household[f"{name}_{column}"] = sim.calculate(column, period)

household *= 1

household.to_csv("analyses/household_results.csv", index=False)
