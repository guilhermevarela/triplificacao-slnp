# -*- coding:utf-8 -*-
from rdflib import BNode, ConjunctiveGraph, URIRef, Literal, Namespace, RDF, Graph

from .helpers import generate_uri

ONTOLOGY_PATH = './ontology/agent-180422.owl'
NAMESPACE = Namespace('http://www.w3.org/ns/org#')


class Agent:
    def __init__(self):
        self.graph = Graph()
        self.graph.load(ONTOLOGY_PATH, format='n3')

    def save(self):
        self.graph.serialize(ONTOLOGY_PATH, format='n3')

    def new_jurisdiction(self, jurisdiction_name):
        self.graph.add(jurisdiction_name, RDF.type, NAMESPACE['geonames'])

    def new_post(self, jurisdiction_name):
        post_uri = URIRef(generate_uri())
        self.graph.add(post_uri, RDF.type, NAMESPACE['Post'])
        self.graph.add((post_uri, NAMESPACE['hasJurisdiction'], Literal(jurisdiction_name)))
        self.save()
