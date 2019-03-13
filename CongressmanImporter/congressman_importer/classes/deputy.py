# -*- coding:utf-8 -*-
r"""Deputy objects

This module provides a object to represent Deputies.

2019-02-13: add attributes from elections extending class attributes

"""

__author__ = 'Rebeca Bordini <bordini.rebeca@gmail.com>'

class Deputy:

    CONGRESS_API_MAPPING = {
        'slp:resource_uri': 'resource_uri',
        'cam:dataFalecimento': 'death_date',
        'cam:dataNascimento': 'birth_date',
        'cam:ideCadastro': 'id',
        'cam:nomeCivil': 'name',
        'cam:nomeParlamentarAtual': 'parlamentar_name'
    }
    ELECTED_ATTRIBUTES = [
        'cpf', 'shift', 'party'
        'federal_unity', 'party_name', 'birth_date', 
        'post', 'electoral_unity', 'election_year'

    ]

    def __init__(self, data={}):
        for k, v in self.CONGRESS_API_MAPPING.items():
            setattr(self, v, data.get(k, ''))

    def __repr__(self):
        return "{name}".format(name=self.name)

    def update_data(self, uri, data):

        if self.resource_uri == uri:
            # re-writes in case is empty
            self.resource_uri = uri
            for k, v in data.__dict__.items():
                setattr(self, k, v)

        return self

    def dump(self):
        """
            Converts object into dict form preserving MAPPING
        """
        data = {}
        for k, v in self.CONGRESS_API_MAPPING.items():
            if hasattr(self, v):
                data[k] = getattr(self, v)

        for k in self.ELECTED_ATTRIBUTES:
            if hasattr(self, k):
                data[k] = getattr(self, k)

        return data
