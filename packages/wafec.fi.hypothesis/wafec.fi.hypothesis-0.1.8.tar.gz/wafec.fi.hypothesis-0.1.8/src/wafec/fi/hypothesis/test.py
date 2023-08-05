from wafec.fi.hypothesis.utils import make_custom_wrapper_client, Default
from wafec.fi.hypothesis.utils.wrapper import WrapperDict

import copy
import json


Default.endpoint = 'http://192.168.56.91:8080'

class A:
    def __init__(self):
        self.a = 10
        self.b = {
            'test': 'name',
            'car': 'vw'
        }


a = A()
cb = lambda opt: print(opt)
wrapped_a = make_custom_wrapper_client(a, callback=cb, obj_path='a')
print(wrapped_a.a)
print(wrapped_a.b['car'])
print(json.dumps(wrapped_a.b))