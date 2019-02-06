# -*- coding:utf-8 -*-
import logging

from CongressmanImporter.legislature_importer import Deputy

__author__ = 'Rebeca Bordini <bordini.rebeca@gmail.com>'

def test_deputy_initialization():
    data = {
        'slp:resource_uri': 'uri',
        'cam:dataFalecimento': '00/00/0000',
        'cam:dataNascimento': '00/00/0000',
        'cam:ideCadastro': '2456',
        'cam:nomeCivil': 'Jean Wyllis',
        'cam:nomeParlamentarAtual': 'Jean Wyllis',
    }

    deputy = Deputy(data)
    expected = {
        'resource_uri': 'uri',
        'death_date': '00/00/0000',
        'birth_date': '00/00/0000',
        'id': '2456',
        'name': 'Jean Wyllis',
        'parlamentar_name': 'Jean Wyllis',
    }
    assert deputy.resource_uri == expected['resource_uri']
    assert deputy.death_date == expected['death_date']
    assert deputy.birth_date == expected['birth_date']
    assert deputy.id == expected['id']
    assert deputy.name == expected['name']
    assert deputy.parlamentar_name == expected['parlamentar_name']