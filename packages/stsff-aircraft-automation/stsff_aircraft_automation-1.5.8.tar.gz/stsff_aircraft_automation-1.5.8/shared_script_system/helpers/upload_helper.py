#!/usr/bin/env python
# ----------------------------------------------------------------------------------#
# //////////////////////////////////////////////////////////////////////////////////#
# ----------------------------------------------------------------------------------#
import logging
import os
import sys
import stat
import shutil
import platform
from shutil import copyfile
from typing import re

from helpers.base_helper import BaseHelper
from stsff_automation.utils import Utils
from helpers.product_definition_file import *
from helpers.my_utils import MyUtils

__author__ = 'StepToSky'


# --------------------------------------------------------#
# class


class UploadHelper(BaseHelper):
    # --------------------------------------------------------#
    # Members

    isPython3InUse = (sys.version_info[0] >= 3)

    mConanDepsFileName = os.path.normpath(os.path.join(os.path.dirname(__file__), '../upload_requirements.py'))

    # mTmpDir/"uploading"
    mTmpUploadingDir = ''

    mXupdClient = 'xupd'
    mXupdDeveloperApiKey = ''

    mIsDryLaunch = False

    # --------------------------------------------------------#
    # Methods

    def __init__(self):
        super(UploadHelper, self).__init__()
        self.mXupdClient = os.path.normpath(os.path.join(self.mWorkingDir, 'automation/tmp/uploading/xupd/xupd'))
        if platform.system() == 'Windows':
            self.mXupdClient += '.exe'

    def setupCliArgs(self):
        super(UploadHelper, self).setupCliArgs()
        print("Setting up command line input...")

        self.mArgParser.add_argument('--dry_launch', action='store_true',
                                     help='if set, there will be no any real uploading.')

        print("Setting up the command line input is done.")

    def parseCliArgs(self):
        super(UploadHelper, self).parseCliArgs()
        print("Parsing command line input...")

        if self.mArgs.dry_launch:
            self.mIsDryLaunch = True

        print("Parsing command line input is done.")

    def setupParamsFromEnv(self):
        super(UploadHelper, self).setupParamsFromEnv()
        print('Setting up params from env, if it is needed ...')

        if not self.mXupdDeveloperApiKey:
            self.mXupdDeveloperApiKey = os.environ.get(self.mEnvPrefix + 'XUPD_DEVELOPER_KEY')

        print('Setting up params from env is done.')

    def setupPaths(self, inPackageName):
        super(UploadHelper, self).setupPaths(inPackageName)
        self.mTmpUploadingDir = os.path.join(self.mTmpDir, 'uploading')

    def checkAndCreateDirs(self):
        super(UploadHelper, self).checkAndCreateDirs()
        if os.path.exists(self.mTmpUploadingDir):
            shutil.rmtree(self.mTmpUploadingDir)
        self.checkAndCreateDir(self.mTmpUploadingDir)

    def setupInputParams(self):
        super(UploadHelper, self).setupInputParams()
        self.getRequirements()

    def getRequirements(self):
        print('Installing uploading requirements: ')
        getXupdCmd = 'conan install'
        getXupdCmd += ' --update --no-imports'
        getXupdCmd += ' -if automation/tmp/uploading'
        getXupdCmd += ' "%s"' % self.mConanDepsFileName
        print('Trying to run command: ' + getXupdCmd)
        os.chdir(self.mWorkingDir)
        if os.system(MyUtils.fixCommandLine(getXupdCmd)):
            raise Exception('[ERROR] Installing uploading requirements has failed.')

        getXupdCmd = 'conan imports'
        getXupdCmd += ' -imf automation/tmp/uploading'
        getXupdCmd += ' -if automation/tmp/uploading'
        getXupdCmd += ' "%s"' % self.mConanDepsFileName
        print('Trying to run command: ' + getXupdCmd)
        os.chdir(self.mWorkingDir)
        if os.system(MyUtils.fixCommandLine(getXupdCmd)):
            raise Exception('[ERROR] Importing uploading requirements has failed.')

        state = os.stat(self.mXupdClient)
        os.chmod(self.mXupdClient, state.st_mode | stat.S_IEXEC)

        print('Installing uploading requirements is done.')

    # --------------------------------------------------------#
    # utils

    def ftpCredentialsForAlias(self, ftpServerAlias):
        ftpUser = os.environ.get(self.mEnvPrefix + 'FTP_USER' + '_' + ftpServerAlias)
        ftpPass = os.environ.get(self.mEnvPrefix + 'FTP_PASS' + '_' + ftpServerAlias)
        if not ftpUser:
            ftpUser = os.environ.get(self.mEnvPrefix + 'FTP_USER')
        if not ftpPass:
            ftpPass = os.environ.get(self.mEnvPrefix + 'FTP_PASS')
        if not ftpUser:
            raise Exception('[ERROR] The ftp user for the ftp server %s:$s is not set.'
                            'You can use global env: STSFF_FTP_USER or with server alias: STSFF_FTP_USER_SERVERALIAS')
        if not ftpPass:
            raise Exception('[ERROR] The ftp pass for the ftp server %s:$s is not set.'
                            'You can use global env: STSFF_FTP_PASS or with server alias: STSFF_FTP_PASS_SERVERALIAS')

        return ftpUser, ftpPass

    @staticmethod
    def ftpArchiveNameForAlias(ftpServerAlias, archiveNames, defaultArchiveName):
        if ftpServerAlias in archiveNames:
            return archiveNames[ftpServerAlias]
        else:
            return defaultArchiveName

    def sshCredentialsForAlias(self, sshServerAlias):
        ssh_user = os.environ.get(self.mEnvPrefix + 'SSH_USER' + '_' + sshServerAlias)
        ssh_pass = os.environ.get(self.mEnvPrefix + 'SSH_PASS' + '_' + sshServerAlias)
        ssh_key_file = os.environ.get(self.mEnvPrefix + 'SSH_KEY_FILE' + '_' + sshServerAlias)
        ssh_key_pass = os.environ.get(self.mEnvPrefix + 'SSH_KEY_PASS' + '_' + sshServerAlias)
        if not ssh_user:
            ssh_user = os.environ.get(self.mEnvPrefix + 'SSH_USER')
        if not ssh_pass:
            ssh_pass = os.environ.get(self.mEnvPrefix + 'SSH_PASS')
        if not ssh_key_file:
            ssh_key_file = os.environ.get(self.mEnvPrefix + 'SSH_KEY_FILE')
        if not ssh_key_pass:
            ssh_key_pass = os.environ.get(self.mEnvPrefix + 'SSH_KEY_PASS')
        if not ssh_user:
            raise Exception('[ERROR] The SSH user for the SSH server %s:$s is not set.'
                            'You can use env: STSFF_SSH_USER[_SERVERALIAS]')
        if not ssh_pass and not ssh_key_file:
            raise Exception('[ERROR] Neither of SSH pass nor SSH key for the SSH server %s:$s is not set.'
                            'You can use env: STSFF_SSH_PASS[_SERVERALIAS] or STSFF_SSH_KEY_FILE[_SERVERALIAS] ')

        return ssh_user, ssh_pass, ssh_key_file, ssh_key_pass

    # --------------------------------------------------------#
    # upload to X-Updater

    def xupdSetup(self, productId, commitDescFile):
        print('Setting up the x-updater configuration: ')

        initCmd = '"' + self.mXupdClient + '" init'
        initCmd += ' -productId ' + productId
        print('Trying to run command: ' + initCmd)
        os.chdir(self.mTargetDir)
        if os.system(MyUtils.fixCommandLine(initCmd)):
            raise Exception('[ERROR] Setting up the x-updater configuration has failed.')
        print('Setting up the x-updater configuration is done.')

        print('Setting up the x-updater package description file: ')
        copyfile(commitDescFile, "x-updater/description.txt")
        print('Setting up the x-updater package description file is done.')

        os.chdir(self.mTargetDir)
        Utils.download_xupdater_client()

    def xupdShowFilesWillBeUploaded(self):
        print('Checking files which will to be uploaded to X-Updater: ')

        statusCmd = '"' + self.mXupdClient + '" status'
        print('Trying to run command: ' + statusCmd)
        if self.mXupdDeveloperApiKey:
            statusCmd += ' -apiKey ' + self.mXupdDeveloperApiKey

        os.chdir(self.mTargetDir)
        if os.system(MyUtils.fixCommandLine(statusCmd)):
            raise Exception('[ERROR] Checking files which will to be uploaded to X-Updater has failed.')

        print('Checking files which will to be uploaded to X-Updater is done.')

    def xupdUploadFiles(self, productId, releaseType, commitNote, commitDescFile):
        self.xupdSetup(productId, commitDescFile)
        self.xupdShowFilesWillBeUploaded()
        if not self.mIsSilentMode:
            if self.isPython3InUse:
                userInput = input('Upload these files to the X-Updater Server? yes/no:').lower()
            else:
                userInput = raw_input('Upload these files to the X-Updater Server? yes/no:').lower()
            if userInput != 'y' and userInput != 'yes' and userInput != '1':
                print('Uploading to X-Updater has been canceled by user.')
                return

        # uploading
        print('Uploading files to X-Updater: ')
        uploadCmd = '"' + self.mXupdClient + '" commit'
        uploadCmd += ' -desc "' + commitNote + '"'
        uploadCmd += ' -type ' + releaseType
        uploadCmd += ' -force'
        print('Trying to run command: ' + uploadCmd)
        if self.mXupdDeveloperApiKey:
            uploadCmd += ' -apiKey ' + self.mXupdDeveloperApiKey

        os.chdir(self.mTargetDir)
        if not self.mIsDryLaunch:
            if os.system(MyUtils.fixCommandLine(uploadCmd)):
                raise Exception('[ERROR] Uploading files to X-Updater has failed.')
        else:
            print('The Dry launch has been set up, so there is no any real uploading.')

        print('Uploading files to X-Updater is done.')

    # --------------------------------------------------------#
    # upload to FTP

    def create_package_archive(self, archive_name):
        # removing old archive
        archiveBasePath = os.path.join(self.mTmpUploadingDir, archive_name)
        archiveFullName = archiveBasePath + '.zip'
        if os.path.exists(archiveFullName):
            print('Removing the old prepared archive: ' + archiveFullName)
            os.remove(archiveFullName)
        # creating new archive
        print('Creating the new archive for uploading: ' + archiveFullName)
        shutil.make_archive(base_name=archiveBasePath,
                            format='zip',
                            root_dir=self.mProdDir,
                            base_dir=os.path.basename(os.path.normpath(self.mTargetDir)))
        return archiveFullName

    def convert_file_if_needed(self, orig_file, target_file):
        orig_ext = os.path.splitext(orig_file)[1]
        target_ext = os.path.splitext(target_file)[1]
        # no convert needed
        if orig_ext == target_ext:
            return orig_file
        if orig_ext == ".txt" and target_ext == ".html":
            converted_file_path = os.path.join(self.mTmpUploadingDir, target_file)
            print('Will convert from (' + orig_file + ') to (' + converted_file_path + ')')
            if os.path.exists(converted_file_path):
                print('Removing the old converted file: ' + converted_file_path)
                os.remove(converted_file_path)
            with open(orig_file) as reader:
                with open(converted_file_path, 'w') as writer:
                    writer.write("<!DOCTYPE html>\n")
                    writer.write('<html lang="en">\n')
                    writer.write('<head>\n')
                    writer.write('<title>'+target_file+'</title>\n')
                    writer.write('</head>\n')
                    writer.write('<body><pre>\n')
                    for orig_line in reader:
                        writer.write(orig_line)
                    writer.write('</pre></body>\n')
                    writer.write("</html>\n")
            print('Converted file is written to (' + converted_file_path + ')')
            return converted_file_path
        #
        raise Exception("[ERROR] Conversion from (" + orig_file + ") to (" + target_file + ") is not supported!")

    def upload_one_file_to_ftp(self, ftp, file_path, target_name=None):
        if not target_name:
            target_name = os.path.basename(file_path)
        file_path = self.convert_file_if_needed(file_path, target_name)
        print('Uploading file: <%s> as <%s>' % (file_path, target_name))
        newName = target_name + '.new'
        oldName = target_name + '.old'
        if not self.mIsDryLaunch:
            fileToUpload = open(file_path, 'rb')
            ftp.storbinary('STOR ' + newName, fileToUpload)
            fileToUpload.close()
            try:
                print('Trying to rename the current file (' + target_name + ') to: ' + oldName)
                ftp.rename(target_name, oldName)
            except Exception as ex:
                print(ex)

            print('Trying to rename the uploaded file (' + newName + ') to the current: ' + target_name)
            ftp.rename(newName, target_name)
            try:
                print('Trying to delete the old file: ' + oldName)
                ftp.delete(oldName)
            except Exception as ex:
                print(ex)
        else:
            print('The Dry launch has been set up, so there is no any real uploading.')

    def upload_to_ftp(self, package: ProductDefinitionFile):
        print('Uploading files to FTP Servers: ')
        os.chdir(self.mTargetDir)
        for rel_type, uploads in package.ftpUploads.items():
            if rel_type == package.releaseType:
                #upload: FtpUploadEntry
                for upload in uploads:
                    if upload.serverAlias not in package.ftpServers:
                        raise Exception("[ERROR] Cannot find specified ftp server alias [%s] "
                                        "in the ftp server list." % upload.serverAlias)
                    ftpAddress = package.ftpServers[upload.serverAlias]
                    print('Uploading files to the FTP Server: %s: %s' % (upload.serverAlias, ftpAddress))
                    ftpUser, ftpPass = self.ftpCredentialsForAlias(upload.serverAlias)
                    archiveName = package.name
                    if upload.customArchiveName:
                        archiveName = upload.customArchiveName
                    if not self.mIsSilentMode:
                        userInput = input('Upload the package (' + archiveName + ') '
                                                                                 'to the selected FTP Server '
                                                                                 '(' + upload.serverAlias + ': ' + ftpAddress + ')? yes/no:').lower()
                        if userInput != 'y' and userInput != 'yes' and userInput != '1':
                            print('Uploading to the selected FTP server has been canceled by user.')
                            continue

                    archiveFullName = self.create_package_archive(archiveName)
                    print('Connecting to a FTP Server: ' + ftpAddress)
                    import ftplib
                    ftp = ftplib.FTP(ftpAddress, ftpUser, ftpPass)
                    self.upload_one_file_to_ftp(ftp, archiveFullName)
                    if isinstance(upload.additionalFilesToUpload, dict):
                        for file, tgt_name in upload.additionalFilesToUpload.items():
                            self.upload_one_file_to_ftp(ftp, file, archiveName + "_" + os.path.basename(tgt_name))
                    else:
                        for file in upload.additionalFilesToUpload:
                            self.upload_one_file_to_ftp(ftp, file, archiveName + "_" + os.path.basename(file))
                    ftp.close()
                    print('Uploading files to the FTP Server: %s: %s is done.' % (upload.serverAlias, ftpAddress))

        print('Uploading to FTP Servers is done.')

    # legacy
    def ftpUploadFiles(self, ftpServers, archiveName, archiveNames=None):
        print('[LEGACY] Uploading files to FTP Servers: ')
        os.chdir(self.mTargetDir)

        for alias, server in ftpServers.items():
            # some setup for current ftp server
            ftpUser, ftpPass = self.ftpCredentialsForAlias(alias)
            if archiveNames is not None:
                archiveName = self.ftpArchiveNameForAlias(alias, archiveNames, archiveName)
            if not self.mIsSilentMode:
                if self.isPython3InUse:
                    userInput = input('[LEGACY] Upload the package (' + archiveName + ') '
                                                                                      'to the selected FTP Server (' + server + ')? yes/no:').lower()
                else:
                    userInput = raw_input('[LEGACY] Upload the package (' + archiveName + ') '
                                                                                          'to the selected FTP Server (' + server + ')? yes/no:').lower()
                if userInput != 'y' and userInput != 'yes' and userInput != '1':
                    print('[LEGACY] Uploading to the selected FTP server has been canceled by user.')
                    return

            archiveFullName = self.create_package_archive(archiveName)
            print('[LEGACY] Connecting to a FTP Server: ' + server)
            import ftplib
            ftp = ftplib.FTP(server, ftpUser, ftpPass)
            self.upload_one_file_to_ftp(ftp, archiveFullName)
            ftp.close()
            print('[LEGACY] Uploading to a FTP Server (' + server + ') is done.')

        print('[LEGACY] Uploading to FTP Servers is done.')

    # --------------------------------------------------------#
    # upload over ssh (scp)

    def upload_one_file_over_ssh(self, scp, local_file, remote_path_prefix, target_name = None):
        if not target_name:
            target_name = os.path.basename(local_file)
        local_file = self.convert_file_if_needed(local_file, target_name)
        print('Uploading file: <%s> as <%s>' % (local_file, target_name))
        if not self.mIsDryLaunch:
            scp.put(local_file, remote_path=remote_path_prefix + "/" + target_name)
        else:
            print('The Dry launch has been set up, so there is no any real uploading.')

    def upload_over_ssh(self, package: ProductDefinitionFile):
        print('Uploading files over SSH: ')
        os.chdir(self.mTargetDir)
        for rel_type, uploads in package.sshUploads.items():
            if rel_type == package.releaseType:
                #upload: FtpUploadEntry
                for upload in uploads:
                    if upload.serverAlias not in package.sshServers:
                        raise Exception("[ERROR] Cannot find specified SSH server alias [%s] "
                                        "in the SSH server list." % upload.serverAlias)
                    ssh_address = package.sshServers[upload.serverAlias]
                    print('Uploading files to the SSH Server: %s: %s' % (upload.serverAlias, ssh_address))
                    ssh_user, ssh_pass, ssh_key_file, ssh_key_pass = self.sshCredentialsForAlias(upload.serverAlias)
                    archive_full_name = None
                    archive_name = package.name
                    if upload.customArchiveName:
                        archive_name = upload.customArchiveName
                    if not self.mIsSilentMode:
                        userInput = input('Upload the package (' + archive_name + ') '
                                                                                  'to the selected SSH Server '
                                                                                  '(' + upload.serverAlias + ': ' + ssh_address + ')? yes/no:').lower()
                        if userInput != 'y' and userInput != 'yes' and userInput != '1':
                            print('Uploading to the selected SSH server has been canceled by user.')
                            continue
                    if not upload.onlyAdditionalFiles:
                        archive_full_name = self.create_package_archive(archive_name)
                    # SSH
                    print('Connecting to a SSH Server: ' + ssh_address)
                    import paramiko
                    import scp
                    paramiko.util.logging.getLogger().setLevel(logging.DEBUG)
                    ssh_key = None
                    if ssh_key_file:
                        ssh_key = paramiko.RSAKey.from_private_key_file(ssh_key_file)
                    with paramiko.SSHClient() as ssh:
                        ssh.load_system_host_keys()
                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        ssh.connect(ssh_address, username=ssh_user, password=ssh_pass, passphrase=ssh_key_pass,
                                    pkey=ssh_key, look_for_keys=True, allow_agent=True)
                        with scp.SCPClient(ssh.get_transport()) as scp_client:
                            # uploading main archive if needed
                            if not upload.onlyAdditionalFiles and archive_full_name:
                                self.upload_one_file_over_ssh(scp_client, archive_full_name, upload.remotePathPrefix)
                            # uploading additional files
                            if isinstance(upload.additionalFilesToUpload, dict):
                                for file, tgt_name in upload.additionalFilesToUpload.items():
                                    self.upload_one_file_over_ssh(scp_client, file, upload.remotePathPrefix,
                                                                  archive_name + "_" + os.path.basename(tgt_name))
                            else:
                                for file in upload.additionalFilesToUpload:
                                    self.upload_one_file_over_ssh(scp_client, file, upload.remotePathPrefix,
                                                                  archive_name + "_" + os.path.basename(file))
                    print('Uploading files to the SSH Server: %s: %s is done.' % (upload.serverAlias, ssh_address))
        print('Uploading over SSH is done.')


# --------------------------------------------------------#
# main method


def main():
    exit()


# # --------------------------------------------------------#
# # launch
if __name__ == '__main__':
    main()
