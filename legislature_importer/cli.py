# -*- coding:utf-8 -*-
import click

from .classes import ElectionResults, Identity, Agent, JsonMapper
from .helpers import generate_uri


# 5. A partir deste JSON, gerar um mapeamento no KARMA (https://usc-isi-i2.github.io/karma/) \
#    para gerar o RDF conforme a ontologia AGENTS que está no diretório.


@click.group()
def cli():
    pass


@click.command()
def import_all_elected():
    ontology = Agent()
    identity = Identity()
    election_results = ElectionResults()
    json_mapper = JsonMapper()

    elected_2018 = election_results.get_all_elected()
    ontology.add_all_jurisdictions()

    for elected in elected_2018:
        post_uri = generate_uri()
        ontology.new_post(elected, post_uri)

        previous_elected_congressman = identity.find(elected.name)
        if previous_elected_congressman:
            json_mapper.generate_resource(elected, previous_elected_congressman.resource_uri, post_uri, previous_elected_congressman.name)

        else:
            elected_uri = generate_uri()
            json_mapper.generate_resource(elected, elected_uri, post_uri, '')
            identity.update_data(elected_uri, elected)

    json_mapper.save_file()

cli.add_command(import_all_elected)


if __name__ == '__main__':
    cli()

