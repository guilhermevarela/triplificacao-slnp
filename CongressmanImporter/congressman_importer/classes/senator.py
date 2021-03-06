# -*- coding:utf-8 -*-
r"""Senator objects

This module provides a object to represent Senators.

"""

__author__ = 'Rebeca Bordini <bordini.rebeca@gmail.com>'

class Senator:

    SENATE_API_MAPPING = {
        'slp:resource_uri': 'resource_uri',
        'sen:NomeCompletoParlamentar': 'name',
        'sen:NomeParlamentar': 'parlamentar_name'
    }
    ELECTED_ATTRIBUTES = [
        'cpf', 'shift', 'party', 'name',
        'federal_unity', 'party_name', 'birth_date',
        'post', 'electoral_unity', 'election_year'
    ]

    def __init__(self, data={}):
        for k, v in self.SENATE_API_MAPPING.items():
            setattr(self, v, data.get(k, ''))

    def __repr__(self):
        return "{name}".format(name=self.name)

    def update_data(self, uri, data):

        if self.resource_uri == '' or self.resource_uri == uri:
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
        for k, v in self.SENATE_API_MAPPING.items():
            if hasattr(self, v):
                data[k] = getattr(self, v)

        for k in self.ELECTED_ATTRIBUTES:
            if hasattr(self, k):
                data[k] = getattr(self, k)

        return data
