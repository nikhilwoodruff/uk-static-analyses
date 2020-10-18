from openfisca_uk.tools.simulation import model, entity_df
from plotly import express as px

benunit = entity_df(model(), entity="benunit")
benunit["effective_tax_rate"] = 1 - benunit["benunit_net_income"] / benunit["benunit_income"]
cols = ["benunit_net_income", "benunit_gross_income", "benunit_earnings", "benunit_income_tax", "benunit_NI", "working_tax_credit", "child_tax_credit", "universal_credit", "housing_benefit", "JSA_income", "benunit_pension_income", "benunit_state_pension", "younger_adult_age", "older_adult_age", "benunit_misc", "benunit_interest"]

px.scatter(data_frame=benunit, x="benunit_income", y="effective_tax_rate", hover_data=cols).show()