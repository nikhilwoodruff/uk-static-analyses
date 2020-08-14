import pandas
from openfisca_uk import CountryTaxBenefitSystem
from openfisca_core.simulation_builder import SimulationBuilder
from openfisca_core.model_api import *
from openfisca_uk.entities import *
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

def model(*reforms, data=None, period='2020-01'):
    system = CountryTaxBenefitSystem()
    builder = SimulationBuilder()
    builder.create_entities(system)
    if data is None:
        data = pandas.read_csv('datasets/frs/frs.csv')
    builder.declare_person_entity('person', np.array(data['person_id']))
    households = builder.declare_entity('household', np.unique(np.array(data['household_id'])))
    families = builder.declare_entity('family', np.unique(np.array(data['family_id'])))
    roles = np.array(['adult'] * len(data['household_id']))
    builder.join_with_persons(households, np.array(data['household_id']), roles)
    for reform in reforms:
        system = reform(system)
    model = builder.build(system)
    for column in data.columns[3:]:
        model.set_input(column, period, np.array(data[column]))
    return model