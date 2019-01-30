# -*- coding:utf-8 -*-
import csv

from elected import Elected

RESULTS_FILE = './files/candidatos+resultados+2018.csv'


class ElectionResults:
    POSTS = ['SENADOR', 'DEPUTADO FEDERAL']
    ELECTED_FLAGS = ['ELEITO', 'ELEITO POR MEDIA', 'ELEITO POR QP']

    def __init__(self):
        self.elected = []

        with open(RESULTS_FILE, 'rb') as csvfile:
            spamreader = csv.DictReader(csvfile, delimiter=',')
            for row in spamreader:
                self.add_elected(Elected(row))

    def add_elected(self, elected):
        if elected.post in self.POSTS and elected.shift in self.ELECTED_FLAGS:
            self.elected.append(elected)

    def get_all_elected(self):
        return self.elected
