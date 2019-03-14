# -*- coding:utf-8 -*-
r"""JSON Mapper

This module provides an abstraction to writing JSON files in the following signature:

    {
      "Info": {
        "hasType": "Identity",
        "timstampPub": "19-10-2018 18:57",
        "hasVersion": "0.0.1"
      },
      "Resource": [
        {
          "url": "",
          "nomeCandidato": "",
          "nomeCivil": "",
          "dataNascimento": "",
          "urlPartido": "",
          "postUri": ""
        }
      ]
    }

The Resource data is stored in self.body_data array and Info data is stored in self.header, to persist the changes in disk,
the method save_file must be called.
"""

import io
import json

from ..helpers import generate_timestamp

__author__ = 'Rebeca Bordini <bordini.rebeca@gmail.com>'

VERSION = '0.0.2'
LEGISLATURE_FILE = 'generated-data/legislature_56.json'
LEGISLATURE_FILE_UPDATED = 'generated-data/legislature_56_final.json'
POST_IRI_PREFIX = 'http://www.w3.org/ns/org#Post'
SNLP_IRI_PREFIX = 'http://www.seliganapolitica.org/resource'
MEMBERSHIP_START_DATE = "2019-02-01"


class JsonMapper:
    def __init__(self, load=False, file=LEGISLATURE_FILE):
        if load:
            self.load_file(file)
        else:
            self.header = self.generate_header()
            self.body_data = []

    @staticmethod
    def generate_header():
        """
        Generate the header of JSON file
        """
        return {
            "hasType": "Identity",
            "timstampPub": generate_timestamp(),
            "hasVersion": VERSION
        }

    def generate_resource(self, resource, start_date=MEMBERSHIP_START_DATE):
        """
        Generate one resource based on Resource class
        """
        self.body_data.append({
            'membershipUri': resource.membershipUri,
            'url': resource.url,
            'nomeCandidato': resource.candidate_name,
            'nomeCivil': resource.civil_name,
            'dataNascimento': resource.birth_date,
            'urlPartido': resource.party_url,
            'postUri': resource.postUri,
            'startDate': start_date,
            'finishDate': None,
        })

    def lookup_resource(self, lookup_attributes):
        """
        Looks up resources making comparations on attributes dictionary
        """
        def test(src, lkp):
            """
                Looks up lookup dict onto search dict
            """
            return all([src[k] == v for k, v in lkp.items()])

        for i, src in enumerate(self.body_data):
            if test(src, lookup_attributes):            
                return i
        return None
    
    def update_resource(self, i, update_attributes):
        """
        updates resource at position i
        """
        # if i == 321:
        #     import code; code.interact(local=dict(globals(), **locals()))
        self.body_data[i].update(update_attributes)
        return self.body_data[i]

    def save_file(self, updated=False):
        """
        Save the JSON file specified in LEGISLATURE_FILE location
        """
        document = {}
        document['Info'] = self.header
        document['Resource'] = self.body_data

        with io.open(LEGISLATURE_FILE, 'w', encoding='utf8') as out_file:
            json.dump(document, out_file, ensure_ascii=False)

    def load_file(self, file=LEGISLATURE_FILE):
        """
        Load the JSON file specified in file location
        """        
        with io.open(LEGISLATURE_FILE, 'r', encoding='utf8') as in_file:
            document = json.load(in_file)
        self.header = document['Info']
        self.body_data = document['Resource']
