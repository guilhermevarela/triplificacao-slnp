# -*- coding:utf-8 -*-
class Deputy:

    def __init__(self, data):
        self.resource_uri = data.get('slp:resource_uri', '')
        self.death_date = data.get('cam:dataFalecimento', '')
        self.birth_date = data.get('cam:dataNascimento', '')
        self.id = data.get('cam:ideCadastro', '')
        self.civil_name = data.get('cam:nomeCivil', '')
        self.name = data.get('cam:nomeParlamentarAtual', '')

    def __repr__(self):
        return "{civil_name}".format(civil_name=self.civil_name)
