#!/usr/bin/env python
# ----------------------------------------------------------------------------------#
# //////////////////////////////////////////////////////////////////////////////////#
# ----------------------------------------------------------------------------------#

import os
import sys
import argparse

from helpers.product_definition_file import *
from helpers.my_utils import MyUtils

__author__ = 'StepToSky'


class GetRequirements:
    originWorkDir = os.getcwd()
    workDir = os.getcwd()
    productFile = ''
    targetPath = '.'
    conanContext = ''
    mArgParser = argparse.ArgumentParser(description=__file__)
    mArgs = ''

    def __init__(self, inWorkingDir='', inProductFile='', inContext=''):
        if inWorkingDir:
            self.originWorkDir = inWorkingDir
            self.workDir = inWorkingDir
        if inProductFile:
            self.productFile = inProductFile
        if inContext:
            self.conanContext = inContext

    def conanInstall(self):
        print('[START] Conan install...')
        # conan install --update --no-imports -if automation/tmp automation\B757EX.py
        conanInstallCmd = 'conan install'
        conanInstallCmd += ' --update --no-imports'
        conanInstallCmd += ' --options context=%s' % self.conanContext
        conanInstallCmd += ' -if automation/tmp'
        conanInstallCmd += ' "%s"' % self.productFile
        print('Trying to run command: %s' % conanInstallCmd)
        os.chdir(self.workDir)
        if os.system(MyUtils.fixCommandLine(conanInstallCmd)):
            raise Exception('[ERROR] Conan install has failed.')
        print('[DONE] Conan install is done.')

    def conanImports(self, withCleanup=False):
        # cleanup
        if withCleanup:
            print('[START] Conan imports cleanup...')
            importManifestFile = os.path.join(self.workDir, self.targetPath, "conan_imports_manifest.txt")
            if os.path.exists(importManifestFile) or os.path.isfile(importManifestFile):
                conanImportCmd = 'conan imports'
                conanImportCmd += ' --undo'
                conanImportCmd += ' "%s"' % self.targetPath
                print('Trying to run command: %s' % conanImportCmd)
                os.chdir(self.workDir)
                if os.system(MyUtils.fixCommandLine(conanImportCmd)):
                    raise Exception('[ERROR] Conan imports cleanup has failed.')
            else:
                print('Conan import manifest file is not exist, the step is skipped. File: %s' % importManifestFile)
            print('[DONE] Conan imports cleanup is done.')
        # import
        print('[START] Conan imports...')
        # conan imports -imf . -if automation/tmp automation\B757EX.py
        conanImportCmd = 'conan imports'
        conanImportCmd += ' -imf "%s"' % self.targetPath
        conanImportCmd += ' -if automation/tmp'
        conanImportCmd += ' "%s"' % self.productFile
        print('Trying to run command: %s' % conanImportCmd)
        os.chdir(self.workDir)
        if os.system(MyUtils.fixCommandLine(conanImportCmd)):
            raise Exception('[ERROR] Conan imports has failed.')
        print('[DONE] Conan imports is done.')

    def main(self):
        print('[START] %s...' % __file__)
        if not self.productFile and not self.conanContext:
            self.mArgParser.add_argument('--product_file',
                                         help='A file that describes the product.')
            self.mArgParser.add_argument('--context',
                                         default=Context.developing,
                                         help='Context for installing requirements [developing, packaging], '
                                              'default is developing.')
            self.mArgParser.add_argument('--target_path',
                                         default='.',
                                         help='The path where the requirements will be placed, by default is "."')
            self.mArgs = self.mArgParser.parse_args(sys.argv[1:])
            if self.mArgs.product_file:
                self.productFile = self.mArgs.product_file
            else:
                raise Exception('[ERROR] The product file is not set. (e.g. --product_file=automation/B757EX.py)')
            if self.mArgs.context:
                self.conanContext = self.mArgs.context
            if self.mArgs.target_path:
                self.targetPath = self.mArgs.target_path

        # checking work dir
        if not os.path.exists(self.productFile):
            raise Exception('[ERROR] Cannot find the product definition file: %s ' % self.productFile)

        print('Found the product definition file: %s' % self.productFile)

        self.conanInstall()
        self.conanImports(True)

        print('[DONE] %s' % __file__)

# ----------------------------------------------------------------------------------#
# //////////////////////////////////////////////////////////////////////////////////#
# ----------------------------------------------------------------------------------#


# # --------------------------------------------------------#
# # launch
if __name__ == '__main__':
    obj = GetRequirements()
    try:
        obj.main()
    except Exception as ex:
        # non normal end
        os.chdir(obj.originWorkDir)
        print(ex)
        print('[!!!FAILED!!!] %s' % __file__)
        exit('[!!!FAILED!!!] %s' % __file__)
    # normal end
    os.chdir(obj.originWorkDir)
    exit()
