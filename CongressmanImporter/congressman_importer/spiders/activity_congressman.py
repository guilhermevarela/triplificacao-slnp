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
        scrapy runspider spiders/activity_congressman.py -o generated-data/legislature_56_2019-02-12.json  -a dt='12/02/2019'
http://www.camara.leg.br/internet/deputado/resultadoHistorico.asp?dt_inicial=24/02/2015&dt_final=2015-02-24&parlamentar=&histMandato=1&ordenarPor=1&Pesquisar=Pesquisar
    missing entries -- bkp2 - bkp ?? Why?
    2015-02-09 5830515
    2015-02-24 5830490
    2015-02-24 5830805
    2015-02-24 5830828
    2015-02-24 5830830
    2015-02-24 5830671
    2015-02-25 5830661
    2015-02-25 5830818
    2015-02-27 5830793
    2015-03-02 5830661
    2015-10-22 5830849
    2015-12-15 5830858
    2015-12-16 5830859
    2015-12-28 5830858
    2016-03-15 5830862
    2016-10-10 5830777
    2016-10-11 5830777
    2018-08-21 1635224
    2018-08-22 1635214
    2018-09-14 1635227
'''

__author__ = 'Guilherme Varela <guilhermevarela@hotmail.com>'

from datetime import date, datetime, timedelta
from collections import defaultdict
import re

import scrapy
import bs4


# import utils
# Example
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
        # Handle input arguments
        # legislatura = kwargs.pop('legislatura', 55)
        # start_date = kwargs.pop('start_date', None)
        # finish_date = kwargs.pop('finish_date', None)

        # import code; code.interact(local=dict(globals(), **locals()))        
        self.dt = dt
        super(scrapy.Spider, self).__init__(*args, **kwargs)

        # Process legislatura -- turn into a data interval
        # if legislatura:
        #     legislatura = int(legislatura)
        #     # 55 --> 2015-02-01, 54 --> 2011-02-01, 53 --> 2007-02-01
        #     # legislatura beginings
        #     self.start_date = utils.get_start_from(legislatura)
        #     self.start_date = utils.busday_adjust(self.start_date + timedelta(days=1))
        #     if not finish_date:
        #         self.finish_date = min(utils.get_finish_from(legislatura), date.today())
        #     else:
        #         self.finish_date = utils.busday_adjust(finish_date)

        #     self.legislatura = legislatura

        # elif start_date:
        #     start_date = datetime.strptime(start_date, '%Y-%m-%d')
        #     self.start_date = utils.busday_adjust(start_date)
        #     if not finish_date:
        #         finish_date = utils.busday_adjust(self.start_date + timedelta(days=1))
        #         self.finish_date = finish_date
        #     else:
        #         self.finish_date = utils.busday_adjust(finish_date)
        # else:
        #     err = 'Either `legislatura` or `start_date` must be provided'
        #     raise ValueError(err)

        self.data = defaultdict(dict)

    def start_requests(self):
        '''
            Stage 1: Request first term dates
        '''
        # sd = self.start_date.strftime('%d/%m/%Y')
        # fd = self.finish_date.strftime('%d/%m/%Y')
        # sd = self.start_date
        # fd = self.finish_date
        # dt = self.dt.strftime('%d/%m/%Y')
        dt = self.dt

        # for dt in utils.busdays_range(sd, fd):
        #     startDate = dt.strftime('%d/%m/%Y')


        #     q = QUERY_STR.format(startDate, startDate)
        #     url = '{:}{:}'.format(ACTIVITY_URL, q)

        #     req = scrapy.Request(
        #         url,
        #         self.activity_congressmen,
        #         headers={'accept': 'application/json'},
        #         meta={'dt': startDate}
        #     )
        #     yield req
        # for dt in utils.busdays_range(sd, fd):
        #     startDate = dt.strftime('%d/%m/%Y')


        q = QUERY_STR.format(dt, dt)
        url = '{:}{:}'.format(ACTIVITY_URL, q)

        req = scrapy.Request(
            url,
            self.activity_congressmen,
            headers={'accept': 'application/json'}
            # meta={'dt': startDate}
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
        data = {}
        # d, m, y = self.dt.split('/')
        # data['dt'] = f'{y}-{m}-{d}'
        # import code; code.interact(local=dict(globals(), **locals()))
        data['refDate'] = self.dt

        # import code; code.interact(local=dict(globals(), **locals()))

        for tag in soup.find(id='content').children:
            # a tag href ideCadastro -- content NomeParlamentarAtual
            info = getattr(tag, 'a', None)
            if info is not None:
                data['id_api'] = info['href'].split('/')[-1]
                data['nomeCandidato'] = info.contents[0]

            # This block reads the contents of the message and assigns
            # entry of exit
            info = getattr(tag, 'li', None)
            if info is not None:
                # gets everything up to the first parenthesis
                # (.*)\(
                contents = re.sub(r'[\r|\t|\n]', '', info.contents[0])
                activity = re.search(r'(.*)\(', contents).group(0)
                # grebs everything enclosed in parenthesis
                activity_detail = re.search(r'\((.*)\)', contents).group(0)
                # import code; code.interact(local=dict(globals(), **locals()))
                if (('Reassunção' in activity) or ('Posse' in activity) or ('Afastamento' in activity_detail)):
                    data['startDate'] = data['refDate']

                elif (('Posse' in activity_detail) or ('Reassunção' in activity_detail) or ('Afastamento' in activity)):
                    data['finishDate'] = data['refDate']
                
                data['message'] = contents
                
                id_api = data['id_api']
                if id_api in self.data:
                    if self.data[id_api]:
                        data['nomeCandidato'] = self.data[id_api]['nomeCandidato']
                        data['id_congressman'] = self.data[id_api]['id_congressman']

                    yield data
                else:                    
                    url = '{url}dep_Detalhe.asp?id={id}'.format(
                        url=CAMARA_URL,
                        id=id_api
                    )
                    req = scrapy.Request(
                        url,
                        self.congressman_info,
                        headers={'accept': 'application/json'},
                        meta={'activity': data, 'url' : url},
                        dont_filter=True
                    )
                    yield req

                data = {}
                data['dt'] = self.dt
                # data['dt'] = '{:year}-{:month}-{:day}'.format(
                #     day=d, month=m, year=y
                # )

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
        data = response.meta['activity']
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
        # import code; code.interact(local=dict(globals(), **locals()))
        # TO DO 
        # * QUERY / CREATE MEMBERSHIP
        # * QUERY POST
        # * QUERY PERSON
        # garantees that one name is being passed along
        # import code; code.interact(local=dict(globals(), **locals()))
        del data['id_api']
        del data['refDate']
        yield data