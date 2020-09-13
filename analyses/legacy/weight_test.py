import numpy as np
from utilities.simulation import model

simulation = model(data_dir="inputs")
period = "2020-08"

earnings = simulation.calculate("employee_earnings", period) * 52
person_weights = simulation.calculate("adult_weight", period)
mean_income = np.average(earnings)
mean_income_adj = np.average(earnings, weights=person_weights * (earnings > 0)) # Remove children and unemployed as well as applying weights

# PASS: £29k is the correct average yearly salary across all employees