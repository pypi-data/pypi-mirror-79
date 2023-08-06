from abc import abstractmethod, ABCMeta
from collections import deque
from typing import Type, List

from pydantic import validate_model, BaseModel, ValidationError

from pypads.app.misc.inheritance import SuperStop
from pypads.model.models import RunObjectModel
from pypads.utils.util import has_direct_attr


class ModelInterface(SuperStop):

    @classmethod
    @abstractmethod
    def get_model_cls(cls) -> Type[BaseModel]:
        raise NotImplementedError("A model cls has to be defined for a class linked to a model.")

    @abstractmethod
    def model(self) -> Type[BaseModel]:
        raise NotImplementedError("A function how to access the model of the class has to be defined.")

    @abstractmethod
    def schema(self):
        raise NotImplementedError("A function how to access the schema of the class has to be defined.")

    @abstractmethod
    def json(self):
        raise NotImplementedError("A function how to convert a class to its json representation has to be defined.")

    @abstractmethod
    def validate(self):
        raise NotImplementedError("A function how to validate the schema for the class has to be defined.")

    def get_model_fields(self):
        """
        Return the field names of a model.
        :return:
        """
        return self.get_model_cls().__fields__


class ModelObject(ModelInterface, metaclass=ABCMeta):
    """
    An object building the model from itself on the fly.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fields = set(self.get_model_fields().keys())

        # Add given fields to metadata object if not already existing
        for key, val in kwargs.items():
            if key in fields and not has_direct_attr(self, key):
                setattr(self, key, val)
                fields.remove(key)

        # Add defaults which are not given
        for key in fields:
            if not has_direct_attr(self, key) and self.get_model_fields():
                setattr(self, key, self.get_model_fields()[key].get_default())
        if issubclass(self.get_model_cls(), RunObjectModel) and (
                not hasattr(self, "uri") or getattr(self, "uri") is None):
            setattr(self, "uri", "{}#{}".format(getattr(self, 'is_a'), getattr(self, 'uid')))

    def model(self):
        return self.get_model_cls().from_orm(self)

    def validate(self):
        validate_model(self.get_model_cls(), self.model().__dict__)

    @classmethod
    def schema(cls):
        schema = cls.get_model_cls().schema()

        # Overwrite the model comment with the comment on the class if one exists
        if cls.__doc__ is not None:
            schema["description"] = cls.__doc__
        return schema

    def json(self, *args, **kwargs):
        return self.model().json(*args, **kwargs)


class ModelHolder(ModelInterface, metaclass=ABCMeta):
    """
    Used for objects storing their information directly into a validated base model
    """

    def __init__(self, *args, model: RunObjectModel = None, **kwargs):
        super().__init__(*args, **kwargs)
        self._model = self.get_model_cls()(**kwargs) if model is None else model

    def __getattr__(self, name):
        if name not in ["_model", "_model_cls"] and name in self.get_model_fields().keys():
            return getattr(self._model, name)
        else:
            return object.__getattribute__(self, name)

    def __setattr__(self, name, value):
        if name not in ["_model", "_model_cls"] and name in self.get_model_fields().keys():
            setattr(self._model, name, value)
        else:
            return object.__setattr__(self, name, value)

    def model(self):
        return self._model

    def validate(self):
        validate_model(self.get_model_cls(), self._model.__dict__)

    def schema(self):
        return self._model.schema()

    def json(self):
        return self._model.json()


class ModelErrorHandler:
    """ Class to handle errors on the validation of an validatable. """

    def __init__(self, absolute_path=None, validator=None, handle=None):
        self._absolute_path = absolute_path
        self._validator = validator
        self._handle = handle

    @property
    def validator(self):
        return self._validator

    @property
    def absolute_path(self):
        return self._absolute_path

    def handle(self, cls, e, options):
        if (not self._absolute_path or deque(self._absolute_path) == e.absolute_path) and (
                not self._validator or self.validator == e.validator):
            if self._handle is None:
                self._default_handle(e)
            else:
                return self._handle(cls, e, options)
        else:
            raise e

    def _default_handle(self, e):
        print("Empty validation handler triggered: " + str(self))
        raise e


class ModelFactory:

    @staticmethod
    def from_object(cls: BaseModel, obj, handlers: List[ModelErrorHandler] = None):
        return ModelFactory._try_creation(cls, cls.from_orm, handlers=handlers, __history=[], obj=obj)

    @staticmethod
    def make(cls, *args, handlers: List[ModelErrorHandler] = None, **options):
        return ModelFactory._try_creation(cls, cls, *args, handlers=handlers, __history=[], **options)

    @staticmethod
    def _try_creation(cls, fn, *args, handlers: List[ModelErrorHandler] = None, __history=None, **options):
        if handlers is None:
            handlers = []
        try:
            return fn(*args, **options)
        except ValidationError as e:
            # Raise error if we can't handle anything
            if handlers is None:
                raise e
            for handler in handlers:
                new_options = handler.handle(cls, e, options)
                # If the handler could fix the problem return the new value
                if new_options is not None and e not in __history and new_options not in __history:
                    __history.append(e)
                    __history.append(new_options)

                    # Try to create object again
                    return ModelFactory._try_creation(cls, handlers=handlers, __history=__history, **new_options)
            # Raise error if we fail
            raise e
