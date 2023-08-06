from invisibleroads_macros_log import get_log
from invisibleroads_macros_security import make_random_string
from os.path import expandvars

from .constants import SECRET_LENGTH
from .formats import load_attributes


L = get_log(__name__)


class Settings(dict):

    def set(self, settings, prefix, key, default=None, parse=None):
        value = set_default(settings, prefix + key, default, parse)
        self[key] = value
        return value


def set_default(settings, key, default, parse=None):
    value = settings.get(key, default)
    if key not in settings:
        L.warning(f'using default {key} = {value}')
    elif value in ('', None):
        L.warning(f'missing {key}')
    elif parse:
        value = parse(value)
    settings[key] = value
    return value


def fill_environment_variables(settings):
    for k, v in settings.items():
        if not isinstance(v, str):
            continue
        settings[k] = expandvars(v)


def fill_secrets(settings, secret_length=SECRET_LENGTH):
    for k, v in settings.items():
        if v or not k.endswith('.secret'):
            continue
        settings[k] = make_random_string(secret_length)


def fill_extensions(settings):
    for k, v in settings.items():
        if not k.endswith('.extensions'):
            continue
        settings[k] = load_attributes(v)
