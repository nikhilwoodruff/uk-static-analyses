from openfisca_uk.tools.simulation import model, entity_df
from openfisca_uk.reforms.marginal_tax_rates import small_earnings_increase
from plotly import express as px

x = entity_df(model(), entity="household")
y = entity_df(model(small_earnings_increase), entity="household")

x["MTR"] = -(y["household_net_income_bhc"] - x["household_net_income_bhc"]) / y["household_taxed_means_tested_bonus"]
x = x.set_index("household_net_income_bhc")
x["average_MTR"] = x["MTR"].rolling(1).mean()
px.scatter(data_frame=x, x="household_net_income_ahc", y="average_MTR", color="children_in_household").show()