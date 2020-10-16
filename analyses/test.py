from openfisca_uk.tools.simulation import model, entity_df
from openfisca_uk.reforms.basic_income.reform_1 import reform_1
from plotly import express as px
import numpy as np


def calc(var):
    return sim.calculate(var, period)


sim = model()
period = "2020-09"

weight_array = {
    "adult": calc("adult_weight"),
    "benunit": calc("benunit_weight"),
    "household": calc("household_weight"),
}


def mean(var, weight):
    return np.average(var, weights=weight)


def median(var, weight):
    return np.median(np.repeat(var, weight.astype(np.int32)))

df = entity_df(sim, entity="household")
df_p = entity_df(sim, entity="person")
df_p["size"] = df_p["adult_weight"] / 10000

income = df["equiv_household_net_income_ahc"]
show_columns = [
    "employee_earnings",
    "self_employed_earnings",
    "pension_income",
    "state_pension",
    "misc_income",
    "interest",
    "maintenance_income",
    "income_tax",
    "NI",
    "capital_gains_tax",
    "maintenance_expense",
    "student_loan_repayments",
    "deductions",
]
# px.scatter(data_frame=df_p, x="net_income", y="actual_net_income", hover_data=show_columns, size="size").show()
# px.histogram(df_p["net_income"] - df_p["actual_net_income"], nbins=1000).show()
median_household_income_bhc = median(
    calc("equiv_household_net_income_bhc"),
    calc("household_weight") * calc("people_in_household"),
)
median_household_income_ahc = median(
    calc("equiv_household_net_income_ahc"),
    calc("household_weight") * calc("people_in_household"),
)
poverty_bhc = mean(
    calc("in_poverty_bhc"),
    calc("household_weight") * calc("people_in_household"),
)
poverty_ahc = mean(
    calc("in_poverty_ahc"),
    calc("household_weight") * calc("people_in_household"),
)
child_poverty_bhc = mean(
    calc("in_poverty_bhc"),
    calc("household_weight") * calc("children_in_household"),
)
child_poverty_ahc = mean(
    calc("in_poverty_ahc"),
    calc("household_weight") * calc("children_in_household"),
)
print(f"Median household income BHC: {median_household_income_bhc}")
print(f"Median household income AHC: {median_household_income_ahc}")
print(f"Individual poverty BHC: {poverty_bhc:02}, AHC: {poverty_ahc:02}")
print(
    f"Child poverty BHC: {child_poverty_bhc:02}, AHC: {child_poverty_ahc:02}"
)
