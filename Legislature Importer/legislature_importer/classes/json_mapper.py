# -*- coding:utf-8 -*-
import io
import json

VERSION = '0.0.1'
LEGISLATURE_FILE = 'generated-data/legislature_56.json'
POST_IRI_PREFIX = 'http://www.w3.org/ns/org#Post'
SNLP_IRI_PREFIX = 'http://www.seliganapolitica.org/resource'


def generate_timestamp():
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
        return {
            "hasType": "Identity",
            "timstampPub": generate_timestamp(),
            "hasVersion": VERSION
        }

    def generate_resource(self, resource):
        self.body_data.append({
            'url': resource.url,
            'nomeCandidato': resource.candidate_name,
            'nomeCivil': resource.civil_name,
            'dataNascimento': resource.birth_date,
            'urlPartido': resource.party_url,
            'hasPost': resource.hasPost,
        })

    def save_file(self):
        document = {}
        document['Info'] = self.header
        document['Resource'] = self.body_data

        with io.open(LEGISLATURE_FILE, 'w', encoding='utf8') as out_file:
            json.dump(document, out_file, ensure_ascii=False)
