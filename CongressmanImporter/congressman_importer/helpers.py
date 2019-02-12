# -*- coding:utf-8 -*-

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
    from datetime import datetime

    timestamp = time.time()
    return datetime.fromtimestamp(timestamp).strftime(string_format)
