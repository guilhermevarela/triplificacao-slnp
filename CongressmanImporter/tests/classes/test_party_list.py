# -*- coding:utf-8 -*-
import requests_mock

from CongressmanImporter.congressman_importer import PartyList, Party

__author__ = 'Rebeca Bordini <bordini.rebeca@gmail.com>'


def test_party_list_initialization():
    assert PartyList().parties == []


@requests_mock.Mocker(kw='mock')
def test_get_party(**kwargs):
    fake_response = {
        "dados": [
            {
                "id": 36899,
                "sigla": "MDB",
                "nome": "Movimento Democrático Brasileiro",
                "uri": "https://dadosabertos.camara.leg.br/api/v2/partidos/36899"
            }
        ],
        "links": [
            {
                "rel": "self",
                "href": "https://dadosabertos.camara.leg.br/api/v2/partidos?sigla=MDB&ordem=ASC&ordenarPor=sigla"
            },
            {
                "rel": "first",
                "href": "https://dadosabertos.camara.leg.br/api/v2/partidos?sigla=MDB&ordem=ASC&ordenarPor=sigla&pagina=1&itens=15"
            },
            {
                "rel": "last",
                "href": "https://dadosabertos.camara.leg.br/api/v2/partidos?sigla=MDB&ordem=ASC&ordenarPor=sigla&pagina=1&itens=15"
            }
        ]
    }
    kwargs['mock'].get('https://dadosabertos.camara.leg.br/api/v2/partidos?sigla=MDB&sigla=&ordem=ASC&ordenarPor=sigla',
                       json=fake_response)
    expected = Party(fake_response.get('dados')[0])
    found = PartyList().get_party('MDB')
    assert expected.id == found.id
    assert expected.initials == found.initials
    assert expected.name == found.name
    assert expected.uri == found.uri


@requests_mock.Mocker(kw='mock')
def test_get_party_with_spaces_in_initials(**kwargs):
    fake_response = {
        "dados": [
            {
                "id": 36779,
                "sigla": "PCdoB",
                "nome": "Partido Comunista do Brasil",
                "uri": "https://dadosabertos.camara.leg.br/api/v2/partidos/36779"
            }
        ],
        "links": [
            {
                "rel": "self",
                "href": "https://dadosabertos.camara.leg.br/api/v2/partidos?sigla=PCdoB&ordem=ASC&ordenarPor=sigla"
            },
            {
                "rel": "first",
                "href": "https://dadosabertos.camara.leg.br/api/v2/partidos?sigla=PCdoB&ordem=ASC&ordenarPor=sigla&pagina=1&itens=15"
            },
            {
                "rel": "last",
                "href": "https://dadosabertos.camara.leg.br/api/v2/partidos?sigla=PCdoB&ordem=ASC&ordenarPor=sigla&pagina=1&itens=15"
            }
        ]
    }

    kwargs['mock'].get(
        'https://dadosabertos.camara.leg.br/api/v2/partidos?sigla=PCdoB&sigla=&ordem=ASC&ordenarPor=sigla',
        json=fake_response)
    expected = Party(fake_response.get('dados')[0])
    found = PartyList().get_party('PC do B')
    assert expected.id == found.id
    assert expected.initials == found.initials
    assert expected.name == found.name
    assert expected.uri == found.uri
