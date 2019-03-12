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

from datetime import date, datetime, timedelta
import re

import scrapy
import bs4


# import utils
# CAMARA_URL = 'http://www.camara.leg.br/internet/deputado/resultadoHistorico.asp?dt_inicial=02%2F02%2F2015&dt_final=03%2F02%2F2015&parlamentar=&histMandato=1&ordenarPor=1&Pesquisar=Pesquisar'
CAMARA_URL = 'http://www.camara.leg.br/internet/deputado/'
ACTIVITY_URL = '{:}resultadoHistorico.asp'.format(CAMARA_URL)
QUERY_STR = '?dt_inicial={:}&dt_final={:}&parlamentar=&histMandato=1&ordenarPor=1&Pesquisar=Pesquisar'

# Use settings on lauching crawlers from shell or python scripts
def get_spider_settings(feed_uri):
    return {
        'FEED_EXPORT_ENCODING': 'utf-8',
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'FEED_URI': feed_uri
    }

class ActivityCongressmanSpider(scrapy.Spider):
    name = 'activity_congressmen'

    # Overwrites default: ASCII
    custom_settings = {
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def __init__(self, dt, *args, **kwargs):
        self.dt = dt
        super(scrapy.Spider, self).__init__(*args, **kwargs)

    def start_requests(self):
        '''
            Stage 1: Request first term dates
        '''
        dt = self.dt

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

            # This block reads the contents of the message and assigns
            # entry of exit
            info = getattr(tag, 'li', None)
            if info is not None:
                contents = re.sub(r'[\r|\t|\n]', '', info.contents[0])
                # gets everything up to the first parenthesis
                activity = re.search(r'(.*)\(', contents).group(0)
                # grabs everything enclosed in parenthesis
                activity_detail = re.search(r'\((.*)\)', contents).group(0)

                if (('Reassunção' in activity) or ('Posse' in activity) or ('Afastamento' in activity_detail)):
                    data['startDate'] = self.dt

                elif (('Posse' in activity_detail) or ('Reassunção' in activity_detail) or ('Afastamento' in activity)):
                    data['finishDate'] = self.dt

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
            for li in ul.children:
                if isinstance(li, bs4.element.Tag):
                    for el in li.contents:
                        if isinstance(el, bs4.element.Tag): # span div
                            if 'Nome Civil:' in el.contents:
                                key = 'nomeCivil'
                            if 'Data de Nascimento:' in el.contents:
                                key = 'dataNascimento'
                        if isinstance(el, bs4.element.NavigableString): # contents
                            val = el.strip()
                    data[key] = val
                    if 'nomeCivil' in data and 'dataNascimento' in data:
                        break
        yield data