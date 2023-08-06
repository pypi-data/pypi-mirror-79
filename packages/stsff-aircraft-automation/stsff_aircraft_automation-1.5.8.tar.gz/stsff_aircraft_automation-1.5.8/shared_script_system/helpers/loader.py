#!/usr/bin/env python
# ----------------------------------------------------------------------------------#
# //////////////////////////////////////////////////////////////////////////////////#
# ----------------------------------------------------------------------------------#

import os
import inspect
import imp
from conans import ConanFile

from helpers.product_definition_file import ProductDefinitionFile

__author__ = 'StepToSky'


class Loader:
    def __init__(self):
        pass

    @staticmethod
    def load_product_definition_file(file_path, work_dir):
        # load aircraft definition class
        os.chdir(os.path.dirname(file_path))
        module_id = os.path.splitext(os.path.basename(file_path))[0]
        loadedModule = imp.load_source(module_id, os.path.basename(file_path))
        result = None
        for name, attr in loadedModule.__dict__.items():
            if (name.startswith("_") or not inspect.isclass(attr) or
                    attr.__dict__.get("__module__") != module_id):
                continue
            if issubclass(attr, ProductDefinitionFile) and attr != ProductDefinitionFile\
                    and not issubclass(attr, ConanFile):
                if result is None:
                    result = attr()
                else:
                    raise Exception("[ERROR] More than 1 ProductDefinitionFile subclass in the product file.")

        if result is None:
            print("[WARNING] No subclass of ProductDefinitionFile is found. "
                  "Will load ProductDefinitions class in legacy mode.")
            # set correct base class to legacy product definition class
            loadedModule.ProductDefinitions = type('ProductDefinitions',
                                                   (ProductDefinitionFile,),
                                                   dict(loadedModule.ProductDefinitions.__dict__))
            result = loadedModule.ProductDefinitions()

        if not result.version or not result.id or not result.name:
            raise Exception('[ERROR] The ProductDefinitionFile class should contain at least '
                            '"version", "id" and "name" attributes.')

        os.chdir(work_dir)
        return result
