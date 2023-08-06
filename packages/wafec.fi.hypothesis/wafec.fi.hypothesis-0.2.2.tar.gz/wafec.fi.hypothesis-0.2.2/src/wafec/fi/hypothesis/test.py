from wafec.fi.hypothesis.utils.wrapper_ext import wrap
import copy
import json


class C:
    def __init__(self):
        self.m = 'wallace'


class B:
    def __init__(self):
        self.c = {
            'name': 'car',
            'c': C()
        }


class Test:
    def __init__(self):
        self.a = 10
        self.b = B()


w = wrap(Test())
print(w.b.c['name'])
print(w.b.c['c'].m)
copy.deepcopy(w)