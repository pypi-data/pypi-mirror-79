from wafec.fi.hypothesis.utils.wrapper import WrapperClass, WrapperDict, WrapperList, make_wrapper_simple

import copy


class Test:
    def __init__(self):
        self.a = 109

    def hello(self):
        print('hello {}'.format(self.a))


class A:
    def __init__(self):
        self.x = 10
        self.y = 20
        self.b = B()
        self.l = [
            1, 2,
            {
                'test': 'name'
            }
        ]

    def hello(self):
        print('hello {}'.format(self.y))


class B:
    def __init__(self):
        self.z = 50


class MyMeta(type):
    def __new__(mcs, name, bases, dct):
        print(dct)
        return super(MyMeta, mcs).__new__(mcs, name, bases, dct)


class MySub(metaclass=MyMeta):
    def __init__(self, t):
        self.test = t


test = Test()
wrapped = WrapperClass(wrappee=test)
print(isinstance(wrapped, Test))
print(wrapped.a)
wrapped.hello()
d = {'test': 10}
wrapped_dict = WrapperDict(d)
print(wrapped_dict)
wrapped_dict['wallace'] = 'felipe'
print(isinstance(wrapped_dict, dict))
print(wrapped_dict.keys())
l = [1, 2]
wrapped_list = make_wrapper_simple(l)
print(wrapped_list)
print(wrapped_list[1])
wrapped_list.append(3)
print(wrapped_list)
print('-- complex')
a = A()
callback = lambda opt: print(opt)
wrapped_a = make_wrapper_simple(a, callback=callback, obj_path='a')
print(wrapped_a.b.z)
wrapped_a.x = 30
copy_l = copy.copy(wrapped_list)
print(copy_l)
print(wrapped_a.l)
print(wrapped_a.l[2])
print(wrapped_a.l[2]['test'])
wrapped_a.hello()

copy_a = copy.deepcopy(wrapped_a)
print(copy_a.l)
