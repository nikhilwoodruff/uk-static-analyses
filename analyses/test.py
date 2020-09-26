from utilities.simulation import model
from plotly import express as px
import numpy as np

sim = model()
period = "2020-09"

def calc(var):
    return sim.calculate(var, period)

weight_array = {
    "adult": calc("adult_weight"),
    "benunit": calc("benunit_weight"),
    "household": calc("household_weight")
}

def mean(var, entity="adult"):
    return np.average(var, weights=weight_array[entity])

def median(var, entity="adult"):
    return np.median(np.repeat(var, weight_array[entity].astype(np.int32)))

def poverty_rate(cross_section_var, mode="ahc"):
    return np.sum(calc("in_poverty_" + mode) * calc(cross_section_var) * calc("household_weight")) / np.sum(calc(cross_section_var) * calc("household_weight"))

print("Benefit modelled vs. reported error check:")

for benefit in [
    "child_benefit",
    "child_tax_credit",
    "working_tax_credit",
    "income_support"
]:
    print(f'{benefit}: {mean(calc(benefit + "_reported") - calc(benefit), "benunit")}')

print("Poverty rates, before housing costs")
poverty = poverty_rate("people_in_household")
adult_poverty = poverty_rate("adults_in_household")
child_poverty = poverty_rate("children_in_household")
print(poverty, adult_poverty, child_poverty)