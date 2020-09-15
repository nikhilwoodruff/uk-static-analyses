import pandas as pd
from openfisca_uk import CountryTaxBenefitSystem
from openfisca_core.simulation_builder import SimulationBuilder
from openfisca_core.model_api import *
from openfisca_uk.entities import *
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import os
import pandas as pd


def model(*reforms, data_dir="inputs", period="2020-01"):
    """
    Create and populate a tax-benefit simulation model from OpenFisca.

    Arguments:
        reforms: any reforms to apply, in order.
        data: any data to use instead of the loaded Family Resources Survey.
        period: the period in which to enter all data (at the moment, all data is entered under this period).

    Returns:
        A Simulation object.
    """
    system = CountryTaxBenefitSystem()
    for reform in reforms:
        system = reform(system)  # apply each reform in order
    builder = SimulationBuilder()
    builder.create_entities(system)  # create the entities (person, family, etc.)
    if data_dir is None:
        data_dir = "inputs"
    person_file = pd.read_csv(os.path.join(data_dir, "person.csv"))
    family_file = pd.read_csv(os.path.join(data_dir, "family.csv"))
    household_file = pd.read_csv(os.path.join(data_dir, "household.csv"))
    person_ids = np.array(person_file["person_id"])
    family_ids = np.array(family_file["family_id"])
    household_ids = np.array(household_file["household_id"])
    builder.declare_person_entity("person", person_ids)
    families = builder.declare_entity("family", family_ids)
    households = builder.declare_entity("household", household_ids)
    person_roles = person_file["role"]
    builder.join_with_persons(
        families, np.array(person_file["family_id"]), person_roles
    )  # define person-family memberships
    builder.join_with_persons(
        households, np.array(person_file["household_id"]), person_roles
    )
    model = builder.build(system)
    for column in person_file.columns[4:]:
        model.set_input(
            column, period, np.array(person_file[column])
        )  # input data for person data
    for column in family_file.columns[2:]:
        model.set_input(
            column, period, np.array(family_file[column])
        )  # input data for family data
    for column in household_file.columns[1:]:
        model.set_input(
            column, period, np.array(household_file[column])
        )  # input data for household data
    return model


def entity_df(model, entity="family", period="2020-09-12"):
    """
    Create and populate a DataFram with all variables in the simulation

    Arguments:
        model: the model to use.
        entity: the entity to calculate variables for.
        period: the period for which to calculate all data.

    Returns:
        A DataFrame
    """
    if entity not in ["family", "person", "household"]:
        raise Exception("Unsupported entity.")
    if entity == "family":
        weight_col = "family_weight"
    elif entity == "person":
        weight_col = "adult_weight"
    else:
        weight_col = "household_weight"
    df = pd.DataFrame()
    variables = model.tax_benefit_system.variables.keys()
    entity_variables = list(
        filter(
            lambda x: model.tax_benefit_system.variables[x].entity.key == entity,
            variables,
        )
    )
    for var in entity_variables:
        df[var] = model.calculate(var, period)
        df[f"{var}_m"] = model.calculate(weight_col, period)
    return df
