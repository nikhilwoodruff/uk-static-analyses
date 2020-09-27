from utilities.simulation import model, entity_df
from openfisca_uk.reforms.basic_income.reform_1 import reform_1
from openfisca_uk.reforms.basic_income.reform_2 import reform_2
from openfisca_uk.reforms.basic_income.reform_3 import reform_3
from openfisca_uk.reforms.basic_income.reform_4 import reform_4
import numpy as np
from rdbl import gbp, num
from matplotlib import pyplot as plt
import os
from argparse import ArgumentParser
import microdf as mdf
import pandas as pd


def percent_reduction(before, after):
    return (after - before) / before


def poverty_rate(sim, cross_section_var, mode="ahc", period="2020-09-10"):
    x = np.sum(
        sim.calculate("in_poverty_" + mode, period)
        * sim.calculate(cross_section_var, period)
        * sim.calculate("household_weight", period)
    )
    y = np.sum(
        sim.calculate(cross_section_var, period)
        * sim.calculate("household_weight", period)
    )
    z = sim.calculate("adults_in_household", period)
    return np.sum(
        sim.calculate("in_poverty_" + mode, period)
        * sim.calculate(cross_section_var, period)
        * sim.calculate("household_weight", period)
    ) / np.sum(
        sim.calculate(cross_section_var, period)
        * sim.calculate("household_weight", period)
    )


def evaluate_reform(reform):
    baseline = model()
    reformed = model(reform)
    period = "2020-09-10"
    family_weights = baseline.calculate("benunit_weight", period)
    adult_weights = baseline.calculate("adult_weight", period)
    net_gain = reformed.calculate(
        "benunit_net_income", period
    ) - baseline.calculate("benunit_net_income", period)
    gross_ubi_cost = (
        (reformed.calculate("benunit_basic_income", period)) * family_weights
    ).sum() * 52
    total_net_cost = (net_gain * family_weights).sum() * 52
    print("Total cost summary:")
    print(f"    Net cost of reform: {gbp(total_net_cost)}")
    print(f"    Gross cost of UBI: {gbp(gross_ubi_cost)}")
    poverty_ahc_reduction = percent_reduction(
        poverty_rate(baseline, "people_in_household"),
        poverty_rate(reformed, "people_in_household"),
    )
    adult_poverty_ahc_reduction = percent_reduction(
        poverty_rate(baseline, "adults_in_household"),
        poverty_rate(reformed, "adults_in_household"),
    )
    child_poverty_ahc_reduction = percent_reduction(
        poverty_rate(baseline, "children_in_household"),
        poverty_rate(reformed, "children_in_household"),
    )
    print("Poverty statistics:")
    print(f"    AHC poverty change: {num(poverty_ahc_reduction * 100)}%")
    print(
        f"    AHC adult poverty change: {num(adult_poverty_ahc_reduction * 100)}%"
    )
    print(
        f"    AHC child poverty change: {num(child_poverty_ahc_reduction * 100)}%"
    )
    diff_vars_adult = ["income_tax", "NI", "pension_income"]

    diff_vars_family = [
        "child_benefit",
        "working_tax_credit",
        "child_tax_credit",
        "income_support",
    ]

    print("Inequality:")
    household_net_ahc = pd.DataFrame()
    household_net_ahc["w"] = baseline.calculate(
        "household_weight", period
    ) * baseline.calculate("people_in_household", period)
    household_net_ahc["baseline"] = baseline.calculate(
        "equiv_household_net_income_ahc", period
    )
    household_net_ahc["reform"] = reformed.calculate(
        "equiv_household_net_income_ahc", period
    )
    baseline_gini = mdf.gini(household_net_ahc, "baseline")
    reform_gini = mdf.gini(household_net_ahc, "reform")
    gini_reduction = percent_reduction(baseline_gini, reform_gini)
    print(f"    Gini coefficient reduction: {num(gini_reduction * 100)}%")

    print("Rise in amounts per year across all:")
    print("    individuals:")
    for var in diff_vars_adult:
        diff = (
            (reformed.calculate(var, period) - baseline.calculate(var, period))
            * adult_weights
        ).sum() * 52
        print(f"        {var}: {gbp(diff)}")
    print("    families:")
    for var in diff_vars_family:
        diff = (
            (reformed.calculate(var, period) - baseline.calculate(var, period))
            * family_weights
        ).sum() * 52
        print(f"        {var}: {gbp(diff)}")


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Tool to evaluate key figures from each reform simulation"
    )
    parser.add_argument(
        "--reform", help="The name of a specific reform to evaluate"
    )
    args = parser.parse_args()
    reform_list = [reform_1, reform_2, reform_3, reform_4]
    reform_names = {"1": reform_1, "2": reform_2, "3": reform_3, "4": reform_4}
    if args.reform is not None:
        evaluate_reform(reform_names[args.reform])
    else:
        i = 1
        for reform in reform_list:
            print(f"---SIMULATION {i}---")
            i += 1
            evaluate_reform(reform)
