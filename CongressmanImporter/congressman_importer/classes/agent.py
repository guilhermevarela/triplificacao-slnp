# -*- coding:utf-8 -*-
r"""Agent objects

This module provides a object according to an ontology specified in T_BOX_PATH. In this ontology you can:

    1. Add all jurisdictions based on JURISDICTION_LIST content, in the context of this usage all jurisdictions belong to
    electoral unities in Brasil.

    2. Add specific jurisdiction based on jurisdiction name.

    3. Add a post based on an existing jurisdiction.

"""

from rdflib import URIRef, Namespace, RDF, Graph, Literal, XSD

from ..helpers import generate_timestamp

__author__ = 'Rebeca Bordini <bordini.rebeca@gmail.com>'

T_BOX_PATH = './ontology/agent-180422.owl'
A_BOX_PATH = './generated-data/instances-{timestamp}.owl'.format(timestamp=generate_timestamp(string_format='%y%m%d'))

NAMESPACE = Namespace('http://www.w3.org/ns/org#')
SCHEMA_ORG_NAMESPACE = Namespace('http://schema.org/')

POST_IRI_PREFIX ='http://www.w3.org/ns/org#Post'
FEATURE_IRI_PREFIX = 'http://www.geonames.org/ontology#Feature'
SNLP_IRI_PREFIX = 'http://www.seliganapolitica.org/resource'

JURISDICTION_LIST = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT',
                     'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO']

START_DATE="2019-02-01"
END_DATE="2024-01-31"


class Agent:
    def __init__(self):
        self.graph = Graph()
        self.graph.load(T_BOX_PATH, format='n3')

    def save(self):
        self.graph.serialize(A_BOX_PATH, format='n3')

    def add_all_jurisdictions(self):
        """
            Add all jurisdictions based on JURISDICTION_LIST content, in the context of this usage all jurisdictions belong to
            electoral unities in Brasil.
        """
        for jurisdiction in JURISDICTION_LIST:
            self.new_jurisdiction(jurisdiction)

    def new_jurisdiction(self, jurisdiction):
        """
        Add a jurisdiction instance in ontology in the following form: http://www.geonames.org/ontology#Feature/:param

        :param jurisdiction:

        """
        jurisdiction_uri = URIRef('{prefix}/{initials}'.format(prefix=FEATURE_IRI_PREFIX, initials=jurisdiction))
        self.graph.add((jurisdiction_uri, RDF.type, NAMESPACE['geonames:Feature']))

    def new_post(self, elected, uri):
        """
        Add a post based on an existing jurisdiction :param.electoral_unity.

        :param elected: Instance of Elected class
        :param uri: An uuid
        """

        jurisdiction = elected.electoral_unity

        post_uri = URIRef('{prefix}/{uuid}'.format(prefix=POST_IRI_PREFIX, uuid=uri))
        jurisdiction_uri = URIRef('{prefix}/{initials}'.format(prefix=FEATURE_IRI_PREFIX, initials=jurisdiction))

        self.graph.add((post_uri, RDF.type, NAMESPACE['Post']))
        self.graph.add((post_uri, NAMESPACE['hasJurisdiction'], jurisdiction_uri))

        literal_start_date = Literal(START_DATE, datatype=XSD.date)
        literal_end_date = Literal(END_DATE, datatype=XSD.date)
        self.graph.add((post_uri, SCHEMA_ORG_NAMESPACE['startDate'], literal_start_date))
        self.graph.add((post_uri, SCHEMA_ORG_NAMESPACE['endDate'], literal_end_date))
