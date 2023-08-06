from importlib import import_module
from invisibleroads_macros_log import get_log
from invisibleroads_macros_security import make_random_string
from os.path import expandvars

from .constants import SECRET_LENGTH


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

    def load_extensions(extension_specs):
        return [resolve_attribute(_) for _ in extension_specs]

    for k, v in settings.items():
        if not k.endswith('.extensions'):
            continue
        settings[k] = load_extensions(v.split())


def resolve_attribute(attribute_spec):
    module_spec, attribute_name = attribute_spec.rsplit('.', maxsplit=1)
    module = import_module(module_spec)
    return getattr(module, attribute_name)
