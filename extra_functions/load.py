import sys
from os import path, sep
from importlib import import_module


def loadModule(module):
    try:
        new_module = module.split("/")
        path_aux = path.join( "modules", sep.join(new_module))
        path_aux = path_aux.replace(sep,".")
        moduleAux = import_module(path_aux)
        return moduleAux.BoomerModule()
    except Exception as e:
        print(e)
        return None