# (C) Copyright 2024 European Centre for Medium-Range Weather Forecasts.
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.


import logging
import os

try:
    import tomllib  # Only available since 3.11
except ImportError:
    import tomli as tomllib


LOG = logging.getLogger(__name__)


class DotDict(dict):
    """A dictionary that allows access to its keys as attributes"""

    def __getitem__(self, key):
        item = super().__getitem__(key)
        if isinstance(item, dict):
            return DotDict(item)
        return item

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(attr)

    def __setattr__(self, attr, value):
        self[attr] = value


CONFIG = None


def load_config():
    """Load the configuration from disk

    Returns
    -------
    DotDict
        The configuration
    """
    global CONFIG
    if CONFIG is not None:
        return CONFIG

    conf = os.path.expanduser("~/.anemoi.toml")

    if os.path.exists(conf):

        with open(conf, "rb") as f:
            CONFIG = tomllib.load(f)
    else:
        CONFIG = {}

    return DotDict(CONFIG)


def save_config():
    """Save the configuration to disk"""

    conf = os.path.expanduser("~/.anemoi.toml")
    with open(conf, "w") as f:
        tomllib.dump(CONFIG, f)
