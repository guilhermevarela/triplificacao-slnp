# -*- coding:utf-8 -*-
r"""Deputy objects

This module provides a object to represent Deputies.

"""

__author__ = 'Rebeca Bordini <bordini.rebeca@gmail.com>'

class Deputy:

    def __init__(self, data):
        self.resource_uri = data.get('slp:resource_uri', '')
        self.death_date = data.get('cam:dataFalecimento', '')
        self.birth_date = data.get('cam:dataNascimento', '')
        self.id = data.get('cam:ideCadastro', '')
        self.name = data.get('cam:nomeCivil', '')
        self.parlamentar_name = data.get('cam:nomeParlamentarAtual', '')

    def __repr__(self):
        return "{name}".format(name=self.name)
