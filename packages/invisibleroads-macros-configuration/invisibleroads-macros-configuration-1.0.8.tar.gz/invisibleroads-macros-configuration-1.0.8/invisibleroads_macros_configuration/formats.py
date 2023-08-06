import json
from importlib import import_module


def load_attributes(attribute_spec_text):
    return [load_attribute(_) for _ in attribute_spec_text.split()]


def load_attribute(attribute_spec):
    module_spec, attribute_name = attribute_spec.rsplit('.', maxsplit=1)
    module = import_module(module_spec)
    return getattr(module, attribute_name)


def load_json(path):
    return json.load(open(path, 'rt'))
