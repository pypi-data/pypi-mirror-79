"""Proxy for biopipely-xxx"""
from modkit import modkit




@modkit.delegate
def get_module(module, name):
    print(name)
    return lambda: None
