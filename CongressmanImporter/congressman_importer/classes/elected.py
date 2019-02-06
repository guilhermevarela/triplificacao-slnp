# -*- coding:utf-8 -*-
r"""Elected objects

This module provides a object to represent Elected people.

"""


__author__ = 'Rebeca Bordini <bordini.rebeca@gmail.com>'

class Elected:

    def __init__(self, data):
        self.name = data.get('nome', '')
        self.birth_date = data.get('data_nascimento', '')
        self.cpf = data.get('cpf', '')
        self.electoral_unity = data.get('sigla_ue', '')
        self.federal_unity = data.get('sigla_uf', '')
        self.party = data.get('numero_partido', '')
        self.party_name = data.get('sigla_partido', '')
        self.post = data.get('descricao_cargo', '')
        self.shift = data.get('descricao_totalizacao_turno', '')
        self.election_year = data.get('ano_eleicao', '')

    def __repr__(self):
        return str(vars(self))
