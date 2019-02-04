# -*- coding:utf-8 -*-
import requests

from .party import Party

__author__ = 'Rebeca Bordini <bordini.rebeca@gmail.com>'

DADOS_ABERTOS_PATH = 'https://dadosabertos.camara.leg.br/api/v2/partidos?sigla={initials}&sigla=&ordem=ASC&ordenarPor=sigla'

class PartyList:
    def __init__(self):
        self.parties = []

    def find(self, initials):
        for party in self.parties:
            if party.initials == initials:
                return party
        return None

    def get_party(self, initials):
        party = self.find(initials)

        if not party:
            r = requests.get(DADOS_ABERTOS_PATH.format(initials=initials).replace(" ", ""))
            if r.status_code == requests.codes.ok:
                data = r.json().get('dados', [])[0]
                party = Party(data)

        return party


    def get_all_parties(self):
        return self.parties