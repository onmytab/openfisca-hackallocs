#!/usr/bin/env python


# import json

import numpy as np

from openfisca_core import periods
import openfisca_france


def main():
    TaxBenefitSystem = openfisca_france.init_country()
    tax_benefit_system = TaxBenefitSystem()

    scenario = tax_benefit_system.new_scenario()
    scenario.period = periods.period('2014')
    # scenario.init_single_entity(
    #     period = 2014,
    #     parent1 = dict(
    #         birth = '1970-01-01',
    #         salaire_de_base = 1000,
    #         ),
    #     enfants = [
    #         dict(
    #             birth = '2000-02-01',
    #             ),
    #         dict(
    #             birth = '2001-04-17',
    #             ),
    #         ],
    #     )

    scenario.input_variables = {
        variable_name: {periods.period('2014'): input_variable}
        for variable_name, input_variable in {
            'birth': np.array([np.datetime64('1970-01-01'), np.datetime64('2000-02-02'), np.datetime64('2001-02-02')]),
            'idfam': np.array([0, 0, 0]),
            'idfoy': np.array([0, 0, 0]),
            'idmen': np.array([0, 0, 0]),
            'quifam': np.array([0, 2, 3]),
            'quifoy': np.array([0, 2, 3]),
            'quimen': np.array([0, 2, 3]),
            'salaire_de_base': np.array([1000, 0, 0]),
            }.iteritems()
        }
    # scenario_json = scenario.to_json()
    # simulation_json = {
    #     'scenarios': [scenario_json],
    #     'variables': ['ars'],
    #     }
    # print json.dumps(simulation_json, indent = 2)

    simulation = scenario.new_simulation()
    ars = simulation.calculate('ars')
    print ars


if __name__ == '__main__':
    main()
