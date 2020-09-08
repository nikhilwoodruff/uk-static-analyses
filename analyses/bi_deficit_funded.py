from utilities.simulation import model
from openfisca_uk.reforms.basic_income import basic_income_reform
import numpy as np

sim = model(data_dir="inputs")
sim_reformed = model(basic_income_reform, data_dir="inputs")
period = "2020-09-01"
gain = sim_reformed.calculate('family_basic_income', period)
weighted = gain * sim.calculate('family_weight', period)
cost_per_year = np.sum(weighted) * 52
print(cost_per_year)

# £260bn per year following Compass report amounts
# Their gross cost is ~£260bn