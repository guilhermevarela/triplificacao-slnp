# -*- coding:utf-8 -*-
class Senator:

    def __init__(self, data):
        self.resource_uri = data.get('slp:resource_uri', '')
        self.civil_name = data.get('sen:NomeCompletoParlamentar', '')
        self.name = data.get('sen:NomeParlamentar', '')

    def __repr__(self):
        return "{civil_name}".format(civil_name=self.civil_name)
