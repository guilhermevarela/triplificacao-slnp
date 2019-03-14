## Ajuda
all: help

## Comandos disponíveis
help:
	@echo
	@printf "Targets available:\n\n"
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "%-35s%s\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)
	@echo

## Importa os deputados e senadores eleitos
run:
	python -m congressman_importer.cli import-all-elected

## Scrapes congressmen from site
scrape:
	python -m congressman_importer.cli scrape-deputies

## Updates congressmen using both import-all-elected data and scrape-deputies data
update:
	python -m congressman_importer.cli update-deputies	

## Instala as dependêncis do projeto
setup:
	pip install -r requirements.txt

## Executa a suite de testes
test:
	python -m pytest
