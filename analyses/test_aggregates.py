from openfisca_uk.tools.simulation import model, entity_df
import numpy as np
from rdbl import gbp, num

period = "2020-10-12"
sim = model(period=period)
benunits = sim.calculate("benunit_weight", period)


def calc(var):
    return sim.calculate(var, period)


def mean(var, weight):
    return np.average(var, weights=weight)


def median(var, weight):
    return np.median(np.repeat(var, weight.astype(np.int32)))


def total(var, weight="adult"):
    return np.sum(calc(var) * calc(weight + "_weight")) * 52


a = calc("adult_weight")
h = calc("household_weight")
b = calc("benunit_weight")

person_vars = ["JSA_contrib", "income_tax", "state_pension"]
benunit_vars = [
    "JSA_income",
    "income_support",
    "pension_credit",
    "working_tax_credit",
    "child_tax_credit",
    "housing_benefit",
    "child_benefit",
    "universal_credit",
]

for var in person_vars:
    print(
        f"{var}:\n  total expenditure: {gbp(total(var))}\n  total recipients: {num(np.sum((calc(var) > 0) * a))}"
    )

for var in benunit_vars:
    print(
        f"{var}:\n  total expenditure: {gbp(total(var, weight='benunit'))}\n  total recipients: {num(np.sum((calc(var) > 0) * b))}"
    )
