#!/usr/bin/env python
# ----------------------------------------------------------------------------------#
# //////////////////////////////////////////////////////////////////////////////////#
# ----------------------------------------------------------------------------------#

import os
import argparse

from helpers.loader import Loader
from helpers.upload_helper import UploadHelper
from helpers.product_definition_file import *

__author__ = 'StepToSky'


class UploadPackage:
    uploadHelper = UploadHelper()
    argParser = argparse.ArgumentParser(description=__file__)
    args = ''

    def __init__(self):
        pass

    # --------------------------------------------------------#
    # main method

    def main(self):
        print('[START] %s' % __file__)

        # create helper and prepare dirs and paths
        self.uploadHelper.setupInputParams()

        # load aircraft definition class
        packageDefinition = Loader.load_product_definition_file(self.uploadHelper.mProductFile,
                                                                self.uploadHelper.mWorkingDir)
        self.uploadHelper.setupPathsAndDirs(packageDefinition.name)

        # x-updater
        if packageDefinition.xupdProductId and packageDefinition.xupdCommitDesc:
            self.uploadHelper.xupdUploadFiles(packageDefinition.xupdProductId,
                                              packageDefinition.releaseType,
                                              "Uploaded by automation script. Release type: %s; Version: %s"
                                              % (packageDefinition.releaseType, packageDefinition.version),
                                              packageDefinition.xupdCommitDesc[packageDefinition.releaseType])

        # ftp legacy variant
        if packageDefinition.ftpServer:
            if packageDefinition.releaseType == ReleaseType.release:
                self.uploadHelper.ftpUploadFiles(packageDefinition.ftpServer,
                                                 packageDefinition.name,
                                                 packageDefinition.ftpArchiveName)
        if packageDefinition.betaFtpServer:
            if packageDefinition.releaseType == ReleaseType.beta:
                self.uploadHelper.ftpUploadFiles(packageDefinition.betaFtpServer,
                                                 packageDefinition.name + "-BETA",
                                                 packageDefinition.betaFtpArchiveName)

        # ftp
        if len(packageDefinition.ftpServers) and len(packageDefinition.ftpUploads):
            self.uploadHelper.upload_to_ftp(packageDefinition)

        # ssh
        if len(packageDefinition.sshServers) and len(packageDefinition.sshUploads):
            self.uploadHelper.upload_over_ssh(packageDefinition)

        # done
        print('[DONE] %s' % __file__)


# --------------------------------------------------------#
# launch
if __name__ == '__main__':
    obj = UploadPackage()
    try:
        obj.main()
    except Exception as ex:
        # non normal end
        os.chdir(obj.uploadHelper.mOrigWorkingDir)
        print(ex)
        print('[!!!FAILED!!!] %s' % __file__)
        exit('[!!!FAILED!!!] %s' % __file__)
    # normal end
    os.chdir(obj.uploadHelper.mOrigWorkingDir)
    exit()
