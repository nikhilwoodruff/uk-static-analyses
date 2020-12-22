from openfisca_uk import PopulationSim
import numpy as np


sim = PopulationSim()

poverty_bhc = np.average(
    sim.calc("in_poverty_bhc", period="week:2020-01-06"),
    weights=sim.calc("household_weight") * sim.calc("people_in_household"),
)
poverty_ahc = np.average(
    sim.calc("in_poverty_ahc", period="week:2020-01-06"),
    weights=sim.calc("household_weight") * sim.calc("people_in_household"),
)
child_poverty_bhc = np.average(
    sim.calc("in_poverty_bhc", period="week:2020-01-06"),
    weights=sim.calc("household_weight") * sim.calc("children_in_household"),
)
child_poverty_ahc = np.average(
    sim.calc("in_poverty_ahc", period="week:2020-01-06"),
    weights=sim.calc("household_weight") * sim.calc("children_in_household"),
)
print(f"Individual poverty BHC: {poverty_bhc:02}, AHC: {poverty_ahc:02}")
print(
    f"Child poverty BHC: {child_poverty_bhc:02}, AHC: {child_poverty_ahc:02}"
)