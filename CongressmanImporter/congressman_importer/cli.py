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

from enum import Enum

__author__ = 'Rebeca Bordini <bordini.rebeca@gmail.com>'

class DeputyStatus(Enum):
    elected = 'Posse na Sessão Preparatória'
    apointee = 'Posse como Suplente'
    returning = 'Reassunção'

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
def scrape_deputies():
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

    spider_script = 'congressman_importer/spiders/activity_congressman.py'

    target_prefix = 'scrapped-data/legislature_56_'
    for dt in date_range:
        subprocess.Popen(
            "scrapy runspider {script} -o {target}{dt}.json  -a dt='{dt}'".format(
                target=target_prefix,
                script=spider_script,
                dt=dt.strftime('%Y-%m-%d')
            ),
            shell=True
        )

cli.add_command(scrape_deputies)

@click.command()
def update_deputies():
    """
    Updates Resources, Indentities and Ontology
    """
    import glob
    import json

    from .classes import Deputy

    # Initializes all classes
    ontology = Agent()

    identity = Identity(updated=True)

    json_mapper = JsonMapper(load=True)

    party_list = PartyList()

    # Add all 27 jurisdictions (federal unities)
    ontology.add_all_jurisdictions()

    expired_memberships = {}

    scrapped_files = sorted(glob.glob('scrapped-data/legislature_56_*.json'))
    for scrapped_file in scrapped_files:
        try:
            with open(scrapped_file, 'r', encoding='utf8') as f:
                membership_updates = json.load(f)

            # Success: means that the file is not empty
            # finishDates must be processed first as those free up posts that can be occupied
            membership_updates = sorted(
                membership_updates,
                key= lambda x: -1 if 'finishDate' in x else 1
            )
            for membership_update in membership_updates:

                # Generates or re-covers UUIDS
                # * post_uuid, deputy_uuid, party_uri
                deputy_name = membership_update['nomeCandidato']

                # This deputy is leaving office
                is_leaving = 'finishDate' in membership_update

                # This deputy was officialy elected but took office after 2019-02-01
                is_elected = membership_update['replacement'] is None

                # This deputy is either acting as an apointee or is returning into office
                # either way it's assuming a previously occupied post
                is_replacing = membership_update['nomeCandidato'] in expired_memberships
                if is_elected or is_replacing or is_leaving:

                    if is_elected:
                        post_uuid = generate_uuid()

                        party_uri = party_list.get_party(membership_update['party']).uri
                    elif is_replacing:                                            
                        post_uuid = expired_memberships[deputy_name]['postUri'].split('/')[-1]

                        party_uri = expired_memberships[deputy_name]['urlPartido']

                else:
                    raise ValueError(
                        '''Unable to process {membership}
                            deputy_name {name} not found
                            posts {posts}'''.format(
                                membership=membership_update,
                                name=deputy_name,
                                posts=expired_memberships
                        ))

                #Is this name registered in our database
                deputy = identity.find(membership_update['nomeCivil'])

                # Generate an identity for the deputy
                if not deputy:

                    deputy_uuid = generate_uuid()

                    membership_update['resource_uri'] = deputy_uuid
                    deputy = Deputy(membership_update)

                    del expired_memberships[deputy_name]

                    identity.update_data(deputy_uuid, deputy)

                else:
                    # this deputy is already registered
                    deputy_uuid = deputy.resource_uri

                # This segment updates the Resources or Memberships by either:
                # * update an existing Membership ( finishDate == processingDate )
                # * generates a new membership
                if is_leaving: # Closing an existing membership
                    lookup = {
                        'nomeCivil': membership_update['nomeCivil'],
                        'dataNascimento': membership_update['dataNascimento'],
                        'finishDate': None,
                    }

                    resources = json_mapper.find(lookup)
                    if not resources:
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
                        membership = resources[-1]
                        membership.update({
                            'finishDate': membership_update['finishDate'],
                            'nomeCandidato': membership_update['nomeCandidato']
                        })
                        if membership_update['replacement'] is not None:
                            # save postUri for next congressman to occupy the position
                            expired_memberships[membership_update['replacement']] = membership


                else: # Creating a membership
                    membership_uuid = generate_uuid()

                    try:
                        resource = Resource(elected=deputy,
                            elected_uuid=deputy_uuid,
                            post_uuid=post_uuid,
                            party_uri=party_uri,
                            membership_uuid=membership_uuid,
                            candidate_name=membership_update['nomeCandidato'])

                        # Updates legislature_56_final.json file based on current deputy
                        json_mapper.generate_resource(resource, start_date=membership_update['startDate'])
                    except UnboundLocalError:
                        print('UnboundLocalError')
                        import code; code.interact(local=dict(globals(), **locals()))

        except json.decoder.JSONDecodeError:
            pass # empty json file throws JSONDecodeError


    # Saves identity_final.csv file
    identity.save_file()

    # Saves legislature_56_final.json file
    json_mapper.save_file(updated=True)

    # Saves ontology A-Box file
    # ontology.save()


cli.add_command(update_deputies)

if __name__ == '__main__':
    cli()
