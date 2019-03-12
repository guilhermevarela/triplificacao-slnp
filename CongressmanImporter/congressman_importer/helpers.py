# -*- coding:utf-8 -*-
from datetime import datetime, timedelta

__author__ = 'Rebeca Bordini <bordini.rebeca@gmail.com>'

def generate_uuid():
    """
        Return a randon UUID in the form: '16fd2706-8baf-433b-82eb-8c7fada847da'
    """
    import uuid
    return str(uuid.uuid4())


def generate_timestamp(string_format='%d-%m-%Y %H:%M'):
    """
    Return the actual time based on the format %d-%m-%Y %H:%M
    """
    import time    

    timestamp = time.time()
    return datetime.fromtimestamp(timestamp).strftime(string_format)

def generate_legislature_iterator():
    """
        Makes a date iterator class for legislatura
    """
    import glob

    class LegislaturaIterator:
        def __init__(self):
            # API: updated until yesterday
            yesterday = datetime.now().replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0
            ) - timedelta(1)

            # Define lowest date            
            scrapped_list = glob.glob('scrapped-data/legislature_56_*.json')
            if scrapped_list:
                low = max([
                    f.split('_')[-1].split('.')[0]
                    for f in scrapped_list
                ])
                low = datetime.strptime(low, '%Y-%m-%d') + timedelta(1)
            else:
                low = datetime.strptime('2019-02-02', '%Y-%m-%d')
            
            self.current = low                        
            self.high = min(yesterday, datetime.strptime('2023-01-31', '%Y-%m-%d'))

        def __iter__(self):
            return self

        def __next__(self): # Python 3: def __next__(self)
            if self.current > self.high:
                raise StopIteration
            else:
                self.current += timedelta(1)
                return self.current - timedelta(1)
    return LegislaturaIterator()