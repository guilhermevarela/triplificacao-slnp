# -*- coding:utf-8 -*-
import click

from .classes import ElectionResults, Identity, Agent, generate_uri

# 4. Criar um JSON com uma entrada para politico, incluindo a URL dele, o nome do candidato, \
#    o nome civil, a data de nascimento, a url do partido (ORG),   e de um  POST que vc criou para o estado dele (\
#    usar um diferente para cada eleito).
# 5. A partir deste JSON, gerar um mapeamento no KARMA (https://usc-isi-i2.github.io/karma/) \
#    para gerar o RDF conforme a ontologia AGENTS que está no diretório.


# 81 senadores
# 513 deputados federais


def get_jurisdiction_list_from_elected(elected_list):
    return list(set([elected.federal_unity for elected in elected_list]))


def add_all_jurisdictions(jurisdiction_list):
    ontology = Agent()
    for jurisdiction in jurisdiction_list:
        ontology.new_jurisdiction(jurisdiction)

def add_post(elected, uri):
    ontology = Agent()
    ontology.new_post(elected, uri)


@click.group()
def cli():
    pass


@click.command()
def import_all_elected():
    identity = Identity()
    election_results = ElectionResults()
    elected_2018 = election_results.get_all_elected()

    jurisdiction_list = get_jurisdiction_list_from_elected(elected_2018)
    add_all_jurisdictions(jurisdiction_list)

    for elected in elected_2018:
        uri = generate_uri()
        add_post(elected, uri)

        if not identity.find(elected.name):
            identity.update_data(uri, elected)


cli.add_command(import_all_elected)


if __name__ == '__main__':
    cli()

