from openfisca_core.simulation_builder import SimulationBuilder
from openfisca_uk import CountryTaxBenefitSystem
from openfisca_uk.reforms.basic_income.reform_3 import reform_3

TEST_CASE = {
    "people": {
        "pensioner1": {
            "pension_income": {"ETERNITY": 200},
            "state_pension": {"ETERNITY": 175},
            "pension_credit_reported": {"ETERNITY": 1}
        }, 
        "pensioner2": {
            "pension_income": {"ETERNITY": 150},
            "state_pension": {"ETERNITY": 175}
        }
    },
    "benunits": {
        "b1": {
            "adults": ["pensioner1", "pensioner2"]
        }
    },
    "households": {
        "h1": {
            "adults": ["pensioner1", "pensioner2"]
        }
    },
}

system = CountryTaxBenefitSystem()
simulation_builder = SimulationBuilder()
baseline = simulation_builder.build_from_dict(system, TEST_CASE)
reform_system = reform_3(system)
reform = simulation_builder.build_from_dict(reform_system, TEST_CASE)

variables = [
    "household_gross_income",
    "household_net_income_bhc",
    "gross_income",
    "net_income",
    "income_tax",
    "NI",
    "capital_gains_tax",
    "working_tax_credit",
    "child_tax_credit",
    "child_benefit",
    "pension_credit_MG",
    "pension_credit_SC",
    "pension_credit_GC"
]

for model, name in zip([baseline, reform], ["baseline", "reform"]):
    print(f"{name}:")
    for var in variables:
        print(f"    {var}: {model.calculate(var, '2020-10-17')}")