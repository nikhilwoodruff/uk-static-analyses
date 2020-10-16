from openfisca_uk.tools.simulation import model, entity_df
import numpy as np
from rdbl import gbp

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


def print_errors(var1, var2, weight):
    error = var2 - var1
    abs_error = np.abs(var2 - var1)
    print(f"Average error: {np.average(error, weights=weight)}")
    print(f"Average absolute error: {np.average(abs_error, weights=weight)}")
    print(
        f"Average absolute error among claimants: {np.average(abs_error[var1 > 0], weights=weight[var1 > 0])}"
    )
    print(
        f"Total reported spending per year: {gbp(np.sum(var1 * weight) * 52)}, total simulated spending per year: {gbp(np.sum(var2 * weight) * 52)}"
    )

a = calc("adult_weight")
h = calc("household_weight")
b = calc("benunit_weight")

print("Winter Fuel Allowance:")

reported = calc("household_WFA_reported")
simulated = calc("winter_fuel_allowance")
print_errors(reported, simulated, h)

print("JSA (contribution-based):")

reported = calc("JSA_contrib_reported")
simulated = calc("JSA_contrib")
print_errors(reported, simulated, a)

print("JSA (income-based):")

reported = calc("benunit_JSA_income_reported")
simulated = calc("JSA_income")
print_errors(reported, simulated, b)

print("Income Support:")

reported = calc("benunit_IS_reported")
simulated = calc("income_support")
print_errors(reported, simulated, b)

print("Working Tax Credit:")

reported = calc("benunit_WTC_reported")
simulated = calc("working_tax_credit")
print_errors(reported, simulated, b)

print("Child Tax Credit:")

reported = calc("benunit_CTC_reported")
simulated = calc("child_tax_credit")
print_errors(reported, simulated, b)