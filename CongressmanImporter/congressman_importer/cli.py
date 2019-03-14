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
            elected_uuid = previous_elected_congressman.resource_uri
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
    
    # Saves identity_final.csv file
    identity.save_file()

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

    # from datetime import datetime, timedelta
    from congressman_importer import generate_legislature_iterator
    # from congressman_importer.spiders import ActivityCongressmanSpider

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
    import re
    import json

    # from collections import namedtuple
    from .classes import Deputy

    # Person = namedtuple('Person', 'name birth_date')

    def process_message(message):
        m1 = re.search(r'\((.*?)\)', message).group(1)
        m1 = re.search(r'- (.*?) -', m1).group(1)
        return m1

    # Initializes all classes
    ontology = Agent()

    identity = Identity(updated=True)
    # election_results = ElectionResults()
    json_mapper = JsonMapper(load=True)
    # party_list = PartyList()

    # Retrieve the elected Deputies and Senators
    # elected_data = election_results.get_all_elected()

    # Add all 27 jurisdictions (federal unities)
    ontology.add_all_jurisdictions()

    vacant_posts = {}
    for scrapped_file in glob.glob('scrapped-data/legislature_56_*.json'):
        try:
            with open(scrapped_file, 'r', encoding='utf8') as f:
                membership_updates = json.load(f)
            # success process the file
            # finishDates must be processed first
            membership_updates = sorted(membership_updates, key= lambda x: x.get('finishDate', '31/01/2023'))
            for membership_update in membership_updates:

                deputy = identity.find(membership_update['nomeCivil'])

                if not deputy:
                    # create identity for the dude


                    deputy_name = process_message(membership_update['message'])

                    if deputy_name not in vacant_posts:

                        print('create identity for the dude -- posse individual???')
                        import code; code.interact(local=dict(globals(), **locals()))
                        raise ValueError(
                            '''Unable to process {membership}
                                deputy_name {name} not found
                                posts {posts}'''.format(
                                    membership=membership_update,
                                    name=deputy_name,
                                    posts=vacant_posts
                            ))
                    else:
                        post_uuid = vacant_posts[deputy_name]['postUri']

                        party_uri = vacant_posts[deputy_name]['urlPartido']

                        deputy_uuid = generate_uuid()

                        membership_uuid = generate_uuid()

                        membership_update['resource_uri'] = deputy_uuid
                        deputy = Deputy(membership_update)

                        del vacant_posts[deputy_name]

                        identity.update_data(deputy_uuid, deputy)

                lookup = {a: membership_update[a] for a in ['nomeCivil', 'dataNascimento']}
                if 'finishDate' in membership_update:
                    lookup['finishDate'] = None

                    i = json_mapper.lookup_resource(lookup)
                    if i is None:
                        import code; code.interact(local=dict(globals(), **locals()))
                        raise ValueError(
                            """Tried to close a membership which doesn't exist. 
                            File: {file}
                            Congressman: {name}
                            BirthDate: {birth_date}""".format(
                                file=scrapped_file,
                                name=deputy.name,
                                birth_date=lookup['dataNascimento']
                        ))
                    else:
                        # update the membership
                        membership = json_mapper.update_resource(i, {
                            'finishDate': membership_update['finishDate'],
                            'nomeCandidato': membership_update['nomeCandidato']
                        })

                        # save postUri for next congressman to occupy the position
                        vacant_posts[membership['nomeCandidato']] = membership


                else: 
                    resource = Resource(elected=deputy,
                        elected_uuid=deputy_uuid,
                        post_uuid=post_uuid,
                        party_uri=party_uri,
                        membership_uuid=membership_uuid,
                        candidate_name=membership_update['nomeCandidato'])

                    # Updates legislature_56_final.json file based on current deputy
                    json_mapper.generate_resource(resource, start_date=membership_update['startDate'])
                    

        except json.decoder.JSONDecodeError:
            pass # empty json file throws JSONDecodeError


    # Saves identity_final.csv file
    identity.save_file()

    # Saves legislature_56_final.json file
    json_mapper.save_file(updated=True)

    # Saves ontology A-Box file
    # ontology.save()


cli.add_command(update_56)    

if __name__ == '__main__':
    cli()
