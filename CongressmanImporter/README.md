# Congressman Importer

## Estrutura do projeto

- [[generated-data]](https://github.com/rebecabordini/triplificacao-slnp/tree/master/CongressmanImporter/generated-data) Contém o resultado final da execução do projeto.
	 * [[identity-final.json]](https://github.com/rebecabordini/triplificacao-slnp/blob/master/CongressmanImporter/generated-data/identity_final.csv) Consolidação dos deputados eleitos nas útlimas eleições com os eleitos em 2018, com os seus respectivos identificadores únicos. O arquivo é atualizado com as identidades dos suplentes durante a execução do passo 3.
 	* [[legislature_56.json]](https://raw.githubusercontent.com/rebecabordini/triplificacao-slnp/master/CongressmanImporter/generated-data/legislature_56.json) Consolidação dos eleitos em 2018 e as suas respectivas instâncias de *Post* dentro da ontologia **POLARE**.
    * [[legislature_56_final.json]](https://raw.githubusercontent.com/rebecabordini/triplificacao-slnp/master/CongressmanImporter/generated-data/legislature_56_final.json) Consolidação dos processos de: (1) compilação dos dados da eleição 2018 (2) raspagem da movimentação de deputados (3) atualização dos recursos **Memberships** do sistema.
 	* [[instances-180212.owl]](https://raw.githubusercontent.com/rebecabordini/triplificacao-slnp/master/CongressmanImporter/generated-data/instances-190212.owl) Contém as instâncias da classe *Post* geradas automaticamente pelo [congressman_importer](https://github.com/rebecabordini/triplificacao-slnp/tree/master/CongressmanImporter/congressman_importer).
- [[initial-data]](https://github.com/rebecabordini/triplificacao-slnp/tree/master/CongressmanImporter/initial-data) Contém os arquivos necessários para a execução do projeto.
	* [[candidatos+resultados+2018.csv]](https://github.com/rebecabordini/triplificacao-slnp/blob/master/CongressmanImporter/initial-data/candidatos%2Bresultados%2B2018.csv) Contém todos os candidatos às eleições 2018.
	* [[identity.csv]](https://github.com/rebecabordini/triplificacao-slnp/blob/master/CongressmanImporter/initial-data/identity.csv) Contém todas as pessoas que já foram cadastradas previamente na ontologia **POLARE** e os seus respectivos identificadores únicos.
- [[congressman-importer]](https://github.com/rebecabordini/triplificacao-slnp/tree/master/CongressmanImporter/congressman_importer) Pasta do módulo do projeto
- [[ontology]](https://github.com/rebecabordini/triplificacao-slnp/tree/master/CongressmanImporter/ontology) Contém a ontologia original 
	* [[agent-180422.owl]](https://github.com/rebecabordini/triplificacao-slnp/blob/master/CongressmanImporter/ontology/agent-180422.owl) Ontologia **POLARE** original no formato *.owl*.
- [[scraped-data]](https://github.com/rebecabordini/triplificacao-slnp/tree/master/CongressmanImporter/scraped-data) Contém json com as movimentações dos deputados ver passo 3
- [[tests]](https://github.com/rebecabordini/triplificacao-slnp/tree/master/CongressmanImporter/tests) Contém os arquivos de teste do projeto
	* [[logs]](https://github.com/rebecabordini/triplificacao-slnp/blob/master/CongressmanImporter/tests/logs) Contém o arquivo de log da última execução dos testes
- [[assets]](https://github.com/rebecabordini/triplificacao-slnp/tree/master/CongressmanImporter/assets) Contém os assets necessários para o reltório da execução dos testes


## Conjunto de passos a ser executado

### 1. Compilação dos Dados da Eleição 2018

1.1. A etapa inicial consiste em criar dinamicamente todas as instâncias da classe *Post* representando cada uma das vagas para Deputado Federal e Senador, totalizando respectivamente 513 e 81 instâncias, e um estado brasileiro associado a cada uma dessas instâncias.

1.2. A segunda etapa consiste em consultar a tabela de identificadores pelo nome civil do candidato e caso o candidato não conste, gerar uma nova entrada com uma nova URI.

1.3. Criar um JSON com uma entrada para politico, incluindo a sua URI e associar a instância de *Post* criada previamente.

Obs.: Esse JSON é utilizado a posteriori para gerar um mapeamento na ferramenta [Karma](https://usc-isi-i2.github.io/karma/) para a ontologia [agents.owl](https://github.com/rebecabordini/triplificacao-slnp/blob/master/CongressmanImporter/ontology/agent-180422.owl).

### 2. Raspagem da movimentação dos deputados

### 3. Atualização dos recursos memberships

## Dependências do projeto
	
`python3`

## Instalação do projeto
```
git clone git@github.com:rebecabordini/triplificacao-slnp.git
cd triplificacao-slnp/
make setup
```

## Executando o passo 1
`make run` 

## Executando o passo 2
`make scrape` 

## Executando o passo 3
`make update` 

## Rodando os testes
`make test` 