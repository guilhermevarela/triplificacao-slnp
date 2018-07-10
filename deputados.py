# -*- coding:utf-8 -*-
import xml.etree.ElementTree as ET
import csv
import glob
import uuid


class Deputado:

    def __init__(self, data):
        self.resource_uri = data.get('slp:resource_uri', '')
        self.data_falecimento = data.get('cam:dataFalecimento', '')
        self.data_nascimento = data.get('cam:dataNascimento', '')
        self.id_cadastro = data.get('cam:ideCadastro', '')
        self.nome_civil = data.get('cam:nomeCivil', '')
        self.nome_parlamentar_atual = data.get('cam:nomeParlamentarAtual', '')
        self.codigo_parlamentar = data.get('sen:CodigoParlamentar', '')
        self.nome_completo_parlamentar = data.get('sen:NomeCompletoParlamentar', '')
        self.nome_parlamentar = data.get('sen:NomeParlamentar', '')


def load_guids():
    with open('./identity.csv', 'rb') as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=';')
        deputados = []

        for row in spamreader:
            deputados.append(Deputado(row))


if __name__ == '__main__':
    load_guids()
    # xml_files = glob.glob('./dados_deputados' + '/*.xml')
    # xml_element_tree = None
    #
    # for xml_file in xml_files:
    #     tree = ET.parse(xml_file)
    #     root = tree.getroot()
    #     data = root.find('dados')
    #     guid = str(uuid.uuid4())
    #
    #     for child in data:
    #         child.set('guid', guid)
    #     tree.write(xml_file)
