# Legislature Importer

## Estrutura do projeto

- [[generated-data]](https://github.com/rebecabordini/triplificacao-slnp/tree/master/Legislature%20Importer/generated-data) Contém o resultado final da execução do projeto.
	 * [[identity-final.json]](https://github.com/rebecabordini/triplificacao-slnp/blob/master/Legislature%20Importer/generated-data/identity_final.csv) Consolidação dos deputados eleitos nas útlimas eleições com os eleitos em 2018, com os seus respectivos identificadores únicos.
 	* [[legislature_56.json]](https://raw.githubusercontent.com/rebecabordini/triplificacao-slnp/master/Legislature%20Importer/generated-data/legislature_56.json) Consolidação dos eleitos em 2018 e as suas respectivas instâncias de *Post* dentro da ontologia **POLARE**.
- [[initial-data]](https://github.com/rebecabordini/triplificacao-slnp/tree/master/Legislature%20Importer/initial-data) Contém os arquivos necessários para a execução do projeto.
	* [[candidatos+resultados+2018.csv]](https://github.com/rebecabordini/triplificacao-slnp/blob/master/Legislature%20Importer/initial-data/candidatos%2Bresultados%2B2018.csv) Contém todos os candidatos às eleições 2018.
	* [[identity.csv]](https://github.com/rebecabordini/triplificacao-slnp/blob/master/Legislature%20Importer/initial-data/identity.csv) Contém todas as pessoas que já foram cadastradas previamente na ontologia **POLARE** e os seus respectivos identificadores únicos.
- [[legislature-importer]](https://github.com/rebecabordini/triplificacao-slnp/tree/master/Legislature%20Importer/legislature_importer) Pasta do módulo do projeto
- [[ontology]](https://github.com/rebecabordini/triplificacao-slnp/tree/master/Legislature%20Importer/ontology) Contém a ontologia original 
	* [[agent-180422.owl]](https://github.com/rebecabordini/triplificacao-slnp/blob/master/Legislature%20Importer/ontology/agent-180422.owl) Ontologia **POLARE** original no formato *.owl*. Obs.: no momento em que o projeto for executado esse arquivo será alterado para conter as instâncias da classe *Post* geradas automaticamente pelo [legislature_importer](https://github.com/rebecabordini/triplificacao-slnp/tree/master/Legislature%20Importer/legislature_importer).


## Conjunto de passos a ser executado

1. A etapa inicial consiste em criar dinamicamente todas as instâncias da classe *Post* representando cada uma das vagas para Deputado Federal e Senador, totalizando respectivamente 513 e 81 instâncias, e um estado brasileiro associado a cada uma dessas instâncias.

2. A segunda etapa consiste em consultar a tabela de identificadores pelo nome civil do candidato e caso o candidato não conste, gerar uma nova entrada com uma nova URI.

3. Criar um JSON com uma entrada para politico, incluindo a sua URI e associar a instância de *Post* criada previamente.

Obs.: Esse JSON é utilizado a posteriori para gerar um mapeamento na ferramenta [Karma](https://usc-isi-i2.github.io/karma/) para a ontologia [agents.owl](https://github.com/rebecabordini/triplificacao-slnp/blob/master/Legislature%20Importer/ontology/agent-180422.owl).

## Dependências do projeto
	
`python3`

## Instalação do projeto
```
git clone git@github.com:rebecabordini/triplificacao-slnp.git
cd triplificacao-slnp/
make setup
```

## Executando o projeto
`make run`
