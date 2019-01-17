# -*- coding:utf-8 -*-
import csv
from dateutil.parser import parse

# 2. Criar um POST (na ontologia Agents) para cada vaga de deputado/senador, por estado. \
#    com start date 01/02/2019 e end date 31/1/2024), e um estado associado.
# 4. Criar um JSON com uma entrada para politico, incluindo a URL dele, o nome do candidato, \
#    o nome civil, a data de nascimento, a url do partido (ORG),   e de um  POST que vc criou para o estado dele (\
#    usar um diferente para cada eleito).
# 5. A partir deste JSON, gerar um mapeamento no KARMA (https://usc-isi-i2.github.io/karma/) \
#    para gerar o RDF conforme a ontologia AGENTS que está no diretório.

## 81 senadores
## 513 deputados federais


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

    def find(self, name):
        congressman_list = self.deputies + self.senators
        for congressman in congressman_list:
            if congressman.name == name:
                return congressman
        return None

    def get_all_deputies(self):
        return self.deputies

    def get_all_senators(self):
        return self.senators

    def update_data(self, uri, data):
        with open('./identity_final.csv', 'a') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';')
            formated_birth_date = parse(data.birth_date)
            spamwriter.writerow([uri, '', formated_birth_date.strftime('%Y-%m-%d'), '', data.name, '', '', '', ''])


class ElectionResults:

    POSTS = ['SENADOR', 'DEPUTADO FEDERAL']
    ELECTED_FLAGS = ['ELEITO', 'ELEITO POR MEDIA', 'ELEITO POR QP']

    def __init__(self):
        self.elected = []

        with open('./candidatos+resultados+2018.csv', 'rb') as csvfile:
            spamreader = csv.DictReader(csvfile, delimiter=',')
            for row in spamreader:
                self.add_elected(Elected(row))

    def add_elected(self, elected):
        if elected.post in self.POSTS and elected.shift in self.ELECTED_FLAGS:
            self.elected.append(elected)

    def get_all_elected(self):
        return self.elected


class Elected:

    def __init__(self, data):
        self.name = data.get('nome', '')
        self.birth_date = data.get('data_nascimento', '')
        self.cpf = data.get('cpf', '')
        self.electoral_unity = data.get('sigla_uf', '')
        self.party = data.get('numero_partido', '')
        self.party_name = data.get('sigla_partido', '')
        self.post = data.get('descricao_cargo', '')
        self.shift = data.get('descricao_totalizacao_turno', '')
        self.election_year = data.get('ano_eleicao', '')

    def __repr__(self):
        return str(vars(self))


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


def generate_uri():
    import uuid
    return str(uuid.uuid4())


if __name__ == '__main__':
    identity = Identity()
    election_results = ElectionResults()
    elected_2018 = election_results.get_all_elected()
    for elected in elected_2018:
        if not identity.find(elected.name):
            uri = generate_uri()
            identity.update_data(uri, elected)
