import sys
from os import path, sep
from importlib import import_module


def loadModule(module, directory="modules"):
    try:
        new_module = module.split("/")
        path_aux = path.join(directory, sep.join(new_module))
        path_aux = path_aux.replace(sep,".")
        moduleAux = import_module(path_aux)
        if directory != "support/payloads":
            return moduleAux.BoomerModule()
        return moduleAux.Shellcode()
    except Exception as e:
        print(e)
        return None