import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from utilities.simulation import model
from utilities.visualisation import banded_lineplot
import seaborn as sns

simulation = model(data_dir="inputs")
period = "2020-08"

child_benefit = simulation.calculate('child_benefit', period)
child_benefit_actual = simulation.calculate('child_benefit_actual', period)
cb_error = np.abs(child_benefit - child_benefit_actual)
cb_average_error = cb_error.mean()

JSA = simulation.calculate('JSA', period)
JSA_actual = simulation.calculate('JSA_actual', period)
JSA_error = np.abs(JSA - JSA_actual)
JSA_average_error = JSA_error.mean()

income_support = simulation.calculate('income_support', period)
income_support_actual = simulation.calculate('income_support_actual', period)
is_error = np.abs(income_support - income_support_actual)
is_average_error = is_error.mean()


income = simulation.calculate('income', period) * 52
etr = simulation.calculate('effective_tax_rate', period)
banded_lineplot(income, etr)
plt.show()