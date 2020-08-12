import pandas
from openfisca_uk import CountryTaxBenefitSystem
from openfisca_core.simulation_builder import SimulationBuilder
from openfisca_uk.reforms.basic_income import bi_from_pa
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

def model(*reforms, period='2020-01'):
    system = CountryTaxBenefitSystem()
    builder = SimulationBuilder()
    builder.create_entities(system)
    data = pandas.read_csv('datasets/frs/frs.csv')
    builder.declare_person_entity('person', np.array(data['person_id']))
    for reform in reforms:
        system = reform(system)
    model = builder.build(system)
    for column in data.columns[1:]:
        model.set_input(column, period, np.array(data[column]))
    return model