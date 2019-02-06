# Triplificação Se Liga na Política
Projeto de triplificação dos dados da Câmara dos Deputados e do Senado para a Legislatura 56 (Eleições 2018).

## Arquitetura do projeto

![Arquitetura do projeto](https://raw.githubusercontent.com/rebecabordini/triplificacao-slnp/master/arquitetura.png)


## Organização do projeto

[[Karma]](https://github.com/rebecabordini/triplificacao-slnp/tree/master/Karma) Contém os arquivos referentes
ao processo de mapeamento da ferramenta [Karma](https://usc-isi-i2.github.io/karma/). Dentro dessa pasta, encontram-se dois arquivos:


- [[legislature_56.json-auto-model.ttl]](https://github.com/rebecabordini/triplificacao-slnp/blob/master/Karma/legislature_56.json-auto-model.ttl)
Consiste na descrição do mapeamento executado dentro da ferramenta

- [[ontology-applied.ttl]](https://github.com/rebecabordini/triplificacao-slnp/blob/master/Karma/ontology-applied.ttl)
Consiste no resultado da execução do processo em formato *.rdf*

[[Congressman Importer]](https://github.com/rebecabordini/triplificacao-slnp/tree/master/CongressmanImporter)
Contém um projeto Python responsável por filtrar entre todos os candidatos às eleições 2018, quais serão incluídos dentro da ontologia SLNP. A documentação relativa a ele encontra-se [aqui](https://github.com/rebecabordini/triplificacao-slnp/tree/master/CongressmanImporter/README.md).


## Referências

[[1]](https://arxiv.org/abs/1804.06015v1)  Laufer, C.; Schwabe, D.; Busson, A.; Ontologies for Representing Relations among Political Agents.
