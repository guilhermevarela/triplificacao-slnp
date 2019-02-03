# -*- coding:utf-8 -*-

class Party:
    def __init__(self, data):
        self.id = data.get('id')
        self.initials = data.get('sigla')
        self.name = data.get('nome')
        self.uri = data.get('uri')

    def __repr__(self):
        return "{name}".format(name=self.name)
