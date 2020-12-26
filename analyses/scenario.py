import logging
import pandas as pd

from openfisca_core import periods
from openfisca_survey_manager.scenarios import AbstractSurveyScenario
from openfisca_uk import CountryTaxBenefitSystem as UKTaxBenefitSystem


csv_path_by_entity = {
    "benunit": "~/data/uk/randomised_benunit.csv",
    "household": "~/data/uk/randomised_household.csv",
    "person": "~/data/uk/randomised_person.csv",
    }


log = logging.getLogger(__name__)


class UKSurveyScenario(AbstractSurveyScenario):
    def __init__(self, tax_benefit_system = None, baseline_tax_benefit_system = None,
            data = None, year = None):
        super(UKSurveyScenario, self).__init__()
        if tax_benefit_system is None:
            tax_benefit_system = UKTaxBenefitSystem()
        self.set_tax_benefit_systems(
            tax_benefit_system = tax_benefit_system,
            baseline_tax_benefit_system = baseline_tax_benefit_system,
            )
        self.year = year
        self.role_variable_by_entity_key = {
            "benunit": "role",
            "household": "role",
            }
        if data is None:
            return

        input_data_frame_by_entity_by_period = data['input_data_frame_by_entity_by_period']
        for period, input_data_frame_by_entity in input_data_frame_by_entity_by_period.items():
            log.info(f"Initialising using period: {period}")
            for entity, df in input_data_frame_by_entity.items():
                print(entity)
                print(df.columns)

            entity_variables = [set(df.columns) for df in input_data_frame_by_entity.values()]

        variables_from_data = set.union(*entity_variables)


        print(variables_from_data)
        self.used_as_input_variables = list(
            set(tax_benefit_system.variables.keys()).intersection(
                set(variables_from_data)
                )
            )
        unused_variables = set([
            "housing_costs",
            "total_benefits",
            ])
        self.used_as_input_variables = set(self.used_as_input_variables).difference(unused_variables)
        self.init_from_data(data = data)


def build_entity_dataframe(year):
    input_data_frame_by_entity = dict(
        (entity, pd.read_csv(csv_path))
        for entity, csv_path in csv_path_by_entity.items()
        )
    household = input_data_frame_by_entity["household"]
    person = input_data_frame_by_entity["person"]

    person["role"] = person["role"].replace({"adult": 0, "child": 1})
    household.rename(
        columns = {
            "rent": "weekly_rent",
            },
        inplace = True
        )

    person.rename(
        columns = {
            "childcare": "weekly_childcare",
            },
        inplace = True
        )
    input_data_frame_by_entity_by_period = {periods.period(year): input_data_frame_by_entity}
    data = dict()
    data['input_data_frame_by_entity_by_period'] = input_data_frame_by_entity_by_period
    return data


if __name__ == "__main__":
    year = 2020
    data = build_entity_dataframe(year = year)
    scenario = UKSurveyScenario(data = data, year = year)
    print(scenario.memory_usage())