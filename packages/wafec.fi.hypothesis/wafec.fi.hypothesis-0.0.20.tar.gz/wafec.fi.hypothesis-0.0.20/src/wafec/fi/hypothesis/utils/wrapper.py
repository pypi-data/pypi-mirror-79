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
        if d is not None and 'keys' in d:
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
