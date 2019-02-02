# -*- coding:utf-8 -*-
import csv

from .elected import Elected
from .agent import  Agent

RESULTS_FILE = './files/candidatos+resultados+2018.csv'


class ElectionResults:
    POSTS = ['SENADOR', 'DEPUTADO FEDERAL']
    ELECTED_FLAGS = ['ELEITO', 'ELEITO POR MEDIA', 'ELEITO POR QP']

    def __init__(self):
        self.elected = []
        self.ontology = Agent()

        with open(RESULTS_FILE, 'rt') as csvfile:
            spamreader = csv.DictReader(csvfile, delimiter=',')
            for row in spamreader:
                self.add_elected(Elected(row))

    def add_elected(self, elected):
        if elected.post in self.POSTS and elected.shift in self.ELECTED_FLAGS:
            self.elected.append(elected)
            # self.populate_post(elected)

    def get_all_elected(self):
        return self.elected

    def populate_post(self, elected):
        self.ontology.new_jurisdiction(elected.electoral_unity)
        self.ontology.new_post(elected)
