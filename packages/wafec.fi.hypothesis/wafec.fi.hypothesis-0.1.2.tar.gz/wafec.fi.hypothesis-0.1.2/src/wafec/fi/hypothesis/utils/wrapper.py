from . import parameter_client_factory

import wrapt
import logging
import copy

LOG = logging.getLogger(__name__)


def make_wrapper(instance, service, context):
    if instance is not None:
        d = None
        if isinstance(instance, dict):
            d = instance
        elif hasattr(instance, '__dict__'):
            d = getattr(instance, '__dict__')
        if d is not None and ('keys' in d or hasattr(d, 'keys')):
            instance = Wrapper(instance, service, context)
            for k in d.keys():
                wrappee = make_wrapper(d[k], service, '{}.{}'.format(context, k))
                if isinstance(instance, dict):
                    d[k] = wrappee
                else:
                    setattr(instance, k, wrappee)
        elif isinstance(instance, list):
            for index, item in zip(range(len(instance)), instance):
                instance[index] = make_wrapper(item, service, '{}[{}]'.format(service, index))
    return instance


class Wrapper(wrapt.ObjectProxy):
    def __init__(self, wrapped, service, context):
        super(Wrapper, self).__init__(wrapped)
        self._self_service = service
        self._self_context = context
        self._self_parameter_client = parameter_client_factory()

    def __getattr__(self, item):
        try:
            self._self_parameter_client.create_or_update(item, self._self_service, self._self_context)
        except Exception:
            LOG.exception('Failed to send parameter info')
        return super(Wrapper, self).__getattr__(item)

    def __getitem__(self, item):
        try:
            self._self_parameter_client.create_or_update(item, self._self_service, self._self_context)
        except Exception:
            LOG.exception('Failed to send parameter info')
        return super(Wrapper, self).__getitem__(item)

    def __copy__(self):
        if self.__wrapped__ is None:
            return None
        return copy.copy(self.__wrapped__)

    def __deepcopy__(self, memodict={}):
        if self.__wrapped__ is None:
            return None
        return copy.deepcopy(self.__wrapped__, memodict)

    def __reduce__(self):
        if self.__wrapped__ is None:
            return None
        return self.__wrapped__.__reduce__()

    def __reduce_ex__(self, protocol):
        if self.__wrapped__ is None:
            return None
        return self.__wrapped__.__reduce_ex__(protocol)


class WrapperMeta(type):
    def __call__(cls, *args, **kwargs):
        if len(args) > 0:
            wrappee = args[0]
        elif 'wrappee' in kwargs:
            wrappee = kwargs['wrappee']
        else:
            raise ValueError('Wrappee not defined')
        new_cls = type(wrappee.__class__.__name__,
                       (cls, wrappee.__class__),
                       {})
        res = type.__call__(new_cls, *args, **kwargs)
        res.__wrappee__ = wrappee
        res.__callback__ = lambda _: None
        res.__obj_path__ = ''
        if 'callback' in kwargs:
            res.__callback__ = kwargs['callback']
        if 'obj_path' in kwargs:
            res.__obj_path__ = kwargs['obj_path']
        return res


class WrapperClass(metaclass=WrapperMeta):
    def __init__(self, **kwargs):
        pass

    def __getattr__(self, item):
        res = getattr(self.__wrappee__, item)
        self.__callback__({'event': 'get', 'item': item, 'obj_path': self.__obj_path__, 'type': type(res).__name__})
        return make_wrapper_simple(res,
                                   callback=self.__callback__,
                                   obj_path='{}.{}'.format(self.__obj_path__, item))

    def __deepcopy__(self, memodict={}):
        res = copy.deepcopy(self.__wrappee__, memodict)
        return make_wrapper_simple(res,
                                   callback=self.__callback__,
                                   obj_path=self.__obj_path__)

    def __copy__(self):
        res = copy.deepcopy(self.__wrappee__)
        return make_wrapper_simple(res,
                                   callback=self.__callback__,
                                   obj_path=self.__obj_path__)


class WrapperDict(dict, metaclass=WrapperMeta):
    def __init__(self, wrappee, **kwargs):
        super(WrapperDict, self).__init__()
        for k, v in wrappee.items():
            super(WrapperDict, self).__setitem__(k, v)

    def __getitem__(self, item):
        res = super(WrapperDict, self).__getitem__(item)
        self.__callback__({'event': 'get', 'item': item, 'obj_path': self.__obj_path__, 'type': type(res).__name__})
        return make_wrapper_simple(res,
                                   callback=self.__callback__,
                                   obj_path='{}[{}]'.format(self.__obj_path__, item))

    def __setitem__(self, key, value):
        self.__callback__({'event': 'set', 'item': key, 'value': value, 'obj_path': self.__obj_path__})
        super(WrapperDict, self).__setitem__(key, value)


class WrapperList(list, metaclass=WrapperMeta):
    def __init__(self, wrappee, **kwargs):
        super(WrapperList, self).__init__()
        for v in wrappee:
            super(WrapperList, self).append(v)

    def __getitem__(self, item):
        res = super(WrapperList, self).__getitem__(item)
        self.__callback__({'event': 'get', 'item': item, 'obj_path': self.__obj_path__, 'type': type(res).__name__})
        return make_wrapper_simple(res,
                                   callback=self.__callback__,
                                   obj_path='{}[{}]'.format(self.__obj_path__, item))

    def __setitem__(self, key, value):
        self.__callback__({'event': 'set', 'item': key, 'value': value, 'obj_path': self.__obj_path__})
        super(WrapperList, self).__setitem__(key, value)

    def append(self, value):
        self.__callback__({'event': 'set', 'item': len(self), 'value': value, 'obj_path': self.__obj_path__})
        super(WrapperList, self).append(value)


def make_wrapper_simple(instance, **kwargs):
    if callable(instance):
        return instance
    if isinstance(instance, dict):
        return WrapperDict(wrappee=instance, **kwargs)
    elif isinstance(instance, list):
        return WrapperList(wrappee=instance, **kwargs)
    else:
        try:
            return WrapperClass(wrappee=instance, **kwargs)
        except:
            return instance


def _make_wrapper_simple_client_callback(opt):
    if opt['event'] == 'get':
        parameter_client = parameter_client_factory()
        parameter_client.create_or_update(opt['item'], 'test', opt['obj_path'])


def make_wrapper_simple_client(instance, **kwargs):
    return make_wrapper_simple(instance, callback=_make_wrapper_simple_client_callback, **kwargs)
