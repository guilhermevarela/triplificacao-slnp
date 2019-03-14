# -*- coding:utf-8 -*-
r"""Election Results objects

This module provides a object to represent all Senators and Federal Deputies elected based on the results of last election
located in RESULTS_FILE constant. All data present in this file were extracted from TSE.

Based on the contract to be elected a candidate must be elected with one of the following flags: ELEITO, ELEITO POR MEDIA
or ELEITO POR QP.

"""

import csv

from .elected import Elected
from .agent import  Agent

__author__ = 'Rebeca Bordini <bordini.rebeca@gmail.com>'

RESULTS_FILE = './initial-data/candidatos+resultados+2018.csv'


class ElectionResults:
    POSTS = ['SENADOR', 'DEPUTADO FEDERAL']
    ELECTED_FLAGS = ['ELEITO', 'ELEITO POR MEDIA', 'ELEITO POR QP']

    def __init__(self):
        """
        Add all candidates for Senators and Federal Deputies elected based on the results of last election
        """
        self.elected = []
        self.ontology = Agent()

        with open(RESULTS_FILE, 'rt') as csvfile:
            spamreader = csv.DictReader(csvfile, delimiter=',')
            for row in spamreader:
                self.add_elected(Elected(row))

    def add_elected(self, elected):
        """
        Add the candidate to self.elected list if he ran for the positions of deputy or senator and if he was elected based on the following
        flags:  ELEITO, ELEITO POR MEDIA
        :param elected: Instance of Elected class
        """
        if elected.post in self.POSTS and elected.shift in self.ELECTED_FLAGS:
            elected.birth_date = '{yr}-{mt}-{dd}'.format(
                yr=elected.birth_date[-4:],
                mt=elected.birth_date[3:5],
                dd=elected.birth_date[:2],
            )
            self.elected.append(elected)

    def get_all_elected(self):
        """
        :return: All elected candidates
        """
        return self.elected
