from openfisca_uk.tools.simulation import model, entity_df, calc_mtr
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
    period = "2020-10"
    family_weights = baseline.calculate("benunit_weight", period)
    adult_weights = baseline.calculate("adult_weight", period)
    household_weights = baseline.calculate("household_weight", period)
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
    senior_poverty_ahc_reduction = percent_reduction(
        poverty_rate(baseline, "seniors_in_household"),
        poverty_rate(reformed, "seniors_in_household"),
    )
    print("Poverty statistics:")
    print(f"    AHC poverty change: {num(poverty_ahc_reduction * 100)}%")
    print(
        f"    AHC adult poverty change: {num(adult_poverty_ahc_reduction * 100)}%"
    )
    print(
        f"    AHC child poverty change: {num(child_poverty_ahc_reduction * 100)}%"
    )
    print(
        f"    AHC senior poverty change: {num(senior_poverty_ahc_reduction * 100)}%"
    )
    diff_vars_adult = ["state_pension", "JSA_contrib"]
    diff_vars_family = [
        "child_benefit",
        "income_support",
        "working_tax_credit",
        "child_tax_credit",
        "benunit_income_tax",
        "benunit_NI",
        "pension_credit",
        "JSA_income",
        "universal_credit",
    ]
    print("MTR:")
    baseline_MTR = calc_mtr(entity="household")
    reform_MTR = calc_mtr(reform, entity="household")
    average_baseline_MTR = np.average(baseline_MTR, weights=household_weights)
    average_reform_MTR = np.average(reform_MTR, weights=household_weights)
    on_benefits = baseline.calculate("household_receives_means_tested_benefits", period).astype(bool)
    average_baseline_ben_MTR = np.average(
        baseline_MTR[on_benefits], weights=household_weights[on_benefits]
    )
    average_reform_ben_MTR = np.average(
        reform_MTR[on_benefits], weights=household_weights[on_benefits]
    )
    print(f"    Average baseline MTR: {average_baseline_MTR}")
    print(f"    Average reform MTR: {average_reform_MTR}")
    print(
        f"    Average baseline MTR for households on benefits: {average_baseline_ben_MTR}"
    )
    print(
        f"    Average reform MTR for households on benefits: {average_reform_ben_MTR}"
    )
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
    baseline_gini = mdf.gini(household_net_ahc, "baseline", w="w")
    reform_gini = mdf.gini(household_net_ahc, "reform", w="w")
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
