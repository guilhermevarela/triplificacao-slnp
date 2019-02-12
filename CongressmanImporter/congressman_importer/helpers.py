# -*- coding:utf-8 -*-

__author__ = 'Rebeca Bordini <bordini.rebeca@gmail.com>'

def generate_uuid():
    """
        Return a randon UUID in the form: '16fd2706-8baf-433b-82eb-8c7fada847da'
    """
    import uuid
    return str(uuid.uuid4())
