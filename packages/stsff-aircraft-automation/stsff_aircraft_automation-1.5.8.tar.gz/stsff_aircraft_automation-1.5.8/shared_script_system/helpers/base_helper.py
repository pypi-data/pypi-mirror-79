#!/usr/bin/env python
# ----------------------------------------------------------------------------------#
# //////////////////////////////////////////////////////////////////////////////////#
# ----------------------------------------------------------------------------------#

import os
import sys
import argparse
import atexit
import shutil

__author__ = 'StepToSky'


class BaseHelper(object):
    # --------------------------------------------------------#
    # Members

    mBaseScriptsPath = 'automation/scripts'
    mEnvPrefix = 'STSFF_'

    mOrigWorkingDir = os.getcwd()  # constant
    mWorkingDir = os.getcwd()

    mProductFile = ''

    # example:
    # e:\StepToSky\FlightFactor\Workspace-Boeing757\757767Production
    mProdDir = ''
    # mProdDir+mPackageName;
    # example: e:\StepToSky\FlightFactor\Workspace-Boeing757\757767Production\Boeing757-200
    mTargetDir = ''
    # autocreated as mProdDir+"tmp"+mPackageName;
    # example: e:\StepToSky\FlightFactor\Workspace-Boeing757\757767Production\tmp\Boeing757-200
    mTmpDir = ''

    # some flags
    mIsSilentMode = False
    mWillClearTmpDirOnExit = True

    # arg parsing
    mArgParser = argparse.ArgumentParser(description=__file__)
    mArgs = ''

    # --------------------------------------------------------#
    # Methods

    def de_init(self):
        if self.mWillClearTmpDirOnExit:
            print('[INFO] Removing the tmp folder on exit: %s' % self.mTmpDir)
            if os.path.exists(self.mTmpDir):
                shutil.rmtree(self.mTmpDir)

    def __init__(self):
        atexit.register(BaseHelper.de_init, self)
        print("[INFO] The current working dir is: %s" % self.mOrigWorkingDir)
        pass

    def setupPathsAndDirs(self, inPackageName):
        self.setupPaths(inPackageName)
        self.checkAndCreateDirs()

    def setupInputParams(self):
        self.setupCliArgs()
        self.parseCliArgs()
        self.setupParamsFromEnv()

    # --------------------------------------------------------#
    # setup params

    def setupCliArgs(self):
        print("Setting up command line input in BaseHelper...")

        self.mArgParser.add_argument('--product_file', help='A file that describes the product to generate.')
        self.mArgParser.add_argument('--production_dir',
                                     help='The production dir for packages producing. '
                                          'The PROD_DIR env variable also can be used.')

        self.mArgParser.add_argument('--silent_mode', action='store_true',
                                     help='enables silent mode, no questions will be asked.')
        self.mArgParser.add_argument('--dont_clear_tmp', action='store_true',
                                     help='if set, the tmp folder will be cleared only on the next launch.')

        print("Setting up command line input in BaseHelper is done.")

    def parseCliArgs(self):
        print("Parsing command line input in BaseHelper...")
        # parse
        self.mArgs = self.mArgParser.parse_args(sys.argv[1:])

        if self.mArgs.product_file:
            self.mProductFile = self.mArgs.product_file
        else:
            raise Exception('[ERROR] The product file is not set. (e.g. --product_file=automation/B757EX.py)')

        if self.mArgs.production_dir:
            self.mProdDir = self.mArgs.production_dir

        if self.mArgs.silent_mode:
            self.mIsSilentMode = True
        if self.mArgs.dont_clear_tmp:
            self.mWillClearTmpDirOnExit = False

        print("Parsing the command line input in BaseHelper is done.")

    def setupParamsFromEnv(self):
        print('Setting up params from env, if it is needed ...')

        if not self.mProdDir:
            self.mProdDir = os.environ.get(self.mEnvPrefix + 'PROD_DIR')
            if not self.mProdDir:
                raise Exception('[ERROR] The production dir is not set.')

        print('Setting up params from env is done.')

    # --------------------------------------------------------#
    # Paths and Dirs

    def setupPaths(self, inPackageName):
        print('Setting up paths...')

        if not self.mProdDir:
            self.mProdDir = os.environ.get(self.mEnvPrefix + 'PROD_DIR')
            if self.mProdDir is None:
                raise Exception('[ERROR] The production dir is not specified!')
        if os.path.isabs(self.mProdDir):
            self.mProdDir = os.path.normpath(self.mProdDir)
        else:
            self.mProdDir = os.path.join(self.mWorkingDir, os.path.normpath(self.mProdDir))

        self.mTargetDir = os.path.join(self.mProdDir, inPackageName)

        if not self.mTmpDir:
            self.mTmpDir = os.path.join(self.mProdDir, 'tmp', inPackageName)
        else:
            if os.path.isabs(self.mTmpDir):
                self.mTmpDir = os.path.normpath(self.mTmpDir)
            else:
                self.mTmpDir = os.path.join(self.mProdDir, os.path.normpath(self.mTmpDir))

        print("{:<50}{}".format('The working dir is: ', self.mWorkingDir))
        print("{:<50}{}".format('The prod dir is: ', self.mProdDir))
        print("{:<50}{}".format('The target dir is: ', self.mTargetDir))
        print("{:<50}{}".format('The tmp dir is: ', self.mTmpDir))
        print('Paths are set.')

    @staticmethod
    def checkAndCreateDir(inDir):
        if not os.path.exists(inDir):
            os.makedirs(inDir)
            if not os.path.exists(inDir):
                raise Exception('[ERROR] The dir doesn\'t exist and cannot be created: ' + inDir)

    def checkAndCreateDirs(self):
        self.checkAndCreateDir(self.mProdDir)
        self.checkAndCreateDir(self.mTargetDir)
        self.checkAndCreateDir(self.mTmpDir)

    # --------------------------------------------------------#
    # Actions

    # --------------------------------------------------------#
    # Utils

    def addParamToResultFile(self, paramName, paramValue, scriptName):
        resultFileName = self.createResultFileName(scriptName)
        os.chdir(self.mOrigWorkingDir)
        fileName = open(resultFileName, 'a')
        fileName.write(paramName + '=\'' + paramValue + '\'\n')
        fileName.close()

    def resetResultFile(self, scriptName):
        resultFileName = self.createResultFileName(scriptName)
        os.chdir(self.mOrigWorkingDir)
        if os.path.exists(resultFileName):
            os.remove(resultFileName)

    @staticmethod
    def createResultFileName(inScriptName):
        return "automation/tmp/" + os.path.splitext(os.path.basename(inScriptName))[0] + "_results.txt"


# --------------------------------------------------------#
# main method


def main():
    exit()


# # --------------------------------------------------------#
# # launch
if __name__ == '__main__':
    main()
