from utilities.simulation import model
from openfisca_uk.reforms.basic_income.simple_reform import simple_bi_reform
import numpy as np
from ballpark import business
from matplotlib import pyplot as plt

baseline = model(data_dir="inputs")
reformed = model(simple_bi_reform, data_dir="inputs")
period = "2020-09-10"

poverty_in_baseline = baseline.calculate("family_total_income", period) < 340
family_weights = baseline.calculate("family_weight", period)
adult_weights = baseline.calculate("adult_weight", period)
net_cost = reformed.calculate("family_net_income", period) - baseline.calculate("family_net_income", period)
total_net_cost = (net_cost * family_weights).sum() * 52

net_among_poverty = np.average(net_cost, weights=poverty_in_baseline*family_weights)
net_among_all = np.average(net_cost, weights=family_weights)

print(f"Net cost: {business(total_net_cost)}")

ubi_cost = (reformed.calculate("family_basic_income", period) * family_weights).sum() * 52
print(f"Gross UBI cost: {business(ubi_cost)}")

diff_vars_adult = [
    "income_tax",
    "NI"
]

diff_vars_family = [
    "child_benefit",
    "working_tax_credit",
    "child_tax_credit",
    "contributory_JSA",
    "income_JSA",
    "income_support"
]

for var in diff_vars_adult:
    diff = ((reformed.calculate(var, period) - baseline.calculate(var, period)) * adult_weights).sum() * 52
    print(f"{var}:{business(diff)}")

for var in diff_vars_family:
    diff = ((reformed.calculate(var, period) - baseline.calculate(var, period)) * family_weights).sum() * 52
    print(f"{var}:{business(diff)}")
