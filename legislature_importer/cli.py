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


@click.group()
def cli():
    pass


@click.command()
def import_all_elected():
    ontology = Agent()
    identity = Identity()
    election_results = ElectionResults()
    elected_2018 = election_results.get_all_elected()

    ontology.add_all_jurisdictions()

    for elected in elected_2018:
        uri = generate_uri()
        ontology.new_post(elected, uri)

        if not identity.find(elected.name):
            identity.update_data(uri, elected)


cli.add_command(import_all_elected)


if __name__ == '__main__':
    cli()

