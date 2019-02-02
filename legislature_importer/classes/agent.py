# -*- coding:utf-8 -*-
from rdflib import URIRef, Namespace, RDF, Graph

ONTOLOGY_PATH = './ontology/agent-180422.owl'
NAMESPACE = Namespace('http://www.w3.org/ns/org#')
FEATURE_IRI_PREFIX = 'http://www.geonames.org/ontology#Feature'
SNLP_IRI_PREFIX = 'http://www.seliganapolitica.org/resource'


class Agent:
    def __init__(self):
        self.graph = Graph()
        self.graph.load(ONTOLOGY_PATH, format='n3')

    def save(self):
        self.graph.serialize(ONTOLOGY_PATH, format='n3')

    def new_jurisdiction(self, jurisdiction):
        jurisdiction_uri = URIRef('{prefix}/{initials}'.format(prefix=FEATURE_IRI_PREFIX, initials=jurisdiction))
        self.graph.add((jurisdiction_uri, RDF.type, NAMESPACE['geonames:Feature']))
        self.save()

    def new_post(self, elected, uri):
        jurisdiction = elected.electoral_unity

        post_uri = URIRef('{prefix}/{uuid}'.format(prefix=SNLP_IRI_PREFIX, uuid=uri))
        jurisdiction_uri = URIRef('{prefix}/{initials}'.format(prefix=FEATURE_IRI_PREFIX, initials=jurisdiction))

        self.graph.add((post_uri, RDF.type, NAMESPACE['Post']))
        self.graph.add((post_uri, NAMESPACE['hasJurisdiction'], jurisdiction_uri))
        # self.graph.add(post_uri, NAMESPACE['held by'], elected)
        self.save()
