# -*- coding:utf-8 -*-
from LegislatureImporter.legislature_importer import Elected

__author__ = 'Rebeca Bordini <bordini.rebeca@gmail.com>'

def test_elected_initialization():
    data = {
        'nome': 'Jean Wyllis',
        'data_nascimento': '30/01/1977',
        'cpf': '000',
        'sigla_ue': 'RJ',
        'sigla_uf': 'RJ',
        'numero_partido': '47',
        'sigla_partido': 'PSOL',
        'descricao_cargo': 'Deputado Federal',
        'descricao_totalizacao_turno': '',
        'ano_eleicao': '2018',
    }

    elected = Elected(data)
    expected = {
        'name': 'Jean Wyllis',
        'birth_date': '30/01/1977',
        'cpf': '000',
        'electoral_unity': 'RJ',
        'federal_unity': 'RJ',
        'party': '47',
        'party_name': 'PSOL',
        'post': 'Deputado Federal',
        'shift': '',
        'election_year': '2018',
    }

    assert elected.name == expected['name']
    assert elected.birth_date == expected['birth_date']
    assert elected.cpf == expected['cpf']
    assert elected.electoral_unity == expected['electoral_unity']
    assert elected.federal_unity == expected['federal_unity']
    assert elected.party == expected['party']
    assert elected.party_name == expected['party_name']
    assert elected.post == expected['post']
    assert elected.shift == expected['shift']
    assert elected.election_year == expected['election_year']