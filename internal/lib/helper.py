import importlib


def dynamic_import(module_name, symbol_name):
    module = importlib.import_module(module_name)
    return getattr(module, symbol_name)


def add_attribute(name, value):
    def decorator(func):
        setattr(func, name, value)
        return func

    return decorator
