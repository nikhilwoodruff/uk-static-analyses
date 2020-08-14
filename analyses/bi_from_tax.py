import pandas as pd
from openfisca_uk import CountryTaxBenefitSystem
from openfisca_core.simulation_builder import SimulationBuilder
from openfisca_core.model_api import *
from openfisca_uk.entities import *
from utilities.simulation import model
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from scipy.optimize import minimize, differential_evolution
from random import random

def reform_model(x, data, period):
    def tax(incomes, bands, rates):
        incomes_ = np.broadcast_to(incomes, (bands.shape[0] - 1, incomes.shape[0]))
        amounts_in_bands = np.clip(incomes_.transpose(), bands[:-1], bands[1:]) - bands[:-1]
        taxes = rates * amounts_in_bands
        total_taxes = taxes.sum(axis=1)
        return total_taxes

    class non_taxable_income(Variable):
        value_type = float
        entity = Person
        label = u'Total non-taxable income per month'
        definition_period = MONTH

        def formula(person, period, parameters):
            non_taxable_benefits = [
                'income_support',
                'housing_benefit',
                'child_benefit',
                'child_tax_credit',
                'working_tax_credit_childcare',
                'tax_free_childcare',
                'working_tax_credit'
            ]
            return sum(map(lambda benefit_name : person(benefit_name, period), non_taxable_benefits)) + x[0]

    class income_tax(Variable):
        value_type = float
        entity = Person
        label = u'Income tax paid per month'
        definition_period = MONTH

        def formula(person, period, parameters):
            estimated_yearly_income = person('taxable_income', period) * 12
            pa_null_band = np.array([100000, 125000])
            pa_null_rate = np.array([0.5])
            pa_discount = tax(estimated_yearly_income, pa_null_band, pa_null_rate)
            bands = np.array([12500, 50000, 150000, np.inf])
            rates = np.array([0.2, 0.4, 0.45 + x[1]])
            return tax(estimated_yearly_income + pa_discount, bands, rates) / 12
    
    class bi_and_flat_tax(Reform):
        def apply(self):
            self.update_variable(income_tax)
            self.update_variable(non_taxable_income)
    
    reformed_model = model(bi_and_flat_tax, data=data, period=period)
    return reformed_model

def cost(x, baseline_incomes, baseline_tax_revenue, data, period):
    reformed_model = reform_model(x, data, period)
    reformed_income = reformed_model.calculate('net_income', period) * 12
    reformed_tax_revenue = reformed_model.calculate('income_tax', period) * 12
    surplus = reformed_tax_revenue.sum() - baseline_tax_revenue.sum() - x[0] * reformed_tax_revenue.shape[0]
    poverty_income = np.percentile(baseline_incomes, 40)
    poverty_rate = (reformed_income < poverty_income).mean()
    # return -surplus
    return poverty_rate

data = pd.read_csv('datasets/frs/frs.csv')
period = '2020-01'
baseline_model = model(data=data, period=period)
initial_guess = np.array([0, 0])
baseline_incomes = baseline_model.calculate('net_income', period) * 12
baseline_tax = baseline_model.calculate('income_tax', period) * 12
poverty = np.percentile(baseline_incomes, 40)
solution = differential_evolution(cost, ((0, 10000), (-0.2, 0.2)), args=(baseline_incomes, baseline_tax, data, period))
print(solution.x, solution.fun)
'''
Optimizing for reducing:
    surplus: increase taxes as much as possible, and give the minimum UBI
    poverty_rate: taxes don't change (no incentive to) and give the maximum UBI
'''