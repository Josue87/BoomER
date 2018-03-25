import sys
from os import path, sep
from importlib import import_module


def loadModule(module, directory="modules"):
    try:
        new_module = module.split("/")
        path_aux = path.join(directory, ".".join(new_module))
        if directory != "support/payloads/":
            path_aux = path_aux.replace(sep,".")
            moduleAux = import_module(path_aux)
            return moduleAux.BoomerModule()
        else:
            path_aux = path_aux.replace("/",".")
            moduleAux = import_module(path_aux)
            return moduleAux.Shellcode()
    except Exception as e:
        print(e)
        return None