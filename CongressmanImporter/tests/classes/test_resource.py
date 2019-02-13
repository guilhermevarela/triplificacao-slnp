# -*- coding:utf-8 -*-
from CongressmanImporter.congressman_importer import Resource, Elected

__author__ = 'Rebeca Bordini <bordini.rebeca@gmail.com>'

def test_resource_initialization_with_candidate_name():
    elected = Elected({
        "nome": "nome",
        "data_nascimento": "01/01/19000"
    })
    resource = Resource(elected, 'elected_uri', 'post_uri', 'party_uri', 'membership_uri', 'Name')
    expected = {
        'url': 'http://www.seliganapolitica.org/resource/elected_uri',
        'candidate_name': 'Name',
        'civil_name': 'nome',
        'birth_date': '01/01/19000',
        'party_url': 'party_uri',
        'hasPost': 'http://www.w3.org/ns/org#Post/post_uri'
    }
    assert resource.url == expected['url']
    assert resource.candidate_name == expected['candidate_name']
    assert resource.civil_name == expected['civil_name']
    assert resource.birth_date == expected['birth_date']
    assert resource.party_url == expected['party_url']
    assert resource.postUri == expected['hasPost']

def test_resouruce_initialization_without_candidate_name():
    elected = Elected({
        "nome": "nome",
        "data_nascimento": "01/01/19000"
    })
    resource = Resource(elected, 'elected_uri', 'post_uri', 'party_uri', 'membership_uri')
    expected = {
        'url': 'http://www.seliganapolitica.org/resource/elected_uri',
        'candidate_name': '',
        'civil_name': 'nome',
        'birth_date': '01/01/19000',
        'party_url': 'party_uri',
        'hasPost': 'http://www.w3.org/ns/org#Post/post_uri'
    }
    assert resource.url == expected['url']
    assert resource.candidate_name == expected['candidate_name']
    assert resource.civil_name == expected['civil_name']
    assert resource.birth_date == expected['birth_date']
    assert resource.party_url == expected['party_url']
    assert resource.postUri == expected['hasPost']
