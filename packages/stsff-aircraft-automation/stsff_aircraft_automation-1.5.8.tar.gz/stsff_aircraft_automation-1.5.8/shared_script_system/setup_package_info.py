#!/usr/bin/env python
# ----------------------------------------------------------------------------------#
# //////////////////////////////////////////////////////////////////////////////////#
# ----------------------------------------------------------------------------------#

import os
import sys
import argparse
import distutils.file_util
from stsff_automation.utils import Utils
from helpers.loader import Loader
from helpers.my_utils import MyUtils

__author__ = 'StepToSky'


class SetupPackageInfo:
    originWorkDir = os.getcwd()
    workDir = os.getcwd()
    productFile = ''
    mArgParser = argparse.ArgumentParser(description=__file__)
    mArgs = ''

    def __init__(self, inOriginWorkDir='', inWorkingDir='', inProductFile=''):
        if inOriginWorkDir and inWorkingDir:
            self.originWorkDir = inOriginWorkDir
            self.workDir = inWorkingDir
        if inProductFile:
            self.productFile = inProductFile

    def preparePath(self, path):
        path = os.path.normpath(path)
        if not os.path.isabs(path):
            path = os.path.join(self.workDir, path)
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        return path

    def createGitRevisionFile(self, fileName):
        gitOrigRevFile = os.path.normpath(fileName)
        gitRevFile = os.path.normpath(fileName)
        if not os.path.isabs(gitOrigRevFile):
            gitOrigRevFile = os.path.join(self.originWorkDir, gitOrigRevFile)
        if not os.path.isabs(gitRevFile):
            gitRevFile = os.path.join(self.workDir, gitRevFile)
        gitRevCmd = 'git rev-parse --short HEAD > "' + gitOrigRevFile + '"'
        print('Getting git revision...')
        print('Trying to run command: ' + gitRevCmd)
        if not os.path.exists(os.path.dirname(gitOrigRevFile)):
            os.makedirs(os.path.dirname(gitOrigRevFile))
        os.chdir(self.originWorkDir)
        if os.system(MyUtils.fixCommandLine(gitRevCmd)):
            raise Exception('[ERROR] Git revision getting has failed.')
        if self.originWorkDir != self.workDir:
            if not os.path.exists(os.path.dirname(gitRevFile)):
                os.makedirs(os.path.dirname(gitRevFile))
            distutils.file_util.copy_file(gitOrigRevFile, gitRevFile)
        print('[INFO] Git revision file is created at: %s.' % gitRevFile)

    def createVersionFile(self, fileName, versionString):
        os.chdir(self.workDir)
        versionFile = self.preparePath(fileName)
        with open(versionFile, 'w') as fileName:
            fileName.write(Utils.string_to_version(versionString))
        print('[INFO] Version file is created at: %s' % versionFile)

    def createDebugFile(self, fileName):
        os.chdir(self.workDir)
        debugFile = self.preparePath(fileName)
        with open(debugFile, 'w') as fileName:
            fileName.write("If this file exists then the product will be running in debug mode.")
        print('[INFO] Debug file is created at: %s' % debugFile)

    def createPropFileForCi(self, fileName, packageDefinition):
        fileName = self.preparePath(fileName)
        with open(fileName, 'w') as fileHandle:
            primitiveTypes = (int, float, bool, str)
            for key in [i for i in dir(packageDefinition) if not callable(i) and not i.startswith('__')]:
                value = getattr(packageDefinition, key)
                if type(value) in primitiveTypes:
                    fileHandle.write("STSFF_PACKAGE_" + key.upper() + "='" + str(value).replace('\'', '\\\'') + "'\n")
        print('[INFO] Package definitions for Ci file is created at: %s' % fileName)

    def main(self):
        print('[START] %s...' % __file__)
        if not self.productFile:
            self.mArgParser.add_argument('--product_file',
                                         help='A file that describes the product.')
            self.mArgs = self.mArgParser.parse_args(sys.argv[1:])
            if self.mArgs.product_file:
                self.productFile = self.mArgs.product_file
            else:
                raise Exception('[ERROR] The product file is not set. (e.g. --product_file=automation/B757EX.py)')

        # checking work dir
        if not os.path.exists(self.productFile):
            raise Exception('[ERROR] Cannot find the product definition file: %s ' % self.productFile)

        print('Found the product definition file: %s' % self.productFile)

        # load aircraft definition class
        packageDefinition = Loader.load_product_definition_file(self.productFile, self.workDir)

        if packageDefinition.gitRevisionFile:
            self.createGitRevisionFile(packageDefinition.gitRevisionFile)
        if packageDefinition.versionFile:
            self.createVersionFile(packageDefinition.versionFile, packageDefinition.version)
        self.createDebugFile("debug.txt")
        self.createPropFileForCi("automation/tmp/packageDefinition", packageDefinition)

        print('[DONE] %s' % __file__)

# ----------------------------------------------------------------------------------#
# //////////////////////////////////////////////////////////////////////////////////#
# ----------------------------------------------------------------------------------#


# # --------------------------------------------------------#
# # launch
if __name__ == '__main__':
    obj = SetupPackageInfo()
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
