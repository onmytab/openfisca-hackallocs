#!/usr/bin/env python


import json

import openfisca_france


def main():
    TaxBenefitSystem = openfisca_france.init_country()
    tax_benefit_system = TaxBenefitSystem()

    scenario = tax_benefit_system.new_scenario()
    scenario.init_single_entity(
        period = 2014,
        parent1 = dict(
            birth = '1970-01-01',
            salaire_de_base = 1000,
            ),
        enfants = [
            dict(
                birth = '2000-02-01',
                ),
            dict(
                birth = '2001-04-17',
                ),
            ],
        )

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
