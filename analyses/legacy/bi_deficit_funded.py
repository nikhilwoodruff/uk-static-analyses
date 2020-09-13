from utilities.simulation import model
from openfisca_uk.reforms.basic_income import basic_income_reform
import numpy as np
from rdbl import gbp

sim = model(data_dir="inputs")
sim_reformed = model(basic_income_reform, data_dir="inputs")
period = "2020-09-01"
gain = sim_reformed.calculate('family_basic_income', period)
family_weights = sim.calculate('family_weight', period)
weighted = gain * family_weights
cost_per_year = np.sum(weighted) * 52
print(f"Gross cost: {gbp(cost_per_year)}")

gain = sim_reformed.calculate('family_net_income', period) - sim.calculate('family_net_income', period)
weighted = gain * family_weights
net_cost_per_year = np.sum(weighted) * 52
print(f"Net cost: {gbp(net_cost_per_year)}")

# £260bn per year following Compass report amounts
# Their gross cost is ~£268bn

benefits = [
    "child_working_tax_credit_combined",
    "child_benefit",
    "income_support",
    "housing_benefit_actual",
    "contributory_JSA",
    "income_JSA",
    "benefit_cap_reduction"
]

total_saved = 0

for benefit in benefits:
    amount_normal = sim.calculate(benefit, period)
    amount_reformed = sim_reformed.calculate(benefit, period)
    difference = amount_reformed - amount_normal
    average_difference = np.average(difference, weights=family_weights) * 52
    amount_saved = np.sum(difference * family_weights) * 52
    total_saved += amount_saved
    print(f"{benefit}: average difference per year={gbp(average_difference)}, total difference per year={gbp(amount_saved)}")

print(f"Total saved in benefits: {gbp(total_saved)}")

# Total saved is £10bn
# Compass report finds £17bn