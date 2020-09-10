from utilities.simulation import model
from openfisca_uk.reforms.basic_income.simple_reform import simple_bi_reform
import numpy as np
from ballpark import business
from matplotlib import pyplot as plt

baseline = model(data_dir="inputs")
reformed = model(simple_bi_reform, data_dir="inputs")
period = "2020-09-10"

family_weights = baseline.calculate("family_weight", period)
adult_weights = baseline.calculate("adult_weight", period)
net_cost = reformed.calculate("family_net_income", period) - baseline.calculate("family_net_income", period)
total_net_cost = (net_cost * family_weights).sum() * 52
print(business(total_net_cost))

ubi_cost = (reformed.calculate("family_basic_income", period) * family_weights).sum() * 52

diff_vars_adult = [
    "income_tax",
    "NI",
]

diff_vars_family = [
    "child_benefit",
    "working_tax_credit",
    "child_tax_credit",
    "contributory_JSA",
    "income_JSA",
]

for var in diff_vars_adult:
    diff = ((reformed.calculate(var, period) - baseline.calculate(var, period)) * adult_weights).sum() * 52
    print(f"{var}:{business(diff)}")

for var in diff_vars_family:
    diff = ((reformed.calculate(var, period) - baseline.calculate(var, period)) * family_weights).sum() * 52
    print(f"{var}:{business(diff)}")