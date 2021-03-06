# -*- coding: utf-8 -*-
'''
    Date: Nov 9th, 2018
    Author: Guilherme Varela
    
    References:
        https://doc.scrapy.org/en/1.4/intro/tutorial.html#intro-tutorial
    
    Shell:
        scrapy shell 'https://www.camara.leg.br/internet/deputado/resultadoHistorico.asp?dt_inicial=12/2/2019&dt_final=12/2/2019&parlamentar=&histMandato=1&filiacaoPartidaria=1&mudancaNomePart=1&histLideranca=1&comisPermanente=1&comisTemporaria=1&ordenarPor=1&Pesquisar=Pesquisar'
        scrapy shell 'http://www.camara.leg.br/internet/deputado/dep_Detalhe.asp?id=5830803'
    
    CommandLine:
        From the folder congressman_importer run:
        scrapy runspider spiders/activity_congressman.py -o ../scrapped-data/legislature_56_2019-02-05.json  -a dt='2019-02-05'

'''

__author__ = 'Guilherme Varela <guilhermevarela@hotmail.com>'
from datetime import datetime
import re
import scrapy
import bs4

# CAMARA_URL = 'http://www.camara.leg.br/internet/deputado/resultadoHistorico.asp?dt_inicial=02%2F02%2F2015&dt_final=03%2F02%2F2015&parlamentar=&histMandato=1&ordenarPor=1&Pesquisar=Pesquisar'
CAMARA_URL = 'http://www.camara.leg.br/internet/deputado/'
ACTIVITY_URL = '{:}resultadoHistorico.asp'.format(CAMARA_URL)
QUERY_STR = '?dt_inicial={:}&dt_final={:}&parlamentar=&histMandato=1&ordenarPor=1&Pesquisar=Pesquisar'

class ActivityCongressmanSpider(scrapy.Spider):
    name = 'activity_congressmen'

    # Overwrites default: ASCII
    custom_settings = {
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def __init__(self, dt, *args, **kwargs):
        self.dt = datetime.strptime(dt, '%Y-%m-%d')
        super(scrapy.Spider, self).__init__(*args, **kwargs)

    def start_requests(self):
        '''
            Stage 1: Request first term dates
        '''
        dt = self.dt.strftime('%Y-%m-%d')

        q = QUERY_STR.format(dt, dt)
        url = '{:}{:}'.format(ACTIVITY_URL, q)

        req = scrapy.Request(
            url,
            self.activity_congressmen,
            headers={'accept': 'application/json'}
        )
        yield req

    def activity_congressmen(self, response):
        '''Fetches the camara activity -- nomination of posts

        Example:
            http://www.camara.leg.br/internet/deputado/resultadoHistorico.asp?dt_inicial=03/02/2015&dt_final=03/02/2015&parlamentar=&histMandato=1&ordenarPor=1&Pesquisar=Pesquisa

        Arguments:
            response {[type]} -- [description]
        '''
        soup = bs4.BeautifulSoup(response.body_as_unicode(), features='lxml')
        for tag in soup.find(id='content').children:
            # a tag href ideCadastro -- content NomeParlamentarAtual
            info = getattr(tag, 'a', None)
            if info is not None:
                data = {}
                id_api = info['href'].split('/')[-1]
                data['nomeCandidato'] = info.contents[0]

            # This block captures PARTY NAME and jurisdiction
            info = getattr(tag, 'h4', None)
            if info is not None:
                party_info = re.search(r'- (.*?)<\/h4>', str(info)).group(1)
                data['party']  = party_info.split('/')[0]
                data['jurisdiction'] = party_info.split('/')[1].strip()

            # This block reads the contents of the message and assigns
            info = getattr(tag, 'li', None)
            if info is not None:
                contents = re.sub(r'[\r|\t|\n]', '', info.contents[0])
                # gets everything up to the first parenthesis
                # activity = re.search(r'(.*)\(', contents).group(0)
                event = re.search(r'- (.*)\(', contents).group(1)
                # grabs everything enclosed in parenthesis
                event_complement = re.search(r'\((.*)\)', contents).group(1)

                if (('Reassunção' in event) or ('Posse' in event) or ('Afastamento' in event_complement)):

                    data['startDate'] = self.dt.strftime('%Y-%m-%d')
                    # The event is someone starting a new membership
                    data['status'] = event

                elif (('Posse' in event_complement) or ('Reassunção' in event_complement) or ('Afastamento' in activity)):
                    data['finishDate'] = self.dt.strftime('%Y-%m-%d')
                    # The event is someone leaving office
                    data['motive'] = event

                data['replacement'] = re.search(r'- (.*) -', event_complement).group(1)
                if data['replacement'] == '':
                    data['replacement'] = None

                data['message'] = contents
                url = '{url}dep_Detalhe.asp?id={id}'.format(
                    url=CAMARA_URL,
                    id=id_api
                )
                req = scrapy.Request(
                    url,
                    self.congressman_info,
                    headers={'accept': 'application/json'},
                    meta={'data': data, 'url' : url},
                    dont_filter=True
                )
                yield req


    def congressman_info(self, response):
        '''Fetches full name from congressman
        activity page has information using internal names and not 
        birth names leading to dynamic information and possibly
        identity mismatchs -- fetches only the names
        Example:
            http://www.camara.leg.br/internet/deputado/dep_Detalhe.asp?id=5830803
        Arguments:
            response {[type]} -- [description]
        '''
        soup = bs4.BeautifulSoup(response.body_as_unicode(), features='lxml')
        data = response.meta['data']
        ul = soup.find('ul', {'class': 'informacoes-deputado'})
        if ul is not None:
            exit_loop = False
            for li in ul.children:
                if isinstance(li, bs4.element.Tag):
                    for el in li.contents:
                        if isinstance(el, bs4.element.Tag): # span div
                            if 'Nome Civil:' in el.contents:
                                key = 'nomeCivil'
                            elif 'Data de Nascimento:' in el.contents:
                                key = 'dataNascimento'
                            else:
                                key = None
                        if isinstance(el, bs4.element.NavigableString): # contents
                            val = el.strip()
                    if key:
                        if key == 'dataNascimento':
                            data[key] = '{yr}-{mt}-{dd}'.format(
                                yr=val[-4:],
                                mt=val[3:5],
                                dd=val[:2],
                            )
                        else:
                            data[key] = val
                    exit_loop = 'nomeCivil' in data and 'dataNascimento' in data
                    if exit_loop:
                        yield data
                        return