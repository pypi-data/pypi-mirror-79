#!/usr/bin/env python
# ----------------------------------------------------------------------------------#
# //////////////////////////////////////////////////////////////////////////////////#
# ----------------------------------------------------------------------------------#

import os
import shutil
import distutils.dir_util
import distutils.file_util

from helpers.base_helper import BaseHelper
from stsff_automation.vcs_info import VcsInfo
from helpers.product_definition_file import *
from helpers.my_utils import MyUtils

__author__ = 'StepToSky'

# --------------------------------------------------------#
# class


class PackageHelper(BaseHelper):
    # --------------------------------------------------------#
    # Members
    mConanContext = Context()

    # mTmpDir/"sasl_source";
    # example: e:\StepToSky\FlightFactor\Workspace-Boeing757\757767Production\tmp\Boeing757-200/sasl_source
    mTmpSourceDir = ''
    # mTmpDir/"sasl_result";
    # example: e:\StepToSky\FlightFactor\Workspace-Boeing757\757767Production\tmp\Boeing757-200/sasl_result
    mTmpResultDir = ''
    # mTmpDir/"clean_git_index";
    # example: e:\StepToSky\FlightFactor\Workspace-Boeing757\757767Production\tmp\Boeing757-200/clean_git_index
    mTmpGitIndexDir = ''

    mIsGitCheckoutDisabled = False

    # access data
    mSaslProtectLogin = ''
    mSaslProtectPass = ''

    # --------------------------------------------------------#
    # Methods

    def setupCliArgs(self):
        super(PackageHelper, self).setupCliArgs()
        print("Setting up command line input...")
        self.mArgParser.add_argument('--without_git_checkout', action='store_true',
                                     help='By default the script will make an additional clean checkout for work, '
                                          'this will disable it.')
        self.mArgParser.add_argument('--context',
                                     help='Context for installing requirements [developing, packaging], '
                                          'default is developing.')
        print("Setting up the command line input is done.")

    def parseCliArgs(self):
        super(PackageHelper, self).parseCliArgs()
        print("Parsing command line input...")
        if self.mArgs.without_git_checkout:
            self.mIsGitCheckoutDisabled = True
        if self.mArgs.context:
            self.mConanContext = Context(self.mArgs.context)

        print("Parsing command line input is done.")

    def setupParamsFromEnv(self):
        super(PackageHelper, self).setupParamsFromEnv()
        print('Setting up params from env, if it is needed ...')
        if not self.mSaslProtectLogin:
            self.mSaslProtectLogin = os.environ.get(self.mEnvPrefix + 'SASL_PROT_LOGIN')
            if not self.mSaslProtectLogin:
                raise Exception('[ERROR] The login for sasl protect system is not set.')
        if not self.mSaslProtectPass:
            self.mSaslProtectPass = os.environ.get(self.mEnvPrefix + 'SASL_PROT_PASS')
            if not self.mSaslProtectPass:
                raise Exception('[ERROR] The password for sasl protect system is not set.')
        print('Setting up params from env is done.')

    # --------------------------------------------------------#
    # Paths and Dirs

    def setupPaths(self, inPackageName):
        super(PackageHelper, self).setupPaths(inPackageName)
        self.mTmpSourceDir = os.path.join(self.mTmpDir, 'sasl_source')
        self.mTmpResultDir = os.path.join(self.mTmpDir, 'sasl_result')
        self.mTmpGitIndexDir = os.path.join(self.mTmpDir, 'clean_git_index')

    def checkAndCreateDirs(self):
        super(PackageHelper, self).checkAndCreateDirs()

        # remove old
        if os.path.exists(self.mTmpSourceDir):
            shutil.rmtree(self.mTmpSourceDir)
        if os.path.exists(self.mTmpResultDir):
            shutil.rmtree(self.mTmpResultDir)
        # create new
        self.checkAndCreateDir(self.mTmpSourceDir)
        self.checkAndCreateDir(self.mTmpResultDir)

        # for clean git index, it's not needed to be created, git creates it by itself
        if os.path.exists(self.mTmpGitIndexDir):
            shutil.rmtree(self.mTmpGitIndexDir)

    # --------------------------------------------------------#
    # Git operations

    def getCorrectCleanIndexCwd(self, inDest):
        from subprocess import check_output
        out = check_output(["git", "rev-parse", "--show-toplevel"]).decode("utf-8").strip()
        relPath = os.path.relpath(os.path.normpath(self.mOrigWorkingDir), os.path.normpath(out))
        resultPath = os.path.normpath(os.path.join(os.path.normpath(inDest), relPath))
        print("[INFO] Clean index working dir: <%s>" % resultPath)
        return resultPath

    def makeCleanGitIndex(self, inDestDir):
        # this slash at the end of prefix line is very important! It won't work without it!
        # So, don't remove it!
        gitCheckoutIndexCmd = 'git checkout-index -a -f --prefix="' + inDestDir + '/"'
        print('Checking out git index...')
        print('Trying to run command: ' + gitCheckoutIndexCmd)
        os.chdir(self.mOrigWorkingDir)
        if os.system(MyUtils.fixCommandLine(gitCheckoutIndexCmd)):
            raise Exception('[ERROR] Git index checking out has failed.')
        self.mWorkingDir = self.getCorrectCleanIndexCwd(inDestDir)
        # generate vcs_info file and copy it into clean checkout dir
        vcsInfo = VcsInfo(vcs_info_file='automation/tmp/vcs_info')
        destVcsInfoFile = os.path.join(self.mWorkingDir, vcsInfo.vcs_info_file)
        if self.mOrigWorkingDir != self.mWorkingDir:
            if not os.path.exists(os.path.dirname(destVcsInfoFile)):
                os.makedirs(os.path.dirname(destVcsInfoFile))
            distutils.file_util.copy_file(vcsInfo.vcs_info_file, destVcsInfoFile)
        print('Git index checking out is done.')

    # --------------------------------------------------------#
    # File operations

    def createPackageWithProdList(self, inProdList, inEolConf):
        prodList = os.path.normpath(inProdList)
        if not os.path.isabs(prodList):
            prodList = os.path.join(self.mWorkingDir, prodList)
        print('Copying files into package using prod list: ' + prodList)
        eolConf = os.path.normpath(inEolConf)
        if not os.path.isabs(eolConf):
            eolConf = os.path.join(self.mWorkingDir, eolConf)

        scriptsDir = os.path.dirname(__file__)
        jarPath = os.path.normpath(os.path.join(scriptsDir, "bin/produce.jar"))
        produceCmd = 'java -jar "%s"' % jarPath
        produceCmd += ' "' + self.mWorkingDir + '"'
        produceCmd += ' "' + self.mTargetDir + '"'
        produceCmd += ' "' + prodList + '"'
        produceCmd += ' "' + eolConf + '"'
        produceCmd += ' 1'
        print('Trying to run command: ' + produceCmd)
        os.chdir(self.mWorkingDir)
        if os.system(MyUtils.fixCommandLine(produceCmd)):
            raise Exception('[ERROR] Files copying has failed.')

        print('Files copying is done.')

    def removeNonReleaseFiles(self, inRelExcludeList):
        excludeList = os.path.normpath(inRelExcludeList)
        if not os.path.isabs(excludeList):
            excludeList = os.path.join(self.mWorkingDir, excludeList)
        print('Removing files that should be excluded in release by the exclude list: ' + excludeList)
        with open(excludeList, 'r') as fileHandle:
            for line in fileHandle:
                line = line.strip()
                line = os.path.normpath(line)
                line = os.path.join(self.mTargetDir, line)
                if os.path.exists(line):
                    if os.path.isdir(line):
                        shutil.rmtree(line)
                    else:
                        os.remove(line)
                else:
                    raise Exception('[ERROR] The given path is not exist: <%s>' % line)
        print('Removing files is done.')

    # --------------------------------------------------------#
    # Sasl special operations

    def prepareSaslFilesForProtecting(self, inSaslProtector):
        if inSaslProtector == SaslProtector.none:
            return
        if inSaslProtector == SaslProtector.sasl2:
            print('SASL2 Protecting Preparing')
            print('Copying files into temp folder...')
            distutils.dir_util.copy_tree(os.path.join(self.mWorkingDir, 'Custom Avionics'),
                                         os.path.join(self.mTmpSourceDir, 'Custom Avionics'))
            distutils.file_util.copy_file(os.path.join(self.mWorkingDir, 'avionics.lua'),
                                          self.mTmpSourceDir)
        elif inSaslProtector == SaslProtector.sasl3:
            print('SASL3 Protecting Preparing')
            print('Copying files into temp folder...')
            distutils.dir_util.copy_tree(os.path.join(self.mWorkingDir, 'modules'),
                                         os.path.join(self.mTmpSourceDir, 'modules'))
        else:
            raise Exception('[ERROR] Unknown SASL Protector given: %s.' % inSaslProtector)

    def protectAndCopySaslFiles(self, inProjId, inSaslProtector):
        if inSaslProtector == SaslProtector.none:
            return
        print('Getting the lua scripts protected...')

        scriptsDir = os.path.dirname(__file__)
        jarPath = os.path.normpath(os.path.join(scriptsDir, "bin/%s" % inSaslProtector))
        protectCmd = 'java -jar "%s"' % jarPath

        if inSaslProtector == SaslProtector.sasl2:
            print('SASL2 Protecting')
            protectCmd += ' -i ' + str(inProjId)
            protectCmd += ' -s "' + self.mTmpSourceDir + '"'
            protectCmd += ' -d "' + self.mTmpResultDir + '"'
        elif inSaslProtector == SaslProtector.sasl3:
            print('SASL3 Protecting')
            protectCmd += ' -i ' + str(inProjId)
            protectCmd += ' -s "' + self.mTmpSourceDir + '"'
            protectCmd += ' -d "' + self.mTmpResultDir + '"'
            protectCmd += ' -f "sasl"'
        else:
            raise Exception('[ERROR] Unknown SASL Protector given: %s.' % inSaslProtector)

        print('Trying to run command: ' + protectCmd)
        # secret part
        protectCmd += ' -u ' + self.mSaslProtectLogin + ' -p ' + self.mSaslProtectPass
        os.chdir(self.mWorkingDir)
        if os.system(MyUtils.fixCommandLine(protectCmd)):
            raise Exception('[ERROR] Lua scripts protecting has failed.')

        print('Copying files into target folder...')
        distutils.dir_util.copy_tree(self.mTmpResultDir, self.mTargetDir)

        print('The lua scripts is successfully protected.')

# --------------------------------------------------------#
# main method


def main():
    exit()


# # --------------------------------------------------------#
# # launch
if __name__ == '__main__':
    main()
