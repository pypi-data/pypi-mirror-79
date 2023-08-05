"""
This extension replaces the default Sphinx HTML source links with links to some
other site (e.g., GitHub).

This extension can be enabled by adding ``"nengo_sphinx_theme.ext.sourcelinks"``
to the ``extensions`` list in ``conf.py``.

This extension adds two new configuration options, ``sourcelinks_module`` (the
importable name of the package we're setting up) and ``sourcelinks_url`` (the base
URL for the site we want the links to refer to).
"""

import importlib
import inspect
import os
import sys


def set_resolver(_, config):  # noqa: C901
    def linkcode_resolve(domain, info):
        """Determine the URL corresponding to Python object.

        Code borrowed from:
            https://github.com/numpy/numpy/blob/master/doc/source/conf.py
        """
        if domain != "py":
            return None

        modname = info["module"]
        fullname = info["fullname"]

        submod = sys.modules.get(modname)
        if submod is None:
            return None

        obj = submod
        for part in fullname.split("."):
            try:
                obj = getattr(obj, part)
            except AttributeError:
                return None

        try:
            fn = inspect.getsourcefile(obj)
        except TypeError:
            fn = None
        if not fn:
            return None

        try:
            source, lineno = inspect.getsourcelines(obj)
            linespec = "#L%d-L%d" % (lineno, lineno + len(source) - 1)
        except IOError:
            linespec = ""

        fn = os.path.relpath(
            fn,
            start=os.path.dirname(
                importlib.import_module(config["sourcelinks_module"]).__file__
            ),
        )

        return "%s/blob/%s/%s/%s%s" % (
            config["sourcelinks_url"],
            "master" if "dev" in config["release"] else ("v" + config["release"]),
            config["sourcelinks_module"],
            fn,
            linespec,
        )

    config["linkcode_resolve"] = linkcode_resolve


def setup(app):
    app.setup_extension("sphinx.ext.linkcode")

    app.add_config_value("sourcelinks_module", None, "")
    app.add_config_value("sourcelinks_url", None, "")

    app.connect("config-inited", set_resolver)
