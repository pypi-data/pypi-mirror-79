import shlex

import toml
from jaraco.context import suppress
from jaraco.functools import apply


def none_as_empty(ob):
    """
    >>> none_as_empty({})
    {}
    >>> none_as_empty(None)
    {}
    >>> none_as_empty({'a': 1})
    {'a': 1}
    """
    return ob or {}


@apply(none_as_empty)
@suppress(Exception)
def read_plugins(filename):
    with open(filename) as strm:
        defn = toml.load(strm)
    return defn["tool"]["jaraco"]["pytest"]["plugins"]


def pytest_configure(config):
    plugins = read_plugins('pyproject.toml')
    matches = filter(config.pluginmanager.has_plugin, plugins)
    for match in matches:
        config.args.extend(shlex.split(plugins[match].get('addopts', "")))
