# -*- coding:utf-8 -*-
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
