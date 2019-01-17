# -*- coding:utf-8 -*-
import csv

# 1. Ler arquivo já consolidado com os eleitos da eleição 2018
# 2. Criar um POST (na ontologia Agents) para cada vaga de deputado/senador, por estado. \
#    com start date 01/02/2019 e end date 31/1/2024), e um estado associado.
# 3. Consultar o tabelão (pelo nome civil) e ver se ele já aparece. Se aparecer,  \
#    n precisa fazer nada. Se não aparecer, tem que criar uma nova entrada, gerando uma URI para ele.
# 4. Criar um JSON com uma entrada para politico, incluindo a URL dele, o nome do candidato, \
#    o nome civil, a data de nascimento, a url do partido (ORG),   e de um  POST que vc criou para o estado dele (\
#    usar um diferente para cada eleito).
# 5. A partir deste JSON, gerar um mapeamento no KARMA (https://usc-isi-i2.github.io/karma/) \
#    para gerar o RDF conforme a ontologia AGENTS que está no diretório.


START_DATE = '01/02/2019'
END_DATE = '31/01/2024'


class Identity:
    def __init__(self):
        self.deputies = []
        self.senators = []

        with open('./identity.csv', 'rb') as csvfile:
            spamreader = csv.DictReader(csvfile, delimiter=';')
            for row in spamreader:
                if row.get('cam:ideCadastro'):
                    self.add_deputy(Deputy(row))
                if row.get('sen:CodigoParlamentar'):
                    self.add_senator(Senator(row))

    def add_deputy(self, deputy):
        self.deputies.append(deputy)

    def add_senator(self, senator):
        self.senators.append(senator)

    def find_deputy(self, name):
        for deputy in self.deputies:
            if deputy.name == name:
                return deputy
        return None

    def get_all_deputies(self):
        return self.deputies

    def get_all_senators(self):
        return self.senators


class ElectionResults:
    def __init__(self):
        self.elected = []

    def get_all_elected(self):
        with open('./candidatos+resultados+2018.csv', 'rb') as csvfile:
            spamreader = csv.DictReader(csvfile, delimiter=',')
            for row in spamreader:
                self.add_elected(Elected(row))
        return self.elected

    def add_elected(self, elected):
        self.elected.append(elected)


class Elected:

    def __init__(self, data):
        self.name = data.get('nome', '')

    def __repr__(self):
        return "{civil_name}".format(civil_name=self.name)


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


class Senator:

    def __init__(self, data):
        self.resource_uri = data.get('slp:resource_uri', '')
        self.civil_name = data.get('sen:NomeCompletoParlamentar', '')
        self.name = data.get('sen:NomeParlamentar', '')

    def __repr__(self):
        return "{civil_name}".format(civil_name=self.civil_name)


def create_post_instance(congressman, state):
    pass


def get_uri():
    pass


def create_uri():
    pass


if __name__ == '__main__':
    identity = Identity()
    deputies = identity.get_all_deputies()

