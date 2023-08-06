from abc import ABCMeta
from functools import wraps
from typing import Type

from pydantic import BaseModel, HttpUrl

from pypads.app.injections.base_logger import LoggerCall, SimpleLogger
from pypads.app.misc.extensions import ExtendableMixin, Plugin
from pypads.injections.analysis.determinism import check_determinism
from pypads.model.models import LoggerModel
from pypads.utils.util import inheritors

validator_plugins = set()


class Validator(SimpleLogger, metaclass=ABCMeta):
    is_a: HttpUrl = "https://www.padre-lab.eu/onto/validator"

    def build_call_object(self, _pypads_env, **kwargs):
        return LoggerCall(logging_env=_pypads_env,
                          is_a="https://www.padre-lab.eu/onto/ValidatorLoggerCall", **kwargs)

    @classmethod
    def get_model_cls(cls) -> Type[BaseModel]:
        return LoggerModel

    def _base_path(self):
        return "Validators/{}/".format(self.__class__.__name__)


class IValidators(Plugin):

    def __init__(self):
        super().__init__(type=Validator)
        validator_plugins.add(self)

    def _get_meta(self):
        """ Method returning information about where the actuator was defined."""
        return self.__module__

    def _get_methods(self):
        return [method_name for method_name in dir(self) if callable(getattr(object, method_name))]


def validator(f):
    """
    Validator used to convert a function to a tracked actuator.
    :param f:
    :return:
    """

    @wraps(f)
    def wrapper(self, *args, **kwargs):
        # self is an instance of the class
        return Validator(fn=f)(self, *args, **kwargs)

    return wrapper


class PyPadsValidators(IValidators):
    def __init__(self):
        super().__init__()

    @property
    def pypads(self):
        from pypads.app.pypads import get_current_pads
        return get_current_pads()

    @validator
    def determinism(self):
        check_determinism()


class ValidatorPluginManager(ExtendableMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(plugin_list=validator_plugins)


pypads_validators = PyPadsValidators()


def validators():
    """
    Returns classes of
    :return:
    """
    return inheritors(Validator)
