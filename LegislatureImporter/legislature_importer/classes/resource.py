# -*- coding:utf-8 -*-
r"""Resource objects

This module provides a object to represent a resource.

"""

__author__ = 'Rebeca Bordini <bordini.rebeca@gmail.com>'

POST_IRI_PREFIX = 'http://www.w3.org/ns/org#Post'
SNLP_IRI_PREFIX = 'http://www.seliganapolitica.org/resource'


class Resource:
    def __init__(self, elected, elected_uri, post_uri, party_uri, candidate_name=''):
        self.url = '{prefix}/{uuid}'.format(prefix=SNLP_IRI_PREFIX, uuid=elected_uri)
        self.candidate_name = candidate_name
        self.civil_name = elected.name
        self.birth_date = elected.birth_date
        self.party_url = party_uri
        self.hasPost = '{prefix}/{uuid}'.format(prefix=POST_IRI_PREFIX, uuid=post_uri)
