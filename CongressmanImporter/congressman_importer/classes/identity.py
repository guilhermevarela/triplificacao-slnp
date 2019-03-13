# -*- coding:utf-8 -*-
r"""Identify objects

This module provides a object to represent all Senators and Federal Deputies elected in previously elections, with his
unique identifiers based on a .csv file located in IDENTITY_FILE location.

This module also provide a way to update the content of the IDENTITY_FILE, in the purpose of this usage a copy is made
located in IDENTITY_FILE_UPDATED location.

"""


import csv
from dateutil.parser import parse

from .deputy import Deputy
from .senator import Senator

__author__ = 'Rebeca Bordini <bordini.rebeca@gmail.com>'

IDENTITY_FILE = './initial-data/identity.csv'
IDENTITY_FILE_UPDATED = './generated-data/identity_final.csv'


class Identity:
    def __init__(self, updated=False):
        """
        Add all candidates of previous elections present in IDENTITY_FILE
        """
        self.deputies = []
        self.senators = []

        if updated:
            file = IDENTITY_FILE_UPDATED
        else:
            file = IDENTITY_FILE

        with open(file, 'rt') as csvfile:
            spamreader = csv.DictReader(csvfile, delimiter=';')
            for row in spamreader:
                # Senators and deputies has different contracts
                # TODO: CREATE ANOTHER FEATURE TELLING SENATORS vs DEPUTIES
                if row.get('sen:CodigoParlamentar') or 'senador' in row.get('post', '').lower():
                    self.add_senator(Senator(row))

                if row.get('cam:ideCadastro') or 'deputado' in row.get('post', '').lower():
                    self.add_deputy(Deputy(row))

    def add_deputy(self, deputy):
        """
        Adds a deputy to deputies_list
        :param deputy:
        """
        self.deputies.append(deputy)

    def add_senator(self, senator):
        """
        Adds a senator to senator_list
        :param senator:
        """
        self.senators.append(senator)

    def find(self, name):
        """
        Look for a congressman based on his name
        :param name:
        :return:
        """
        congressman_list = self.deputies + self.senators
        for congressman in congressman_list:
            if congressman.name == name:
                return congressman
        return None

    def get_all_deputies(self):
        """
        :return: all deputies
        """
        return self.deputies

    def get_all_senators(self):
        """
        :return: all senators
        """
        return self.senators

    def update_data(self, uri, data):
        """
        Update the content of the IDENTITY_FILE, in the purpose of this usage a copy is made
        located in IDENTITY_FILE_UPDATED and the new data is appended. Is not necessary save the file. One row is writed
        per function call.

        :param uri: The unique identifier of the current congressman
        :param data: Elected instance
        """
        if 'deputado' in data.post.lower():

            deputy = self.find(data.name)

            if deputy is None:
                deputy = Deputy()

            deputy.update_data(uri, data)

            self.add_deputy(deputy)

        elif 'senador' in data.post.lower():
            senator = self.find(data.name)

            if senator is None:

                senator = Senator()

            senator.update_data(uri, data)
            self.add_senator(senator)

        else:
            raise ValueError('Unhandled data with post {}'.format(data.post))

    def save_file(self):
        """
            Saves a file which integrates all congressman
        """
        # paginate over deputies and senators getting their fields
        fieldnames = set([])
        congressmen = self.deputies + self.senators
        for data in congressmen:
            fieldnames = fieldnames.union(data.dump().keys())


        with open(IDENTITY_FILE_UPDATED, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=list(fieldnames), delimiter=';')
            writer.writeheader()

            for data in congressmen:
                writer.writerow(data.dump())
