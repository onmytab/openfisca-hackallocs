#!/usr/bin/env python


# import json

import numpy as np

from openfisca_core import periods
import openfisca_france

year_birth = (2014-individu['age']).astype(int).astype(str)
individu['birth'] = year_birth + '-10-02'
individu['birth'] =  pd.to_datetime(individu['birth'])
del individu['age']

def main():
    TaxBenefitSystem = openfisca_france.init_country()
    tax_benefit_system = TaxBenefitSystem()

    scenario = tax_benefit_system.new_scenario()
    scenario.period = periods.period('2014')

    scenario.input_variables = {
        variable_name: {periods.period('2014'): input_variable}
        for variable_name, input_variable in individu.to_dict().iteritems()
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
