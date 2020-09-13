import pandas as pd
from openfisca_uk import CountryTaxBenefitSystem
from openfisca_core.simulation_builder import SimulationBuilder
from openfisca_uk.reforms.basic_income import bi_from_pa
from utilities.simulation import model
from utilities.visualisation import banded_lineplot
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

