import pandas as pd
from openfisca_uk import CountryTaxBenefitSystem
from openfisca_core.simulation_builder import SimulationBuilder
from openfisca_uk.reforms.basic_income import bi_from_pa
from utilities.simulation import model
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

data = pd.read_csv('datasets/frs/frs.csv')
period = '2020-01'
baseline_model = model(period=period)
reform_model = model(bi_from_pa, period=period)
data['net_income'] = baseline_model.calculate('net_income', period) * 12
data['net_income_reformed'] = reform_model.calculate('net_income', period) * 12
data['total_income'] *= 12
plot = sns.scatterplot(data['total_income'], data['net_income'], alpha=0.5, s=2, edgecolor='none')
plot = sns.scatterplot(data['total_income'], data['net_income_reformed'], alpha=0.5, s=2, color='red', edgecolor='none')
plot = sns.scatterplot(data['total_income'], data['net_income_reformed'] - data['net_income'], alpha=0.5, s=2, color='grey', edgecolor='none')
plot.set(xlim=[0, 150000])
plot.set(ylim=[0, 150000])
plt.legend(labels=['baseline', 'reform', 'difference'])
plot.set_title('Change in net income with (+ UBI, - PA) reform')
plt.show()