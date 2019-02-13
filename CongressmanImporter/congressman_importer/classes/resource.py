# -*- coding:utf-8 -*-
r"""Resource objects

This module provides a object to represent a resource.

"""

__author__ = 'Rebeca Bordini <bordini.rebeca@gmail.com>'

POST_IRI_PREFIX = 'http://www.w3.org/ns/org#Post'
MEMBERSHIP_IRI_PREFIX = 'http://www.w3.org/ns/org#Membership'
SNLP_IRI_PREFIX = 'http://www.seliganapolitica.org/resource'
START_DATE = "2019-02-01"


class Resource:
    def __init__(self, elected, elected_uuid, post_uuid, party_uri, membership_uuid, candidate_name=''):
        self.url = '{prefix}/{uuid}'.format(prefix=SNLP_IRI_PREFIX, uuid=elected_uuid)
        self.candidate_name = candidate_name
        self.civil_name = elected.name
        self.birth_date = elected.birth_date
        self.party_url = party_uri
        self.membershipUri = '{prefix}/{uuid}'.format(prefix=MEMBERSHIP_IRI_PREFIX, uuid=membership_uuid)
        self.postUri = '{prefix}/{uuid}'.format(prefix=POST_IRI_PREFIX, uuid=post_uuid)
