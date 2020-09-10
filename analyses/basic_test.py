import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from utilities.simulation import model
from utilities.visualisation import banded_lineplot
import seaborn as sns
from tqdm import tqdm
from ballpark import business

simulation = model(data_dir="inputs")
period = "2020-08"

full_time_workers = (simulation.calculate("hours_worked", period) >= 30)
part_time_workers = (simulation.calculate("hours_worked", period) > 0) * (simulation.calculate("hours_worked", period) < 30)
survey_weights = simulation.calculate("adult_weight", period) * (simulation.calculate("employee_earnings", period) > 0) * (simulation.calculate("self_employed_earnings", period) == 0)

ft = survey_weights*full_time_workers
pt = survey_weights*part_time_workers

salary = simulation.calculate("employee_earnings", period)
income = simulation.calculate("income", period)

mean_ft_salary = np.average(salary, weights=ft) * 52
mean_pt_salary = np.average(salary, weights=pt) * 52

print(f"Mean full-time salary: {business(mean_ft_salary)}")
print(f"Mean part-time salary: {business(mean_pt_salary)}")

income_tax = simulation.calculate("income_tax", period)
NI = simulation.calculate("NI", period)

etr = np.where(income == 0, 0, (income_tax + NI) / income)

mean_etr_ft = np.average(etr, weights=ft)
mean_etr_pt = np.average(etr, weights=pt)

print(f"Mean full-time ETR: {mean_etr_ft}")
print(f"Mean part-time ETR: {mean_etr_pt}")