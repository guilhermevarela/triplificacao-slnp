# -*- coding:utf-8 -*-
from LegislatureImporter.legislature_importer import Senator

__author__ = 'Rebeca Bordini <bordini.rebeca@gmail.com>'

def test_senator_initialization():
    data = {
        'slp:resource_uri': 'uri',
        'sen:NomeCompletoParlamentar': 'Renan Calheiros',
        'sen:NomeParlamentar': 'Renan Calheiros'
    }

    senator = Senator(data)
    expected = {
        'resource_uri': 'uri',
        'name': 'Renan Calheiros',
        'parlamentar_name': 'Renan Calheiros',
    }
    assert senator.resource_uri == expected['resource_uri']
    assert senator.name == expected['name']
    assert senator.parlamentar_name == expected['parlamentar_name']