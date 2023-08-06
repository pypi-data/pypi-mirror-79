#!/usr/bin/env python
# ----------------------------------------------------------------------------------#
# //////////////////////////////////////////////////////////////////////////////////#
# ----------------------------------------------------------------------------------#

import os
import argparse

from helpers.package_helper import PackageHelper
from helpers.loader import Loader
from get_requirements import GetRequirements
from setup_package_info import SetupPackageInfo
from helpers.product_definition_file import *

__author__ = 'StepToSky'


class ProducePackage:
    packHelper = PackageHelper()
    argParser = argparse.ArgumentParser(description=__file__)
    args = ''

    def __init__(self):
        pass

    # --------------------------------------------------------#
    # main method

    def main(self):
        print('[START] %s' % __file__)

        # create helper and prepare dirs and paths
        self.packHelper.setupInputParams()

        # load aircraft definition class
        packageDefinition = Loader.load_product_definition_file(self.packHelper.mProductFile,
                                                                self.packHelper.mWorkingDir)
        self.packHelper.setupPathsAndDirs(packageDefinition.name)

        # clean checking out git index
        if not self.packHelper.mIsGitCheckoutDisabled:
            self.packHelper.makeCleanGitIndex(self.packHelper.mTmpGitIndexDir)

        # create the git revision file, version file and etc...
        SetupPackageInfo(self.packHelper.mOrigWorkingDir,
                         self.packHelper.mWorkingDir,
                         self.packHelper.mProductFile).main()

        # getting requirements
        GetRequirements(self.packHelper.mWorkingDir,
                        self.packHelper.mProductFile,
                        self.packHelper.mConanContext.context).main()

        # create a package
        if packageDefinition.productionList and packageDefinition.releaseExcludeList and packageDefinition.eolConf:
            packageDefinition.onCopyingFiles(True, self.packHelper.mWorkingDir, self.packHelper.mTargetDir)
            self.packHelper.createPackageWithProdList(packageDefinition.productionList, packageDefinition.eolConf)
            packageDefinition.onCopyingFiles(False, self.packHelper.mWorkingDir, self.packHelper.mTargetDir)

        # protecting sasl files
        if packageDefinition.saslProtector != SaslProtector.none:
            self.packHelper.prepareSaslFilesForProtecting(packageDefinition.saslProtector)
            packageDefinition.onProtectingFiles(True, self.packHelper.mWorkingDir, self.packHelper.mTargetDir,
                                                self.packHelper.mTmpSourceDir, self.packHelper.mTmpResultDir)
            self.packHelper.protectAndCopySaslFiles(packageDefinition.saslProductId, packageDefinition.saslProtector)
            packageDefinition.onProtectingFiles(False, self.packHelper.mWorkingDir, self.packHelper.mTargetDir,
                                                self.packHelper.mTmpSourceDir, self.packHelper.mTmpResultDir)

        # strip package for release conf
        if packageDefinition.releaseType == ReleaseType.release:
            self.packHelper.removeNonReleaseFiles(packageDefinition.releaseExcludeList)

        # done
        print('[DONE] %s' % __file__)


# --------------------------------------------------------#
# launch
if __name__ == '__main__':
    obj = ProducePackage()
    try:
        obj.main()
    except Exception as ex:
        # non normal end
        os.chdir(obj.packHelper.mOrigWorkingDir)
        print(ex)
        print('[!!!FAILED!!!] %s' % __file__)
        exit('[!!!FAILED!!!] %s' % __file__)
    # normal end
    os.chdir(obj.packHelper.mOrigWorkingDir)
    exit()
