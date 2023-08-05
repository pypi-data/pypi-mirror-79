from wafec.fi.hypothesis.utils import make_custom_wrapper_client

import copy


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