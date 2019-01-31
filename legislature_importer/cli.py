# -*- coding:utf-8 -*-
import click


from owlready2 import *


from .classes import ElectionResults, Identity
from .helpers import generate_uri


# 2. Criar um POST (na ontologia Agents) para cada vaga de deputado/senador, por estado. \
#    com start date 01/02/2019 e end date 31/1/2024), e um estado associado.
# 4. Criar um JSON com uma entrada para politico, incluindo a URL dele, o nome do candidato, \
#    o nome civil, a data de nascimento, a url do partido (ORG),   e de um  POST que vc criou para o estado dele (\
#    usar um diferente para cada eleito).
# 5. A partir deste JSON, gerar um mapeamento no KARMA (https://usc-isi-i2.github.io/karma/) \
#    para gerar o RDF conforme a ontologia AGENTS que está no diretório.

# 81 senadores
# 513 deputados federais


START_DATE = '01/02/2019'
END_DATE = '31/01/2024'


@click.group()
def cli():
    pass


@click.command()
def import_all_elected():
    identity = Identity()
    election_results = ElectionResults()
    elected_2018 = election_results.get_all_elected()
    for elected in elected_2018:
        if not identity.find(elected.name):
            uri = generate_uri()
            identity.update_data(uri, elected)


@click.command()
def populate_senator_posts():
    click.echo('Initialized senator posts')


@click.command()
def populate_deputies_posts():
    click.echo('Initialized deputies posts')


cli.add_command(import_all_elected)
cli.add_command(populate_senator_posts)
cli.add_command(populate_deputies_posts)


if __name__ == '__main__':
    cli()

