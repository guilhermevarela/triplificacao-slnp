# -*- coding:utf-8 -*-
import click

from .classes import ElectionResults, Identity, Agent, JsonMapper, PartyList, Resource
from .helpers import generate_uri

__author__ = 'Rebeca Bordini <bordini.rebeca@gmail.com>'

@click.group()
def cli():
    pass


@click.command()
def import_all_elected():
    ontology = Agent()
    identity = Identity()
    election_results = ElectionResults()
    json_mapper = JsonMapper()
    party_list = PartyList()

    elected_2018 = election_results.get_all_elected()
    ontology.add_all_jurisdictions()

    for elected in elected_2018:
        post_uri = generate_uri()
        ontology.new_post(elected, post_uri)

        previous_elected_congressman = identity.find(elected.name)
        if previous_elected_congressman:
            resource = Resource(elected=elected,
                                elected_uri=previous_elected_congressman.resource_uri,
                                post_uri=post_uri,
                                party_uri=party_list.get_party(elected.party_name).uri,
                                candidate_name=previous_elected_congressman.parlamentar_name)

        else:
            elected_uri = generate_uri()
            resource = Resource(elected=elected,
                                elected_uri=elected_uri,
                                post_uri=post_uri,
                                party_uri=party_list.get_party(elected.party_name).uri,
                                candidate_name='')
            identity.update_data(elected_uri, elected)

        json_mapper.generate_resource(resource)

    json_mapper.save_file()


cli.add_command(import_all_elected)


if __name__ == '__main__':
    cli()

