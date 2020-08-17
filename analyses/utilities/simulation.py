import pandas
from openfisca_uk import CountryTaxBenefitSystem
from openfisca_core.simulation_builder import SimulationBuilder
from openfisca_core.model_api import *
from openfisca_uk.entities import *
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

def model(*reforms, data=None, period='2020-01'):
    '''
    Create and populate a tax-benefit simulation model from OpenFisca.

    Arguments:
        reforms: any reforms to apply, in order.
        data: any data to use instead of the loaded Family Resources Survey.
        period: the period in which to enter all data (at the moment, all data is entered under this period).
    
    Returns:
        A Simulation object.
    '''
    system = CountryTaxBenefitSystem()
    for reform in reforms:
        system = reform(system) # apply each reform in order
    builder = SimulationBuilder()
    builder.create_entities(system) # create the entities (person, family, etc.)
    if data is None:
        data = pandas.read_csv('datasets/frs/frs.csv')
    builder.declare_person_entity('person', np.array(data['person_id'])) # assign ids
    households = builder.declare_entity('household', np.unique(np.array(data['household_id'])))
    families = builder.declare_entity('family', np.unique(np.array(data['family_id'])))
    roles = np.array(['adult'] * len(data['household_id'])) # for now, every member of a household is an adult
    builder.join_with_persons(households, np.array(data['household_id']), roles) # define person-house memberships
    model = builder.build(system)
    for column in data.columns[3:]:
        model.set_input(column, period, np.array(data[column])) # input data for income and benefit claims
    return model