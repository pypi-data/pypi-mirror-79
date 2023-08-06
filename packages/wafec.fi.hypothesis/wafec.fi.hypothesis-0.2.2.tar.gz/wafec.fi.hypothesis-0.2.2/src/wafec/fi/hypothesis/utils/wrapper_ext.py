from abc import ABC
import copy

import wrapt


primitive = (
    int,
    str,
    float,
    enumerate,
    dict,
    list
)


def is_primitive(obj):
    return type(obj) in primitive


class CustomWrapperExt(wrapt.ObjectProxy, ABC):
    def __init__(self, target, obj_path=''):
        super(CustomWrapperExt, self).__init__(target)
        self._self_obj_path = obj_path

    def __getattr__(self, item):
        return call_get_item(super(CustomWrapperExt, self).__getattr__(item),
                             item,
                             self._self_obj_path)

    def __deepcopy__(self, memodict={}):
        return wrap(copy.deepcopy(self.__wrapped__, memodict),
                    self._self_obj_path)

    def __copy__(self):
        return wrap(copy.copy(self.__wrapped__),
                    self._self_obj_path)


def wrap(target, obj_path=''):
    if target is None:
        return None
    if not is_primitive(target):
        if obj_path == '':
            obj_path = target.__class__.__name__
        return CustomWrapperExt(target, obj_path)
    elif type(target) == dict:
        return wrap_dict(target, obj_path)
    elif type(target) == list:
        return wrap_list(target, obj_path)
    return target


def wrap_dict(target, obj_path=''):
    if target is None:
        return None
    if type(target) == dict:
        for key, value in target.items():
            target[key] = wrap(value, obj_path + '{' + key + '}')
    return target


def wrap_list(target, obj_path):
    if target is None:
        return None
    if type(target) == list:
        for i, value in zip(range(len(target)), target):
            target[i] = wrap(value, '{}[{}]'.format(obj_path, i))
    return target


def call_get_item(obj, item, obj_path, sep='.', sep_suffix=''):
    if obj is None:
        return None
    if callable(obj):
        return obj
    call_get_item_send(obj, item, obj_path, sep, sep_suffix)
    return wrap(obj,
                '{}.{}'.format(obj_path, item))


def call_get_item_send(obj, item, obj_path, sep='.', sep_suffix=''):
    item_str = '{}{}{}{}'.format(obj_path, sep, item, sep_suffix)
    call_get_item_send_text(item_str)
    if obj is None or callable(obj) or type(obj) == CustomWrapperExt or not is_primitive(obj):
        return
    if type(obj) == dict:
        for key, value in obj.items():
            call_get_item_send(value, key, item_str, '{', '}')
    elif type(obj) == list:
        for i, value in zip(range(len(obj)), obj):
            call_get_item_send(value, i, item_str, '[', ']')


def call_get_item_send_text(item_str):
    pass


def wrap_back(wrapped):
    if wrapped is None:
        return None
    if type(wrapped) == CustomWrapperExt:
        return wrapped.__wrapped__
    return wrapped
