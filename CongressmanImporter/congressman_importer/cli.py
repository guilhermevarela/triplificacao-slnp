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
def scrape_56():
    """
    fetches legislature 56 activity
    """
    import os
    import subprocess

    from datetime import datetime, timedelta
    from congressman_importer import generate_legislature_iterator
    from congressman_importer.spiders import ActivityCongressmanSpider

    # DEFINE THE SCRAPPING INTERVAL
    date_range = generate_legislature_iterator()
    
    for dt in date_range:
        subprocess.Popen(
            "scrapy runspider congressman_importer/spiders/activity_congressman.py -o scrapped-data/legislature_56_{dt}.json  -a dt='{dt}'".format(
                dt=dt.strftime('%Y-%m-%d')
            ),
            shell=True
        )

cli.add_command(scrape_56)

@click.command()
def update_56():
    """
    Updates Resources, Indentities and Ontology
    """
    import glob
    import json
    # Initializes all classes
    ontology = Agent()
    # identity = Identity(updated=True)
    identity = Identity()
    election_results = ElectionResults()
    json_mapper = JsonMapper(load=True)
    party_list = PartyList()

    # Retrieve the elected Deputies and Senators
    elected_data = election_results.get_all_elected()

    # Add all 27 jurisdictions (federal unities)
    ontology.add_all_jurisdictions()

    posts = {}
    for scrapped_file in glob.glob('scrapped-data/legislature_56_*.json'):
        membership_updates = [] 
        try:
            with open(scrapped_file, 'r', encoding='utf8') as f:
                membership_updates = json.load(f)
            # success process the file
            for membership_update in membership_updates:
                congressman_identity = identity.find(membership_update['nomeCivil'])
                if not congressman_identity:
                    # create identity for the dude
                    print('create identity for the dude')
                    import code; code.interact(local=dict(globals(), **locals()))
                
                lookup = {a: membership_update[a] for a in ['nomeCivil', 'dataNascimento']}
                if 'finishDate' in membership_update:
                    lookup['finishDate'] = None 
                    
                    i = json_mapper.lookup_resource(lookup)                    
                    if i is None:
                        raise ValueError(
                            """Tried to close a membership which doesn't exist. 
                            File: {file} 
                            Congressman: {name}
                            BirthDate: {birth_date}""".format(
                                file=scrapped_file,
                                name=congressman_identity,
                                birth_date=lookup['dataNascimento']
                        ))
                    else:
                        # update the membership
                        membership = json_mapper.update_resource(i, {'finishDate': lookup['finishDate']})
                        # save postUri for next congressman to occupy the position
                        posts[membership['nomeCandidato']] = membership['postUri']


                else: 
                    # new membership is there a post for it??
                    print('new membership is there a post for it??')
                    import code; code.interact(local=dict(globals(), **locals()))
                # Every Membership created must have a unique identifier                
                membership_uuid = generate_uuid()
        except json.decoder.JSONDecodeError:
            pass # empty json file throws JSONDecodeError

        
    # for elected in elected_data:

    #     # Every Post created must have a unique identifier
    #     post_uuid = generate_uuid()

    #     # Creates Post instance
    #     ontology.new_post(elected, post_uuid)

    #     # Look if the current elected has been elected before (based on legislature 55)
    #     previous_elected_congressman = identity.find(elected.name)

    #     # Every Membership created must have a unique identifier
    #     membership_uuid = generate_uuid()

    #     # If the elected has been elected before, he has an unique identifier already
    #     if previous_elected_congressman:
    #         resource = Resource(elected=elected,
    #                             elected_uuid=previous_elected_congressman.resource_uri,
    #                             post_uuid=post_uuid,
    #                             party_uri=party_list.get_party(elected.party_name).uri,
    #                             membership_uuid=membership_uuid,
    #                             candidate_name=previous_elected_congressman.parlamentar_name)

    #     # If the elected has never been elected before, is necessary to generate a new unique identifier and update identity file
    #     else:
    #         elected_uuid = generate_uuid()
    #         resource = Resource(elected=elected,
    #                             elected_uuid=elected_uuid,
    #                             post_uuid=post_uuid,
    #                             party_uri=party_list.get_party(elected.party_name).uri,
    #                             membership_uuid=membership_uuid,
    #                             candidate_name='')
    #         identity.update_data(elected_uuid, elected)

    #     # Updates legislature_56.json file based on current elected
    #     json_mapper.generate_resource(resource)

    # Saves legislature_56.json file
    # json_mapper.save_file()

    # Saves ontology A-Box file
    # ontology.save()


cli.add_command(update_56)    

if __name__ == '__main__':
    cli()
