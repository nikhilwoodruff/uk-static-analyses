from openfisca_uk.tools.simulation import model, entity_df
from openfisca_uk.reforms.basic_income.reform_1 import reform_1
from openfisca_uk.reforms.basic_income.reform_2 import reform_2
from openfisca_uk.reforms.basic_income.reform_3 import reform_3
from openfisca_uk.reforms.basic_income.reform_4 import reform_4
from openfisca_uk.reforms.marginal_tax_rates import small_earnings_increase
from plotly import express as px
import pandas as pd
import numpy as np

for reform in [reform_1]:
    x = entity_df(model(), entity="benunit")
    y = entity_df(model(small_earnings_increase), entity="benunit")
    x["inc"] = x["benunit_income"]
    x["MTR"] = 1 - (y["benunit_net_income"] - x["benunit_net_income"]) / y["benunit_taxed_means_tested_bonus"]
    cols = ["benunit_housing_costs", "benunit_housing_benefit_reported", "benunit_post_tax_income", "benunit_net_income", "benunit_gross_income", "benunit_earnings", "benunit_income_tax", "benunit_NI", "working_tax_credit", "child_tax_credit", "universal_credit", "housing_benefit", "JSA_income", "income_support", "pension_credit", "benunit_pension_income", "benunit_state_pension", "younger_adult_age", "older_adult_age", "benunit_misc", "benunit_interest"]
    x["ETR"] = np.clip(np.where(x["benunit_income"] > 0, 1 - (x["benunit_net_income"] / x["benunit_income"]), 0), -2, 2)
    x["active"] = x["benunit_earnings"] + x["benunit_state_pension"] + x["benunit_pension_income"] > 0
    px.scatter(data_frame=x, x="inc", y="MTR", hover_data=cols, color="ETR").show()