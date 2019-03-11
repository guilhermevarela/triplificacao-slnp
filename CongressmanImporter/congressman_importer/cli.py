# -*- coding:utf-8 -*-
r"""
This module provides a simple form to work with commands using Click Framework. Click is a simple Python module
to writing command line scripts composable and easily.

This module is responsible to call every step of the project, consisted of:
    1. Create all Post instances based on the current avaiable positions of Federal Deputy and Senator, per Federal Unity in Brasil.

    2. Consulting and updating the identiy table to retrieve correct identifier per candidate.

    3. Create a JSON with candidate url, candidate name, civil name, birth_date, party_url and Post (created in step 1)

"""

import click

from .classes import ElectionResults, Identity, Agent, JsonMapper, PartyList, Resource
from .helpers import generate_uuid

__author__ = 'Rebeca Bordini <bordini.rebeca@gmail.com>'

@click.group()
def cli():
    pass


@click.command()
def import_all_elected():
    """
    Import all elected and saves to ontology and identity_final.csv and legislature_56.json files
    """

    # Initializes all classes
    ontology = Agent()
    identity = Identity()
    election_results = ElectionResults()
    json_mapper = JsonMapper()
    party_list = PartyList()

    # Retrieve the elected Deputies and Senators
    elected_data = election_results.get_all_elected()

    # Add all 27 jurisdictions (federal unities)
    ontology.add_all_jurisdictions()

    for elected in elected_data:

        # Every Post created must have a unique identifier
        post_uuid = generate_uuid()

        # Creates Post instance
        ontology.new_post(elected, post_uuid)

        # Look if the current elected has been elected before (based on legislature 55)
        previous_elected_congressman = identity.find(elected.name)

        # Every Membership created must have a unique identifier
        membership_uuid = generate_uuid()

        # If the elected has been elected before, he has an unique identifier already
        if previous_elected_congressman:
            resource = Resource(elected=elected,
                                elected_uuid=previous_elected_congressman.resource_uri,
                                post_uuid=post_uuid,
                                party_uri=party_list.get_party(elected.party_name).uri,
                                membership_uuid=membership_uuid,
                                candidate_name=previous_elected_congressman.parlamentar_name)

        # If the elected has never been elected before, is necessary to generate a new unique identifier and update identity file
        else:
            elected_uuid = generate_uuid()
            resource = Resource(elected=elected,
                                elected_uuid=elected_uuid,
                                post_uuid=post_uuid,
                                party_uri=party_list.get_party(elected.party_name).uri,
                                membership_uuid=membership_uuid,
                                candidate_name='')
            identity.update_data(elected_uuid, elected)

        # Updates legislature_56.json file based on current elected
        json_mapper.generate_resource(resource)

    # Saves legislature_56.json file
    json_mapper.save_file()

    # Saves ontology A-Box file
    ontology.save()


cli.add_command(import_all_elected)

@click.command()
@click.option('--legislature', default=56, 
               help="""id from term ie .: 56 
                       start: 2019-02-01*
                       finish: 2022-01-31 
                       first day is ignored by the script """)
def update_legislature():
   """
   fetches all legislature updates
   """
   from datetime import datetime
   #compute all business days from legislature
   busdays = [datetime.date(2019,2,2), datetime.date(2019,2,3)]


if __name__ == '__main__':
    cli()
