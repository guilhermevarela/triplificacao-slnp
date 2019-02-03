# -*- coding:utf-8 -*-
class Senator:

    def __init__(self, data):
        self.resource_uri = data.get('slp:resource_uri', '')
        self.name = data.get('sen:NomeCompletoParlamentar', '')
        self.parlamentar_name = data.get('sen:NomeParlamentar', '')

    def __repr__(self):
        return "{name}".format(name=self.name)
