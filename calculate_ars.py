#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import json
import os

import numpy as np
import pandas as pd

from openfisca_core import periods
import openfisca_france


script_dir = os.path.realpath(os.path.dirname(__file__))
data_dir = os.path.realpath(os.path.join(script_dir, 'data'))


def read_data(path):
    # path_agen = os.path.join(path, 'agen_utile.csv')
    # agen = pd.read_csv(path_agen, sep=';')

    path_fil = os.path.join(path, 'fil_utile.csv')
    fil = pd.read_csv(path_fil, sep=';')

    ###
    # données foyer familliales
    # fam = fil['ARSVERS']
    # NUMCOMDO ?
    # fam2 = agen[['ARSVERS', 'MTARSVER']]

    # données individuelles
    # on part de la table par foyer

    var_ages = ['DTNAIRES', 'DTNAICON']
    var_age_enf = [u'ANNNEN1', u'ANNNEN2', u'ANNNEN3', u'ANNNEN4']
    ind = fil[['PERSCOUV', 'SEXE'] + var_ages + var_age_enf]

    nb_adulte = 1 + (ind.DTNAICON != 99)
    nb_enf = (ind.PERSCOUV - nb_adulte)
    nb_enf_autres = nb_enf - 4 * (ind.ANNNEN4.notnull())
    nb_enf_autres[nb_enf_autres < 0] = 0

    for var in var_age_enf:
        ind[var].replace(0, np.nan, inplace=True)
        ind[var] = 2013 - ind[var]

    # sexe_conj = ~ind['SEXE']  # inutile en fait

    for var in var_ages:
        age = ind[var]
        age[age == 99] = np.nan
        age = 5 * (age - 2) + 20 + 2
        age[age == 17] = 10
        ind[var] = age

    ind['idfam'] = ind.index

    # quifam = 0
    quifam0 = ind[['idfam', 'DTNAIRES']]
    quifam0.columns = ['idfam', 'age']
    quifam0['quifam'] = 0
    # quifam = 0
    quifam1 = ind.loc[ind['DTNAICON'].notnull(),
                      ['idfam', 'DTNAICON']]
    quifam1.columns = ['idfam', 'age']
    quifam1['quifam'] = 1

    list_enf = []
    for num_enf in range(4):
        var_enf_name = 'ANNNEN' + str(num_enf + 1)
        var_enf = ind[var_enf_name]
        enf = ind.loc[var_enf.notnull(), ['idfam', var_enf_name]]
        enf.columns = ['idfam', 'age']
        enf['quifam'] = 2 + num_enf + 1
        list_enf += [enf]

    count = 7
    while sum(nb_enf_autres > 0) > 0:
        cond = nb_enf_autres > 0
        enf_autre = ind.loc[cond, ['idfam', 'ANNNEN4']]
        enf_autre.columns = ['idfam', 'age']
        enf_autre['age'] += count - 6
        enf_autre['quifam'] = count
        nb_enf_autres -= 1
        count += 1
        list_enf += [enf_autre]

    individu = quifam0.append([quifam1] + list_enf)
    return individu


def main():
    TaxBenefitSystem = openfisca_france.init_country()
    tax_benefit_system = TaxBenefitSystem()

    scenario = tax_benefit_system.new_scenario()
    scenario.period = periods.period('2014')

    individu = read_data(data_dir)

    year_birth = (2014 - individu['age']).astype(int).astype(str)
    individu['birth'] = year_birth + '-10-02'
    individu['birth'] = pd.to_datetime(individu['birth'])
    del individu['age']

    scenario.input_variables = {
        variable_name: {periods.period('2014'): serie.values}
        for variable_name, serie in individu.iterkv()
        }

    simulation = scenario.new_simulation()
    ars = simulation.calculate('ars')
    print ars
    print len(ars)


if __name__ == '__main__':
    main()
