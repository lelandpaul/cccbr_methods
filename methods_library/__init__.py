from .models import *
from .update import update_database


def get_method(*args, **kwargs):
    return Method.get(*args, **kwargs)

def search_methods(*args, **kwargs):
    return Method.search(*args, **kwargs)

query = session.query(Method)
