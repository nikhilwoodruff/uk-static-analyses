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


h = calc("household_weight")
b = calc("benunit_weight")

# WTC+CTC

print("Tax credits")
txcred = calc("working_tax_credit") + calc("child_tax_credit")
txcred_reported = calc("benunit_wtc_reported") + calc("benunit_ctc_reported")
print_errors(txcred_reported, txcred, b)

# Child Benefit

print("Child Benefit")
CB = calc("child_benefit")
CB_reported = calc("benunit_CB_reported")
print_errors(CB_reported, CB, b)
