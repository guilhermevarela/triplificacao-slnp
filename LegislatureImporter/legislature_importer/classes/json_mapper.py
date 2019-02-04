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
          "hasPost": ""
        }
      ]
    }

The Resource data is stored in self.body_data array and Info data is stored in self.header, to persist the changes in disk,
the method save_file must be called.
"""

import io
import json

__author__ = 'Rebeca Bordini <bordini.rebeca@gmail.com>'

VERSION = '0.0.1'
LEGISLATURE_FILE = 'generated-data/legislature_56.json'
POST_IRI_PREFIX = 'http://www.w3.org/ns/org#Post'
SNLP_IRI_PREFIX = 'http://www.seliganapolitica.org/resource'


def generate_timestamp():
    """
    Return the actual time based on the format %d-%m-%Y %H:%M
    """
    import time
    from datetime import datetime

    timestamp = time.time()
    return datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M')


class JsonMapper:
    def __init__(self):
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

    def generate_resource(self, resource):
        """
        Generate one resource based on Resource class
        """
        self.body_data.append({
            'url': resource.url,
            'nomeCandidato': resource.candidate_name,
            'nomeCivil': resource.civil_name,
            'dataNascimento': resource.birth_date,
            'urlPartido': resource.party_url,
            'hasPost': resource.hasPost,
        })

    def save_file(self):
        """
        Save the JSON file specified in LEGISLATURE_FILE location
        """
        document = {}
        document['Info'] = self.header
        document['Resource'] = self.body_data

        with io.open(LEGISLATURE_FILE, 'w', encoding='utf8') as out_file:
            json.dump(document, out_file, ensure_ascii=False)
