# -*- coding:utf-8 -*-
import csv
from dateutil.parser import parse

from .deputy import Deputy
from .senator import Senator


IDENTITY_FILE = './generated-data/identity_final.csv'


class Identity:
    def __init__(self):
        self.deputies = []
        self.senators = []

        with open('./initial-data/identity.csv', 'rt') as csvfile:
            spamreader = csv.DictReader(csvfile, delimiter=';')
            for row in spamreader:
                if row.get('cam:ideCadastro'):
                    self.add_deputy(Deputy(row))
                if row.get('sen:CodigoParlamentar'):
                    self.add_senator(Senator(row))

    def add_deputy(self, deputy):
        self.deputies.append(deputy)

    def add_senator(self, senator):
        self.senators.append(senator)

    def find(self, name):
        congressman_list = self.deputies + self.senators
        for congressman in congressman_list:
            if congressman.name == name:
                return congressman
        return None

    def get_all_deputies(self):
        return self.deputies

    def get_all_senators(self):
        return self.senators

    def update_data(self, uri, data):
        with open(IDENTITY_FILE, 'a') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';')
            formated_birth_date = parse(data.birth_date)
            spamwriter.writerow([uri, '', formated_birth_date.strftime('%Y-%m-%d'), '', data.name, '', '', '', ''])
