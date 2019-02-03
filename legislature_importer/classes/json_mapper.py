# -*- coding:utf-8 -*-
import json

VERSION = '0.0.1'
LEGISLATURE_FILE = 'files/legislature_56.json'
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

    def generate_resource(self, data, uuid, post_uri, candidate_name=''):
        self.body_data.append({
            'url': '{prefix}/{uuid}'.format(prefix=SNLP_IRI_PREFIX, uuid=uuid),
            'nomeCandidato': candidate_name,
            'nomeCivil': data.name,
            'dataNascimento': data.birth_date,
            'urlPartido': '',
            'hasPost': '{prefix}/{uuid}'.format(prefix=POST_IRI_PREFIX, uuid=post_uri),
        })

    def save_file(self):
        document = {}
        document['Info'] = self.header
        document['Resource'] = self.body_data

        with open(LEGISLATURE_FILE, 'w') as out_file:
            json.dump(document, out_file)
