# -*- coding:utf-8 -*-
import xml.etree.ElementTree as ET
import csv
import glob
import uuid


class Tabelao:
    def __init__(self):
        self.deputados = []
        self.senadores = []

    def adiciona_deputado(self, deputado):
        self.deputados.append(deputado)

    def procura_deputado(self, nome_parlamentar_atual):
        for deputado in self.deputados:
            if deputado.nome_parlamentar_atual == nome_parlamentar_atual:
                return deputado
        return None

    def adiciona_senador(self, senador):
        self.deputados.append(senador)

    def procura_senador(self, senador):
        pass

    def carrega_deputados(self):
        with open('./identity.csv', 'rb') as csvfile:
            spamreader = csv.DictReader(csvfile, delimiter=';')
            for row in spamreader:
                if row.get('cam:ideCadastro'):
                    self.adiciona_deputado(Deputado(row))
        return self.deputados

    def carrega_senadores(self):
        with open('./identity.csv', 'rb') as csvfile:
            spamreader = csv.DictReader(csvfile, delimiter=';')
            for row in spamreader:
                if row.get('sen:CodigoParlamentar'):
                    self.adiciona_senador(Senador(row))
        return self.senadores

    def carrega_membros_congresso(self):
        return self.carrega_deputados(), self.carrega_senadores()


class Deputado:

    def __init__(self, data):
        self.posicao = 'DEPUTADO'
        self.resource_uri = data.get('slp:resource_uri', '')
        self.data_falecimento = data.get('cam:dataFalecimento', '')
        self.data_nascimento = data.get('cam:dataNascimento', '')
        self.id_cadastro = data.get('cam:ideCadastro', '')
        self.nome_civil = data.get('cam:nomeCivil', '')
        self.nome_parlamentar_atual = data.get('cam:nomeParlamentarAtual', '')

    def __repr__(self):
        return "{nome_civil}".format(nome_civil=self.nome_civil)


class Senador:

    def __init__(self, data):
        self.posicao = 'SENADOR'
        self.resource_uri = data.get('slp:resource_uri', '')
        self.codigo_parlamentar = data.get('sen:CodigoParlamentar', '')
        self.nome_completo_parlamentar = data.get('sen:NomeCompletoParlamentar', '')
        self.nome_parlamentar = data.get('sen:NomeParlamentar', '')

    def __repr__(self):
        return "{nome_completo_parlamentar}".format(nome_completo_parlamentar=self.nome_completo_parlamentar)


if __name__ == '__main__':
    tabelao = Tabelao()
    deputados = tabelao.carrega_deputados()

    xml_files = glob.glob('./dados_deputados' + '/*.xml')
    xml_element_tree = None

    for xml_file in xml_files:
        tree = ET.parse(xml_file)
        root = tree.getroot().find('dados')

        for deputado in root.findall('deputado_'):
            nome_deputado = deputado.find('nome').text
            dados_deputado_tabelao = tabelao.procura_deputado(nome_deputado)

            if dados_deputado_tabelao:
                guid = dados_deputado_tabelao.resource_uri
            else:
                guid = str(uuid.uuid4())
                ET.SubElement(deputado, 'guid').text = guid

        tree.write(xml_file)
