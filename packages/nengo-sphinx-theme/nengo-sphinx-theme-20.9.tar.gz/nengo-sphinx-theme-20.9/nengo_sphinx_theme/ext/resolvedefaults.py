import inspect
import warnings
import time

from nengo.params import Default, IntParam, iter_params, StringParam
import numpy as np


def test_func(
    param0=np.random,
    param1=np.random.randint,
    param2=np.random.RandomState,
    param4=np.random.RandomState(),
):
    """Test that setting various different object types as args renders nicely."""


class TestClass:
    """For testing that defaults are properly rendered in docs."""

    int_param = IntParam("int_param", default=1)
    str_param = StringParam("str_param", default="hello")

    def __init__(self, int_param=Default, str_param=Default, module_param=np.random):
        """Init method"""

    def another_method(self, module_param=np.random):
        """A method"""


# `inspect.signature` fails on built-ins; test that `autodoc_defaults` handles this
test_builtin_func = time.time


class TestBuiltinClass(np.random.RandomState):
    pass


class DisplayDefault:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return self.value


def resolve_default(cls, param):
    if inspect.ismodule(param.default):
        return DisplayDefault(param.default.__name__)
    elif param.default is not Default:
        return param.default
    else:
        for cls_param in (getattr(cls, name) for name in iter_params(cls)):
            if cls_param.name == param.name:
                return DisplayDefault("Default<{!r}>".format(cls_param.default))
        warnings.warn(
            "Default value for argument {} of {} could not be "
            "resolved.".format(param.name, cls)
        )
        return param.default


def autodoc_defaults(app, what, name, obj, options, signature, return_annotation):
    if what not in ("function", "method", "class"):
        return None

    try:
        spec = inspect.signature(obj)
    except ValueError as e:
        if str(e).startswith("no signature found for builtin"):
            return None
        else:
            raise

    if not any(
        inspect.ismodule(p.default) or p.default is Default
        for p in spec.parameters.values()
    ):
        return None

    new_params = [
        p.replace(default=resolve_default(obj, p)) for p in spec.parameters.values()
    ]
    new_spec = spec.replace(
        parameters=new_params, return_annotation=inspect.Signature.empty
    )

    return str(new_spec), return_annotation


def setup(app):
    # note: setting priority<500 so that this will be prioritized ahead of
    # numpydoc's mangle_signature, otherwise it has no effect (as sphinx only applies
    # the first non-None output from the list of listeners)
    app.connect("autodoc-process-signature", autodoc_defaults, priority=499)
