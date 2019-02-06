# -*- coding:utf-8 -*-

from CongressmanImporter.congressman_importer import Party

__author__ = 'Rebeca Bordini <bordini.rebeca@gmail.com>'

def test_party():
    data = {
        'id': '36779',
        'sigla': 'PCdoB',
        'uri': 'https://dadosabertos.camara.leg.br/api/v2/partidos/36779',
        'nome': 'Partido Comunista do Brasil'
    }

    party = Party(data)
    expected = {
        'id': '36779',
        'initials': 'PCdoB',
        'uri': 'https://dadosabertos.camara.leg.br/api/v2/partidos/36779',
        'name': 'Partido Comunista do Brasil'
    }
    assert party.id == expected['id']
    assert party.initials == expected['initials']
    assert party.uri == expected['uri']
    assert party.name == expected['name']