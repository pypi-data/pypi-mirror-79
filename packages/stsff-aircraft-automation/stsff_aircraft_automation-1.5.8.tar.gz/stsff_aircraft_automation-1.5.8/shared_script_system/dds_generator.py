#!/usr/bin/env python
# ----------------------------------------------------------------------------------#
# //////////////////////////////////////////////////////////////////////////////////#
# ----------------------------------------------------------------------------------#

import os
import sys
import platform
import hashlib
import argparse
from helpers.my_utils import MyUtils

__author__ = 'StepToSky'

# --------------------------------------------------------#
# class


class DdsGenerator:

    mDdsToolName = 'DDSTool'
    mDdsToolLaunchName = 'DDSTool'
    mDdsToolPath = ''

    mFileWithList = ''
    mIsGenerationForced = False

    mArgParser = argparse.ArgumentParser(description='Dds Generator Arg Parser.')

    def __init__(self):
        if platform.system() == 'Windows':
            self.mDdsToolName = 'DDSTool-Win.exe'
        self.mDdsToolPath = os.path.normpath(os.path.join(os.path.dirname(__file__), 'helpers', 'bin', self.mDdsToolName))
        self.mDdsToolLaunchName = self.mDdsToolPath

        self.mArgParser.add_argument('-l', '--file_list',
                                     help='A file with list of png files to process. '
                                          'By default - <automation/dds_generator_list.txt>.',
                                     default='automation/dds_generator_list.txt')

        self.mArgParser.add_argument('-f', '--force_regenerate', action='store_true',
                                     help='Will regenerate dds files in any case',)

        # parse
        args = self.mArgParser.parse_args(sys.argv[1:])
        if args.file_list:
            self.mFileWithList = args.file_list
        if args.force_regenerate:
            self.mIsGenerationForced = args.force_regenerate

    def processFiles(self, inFile=''):
        fileName = self.mFileWithList
        if inFile != '':
            fileName = inFile
        count = 0
        with open(fileName, 'r') as f:
            for line in f:
                line = line.strip()
                if len(line) > 5:
                    # processing one file
                    self.processPngFile(line)
                    count += 1
        print('Processing is done, processed ' + str(count) + ' files.')

    def processPngFile(self, inFile):
        print('Process png file: <' + inFile + '>')
        status, checkSum = self.isDdsOutdatedForFile(inFile)
        if status or self.mIsGenerationForced:
            pre, ext = os.path.splitext(inFile)
            ddsFile = pre + '.dds'
            print('The dds creation is required for file: <' + inFile + '>')
            self.createDdsFile(inFile, checkSum, ddsFile)
        else:
            print('The dds creation is skipped for file: <' + inFile + '>')

    @staticmethod
    def isDdsOutdatedForFile(inFile):
        hash_md5 = hashlib.md5()
        with open(inFile, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        actualCheckSum = hash_md5.hexdigest()

        pre, ext = os.path.splitext(inFile)
        ddsFile = pre + '.dds'
        if not os.path.exists(inFile + '.checksum') or not os.path.exists(ddsFile):
            return True, actualCheckSum
        with open(inFile + '.checksum', 'r') as fileHandle:
            savedCheckSum = fileHandle.read()
        if savedCheckSum == actualCheckSum:
            return False, actualCheckSum
        else:
            return True, actualCheckSum

    def createDdsFile(self, inSrcFile, inActCheckSum, inDestFile):
        print('Creating a dds file from the png file: <' + inSrcFile + '> ...')
        processCmd = '"' + self.mDdsToolLaunchName + '"'
        processCmd += ' --png2dxt'
        processCmd += ' --dummy_arg1 --dummy_arg2'
        processCmd += ' "' + inSrcFile + '"'
        processCmd += ' "' + inDestFile + '"'
        print('Trying to run command: ' + processCmd)

        if os.system(MyUtils.fixCommandLine(processCmd)):
            raise Exception('[ERROR] Creating a dds file has failed.')

        with open(inSrcFile + '.checksum', 'w') as fileHandle:
            fileHandle.write(inActCheckSum)

        print('Adding created the dds and checksum files into git index ...')
        gitAddCmd = 'git add'
        gitAddCmd += ' "' + inDestFile + '"'
        gitAddCmd += ' "' + inSrcFile + '.checksum"'
        # gitAddCmd += ' --dry-run'
        print('Trying to run command: ' + gitAddCmd)

        if os.system(MyUtils.fixCommandLine(gitAddCmd)):
            raise Exception('[ERROR] Adding the dds and checksum files to git index has failed.')

        print('The dds and checksum files have been created and added to git index: <' + inDestFile + '>')


# --------------------------------------------------------#
# main method


def main():
    try:
        helper = DdsGenerator()
        helper.processFiles()

    except Exception as ex:
        print(ex)
        print('[Creating dds files - FAILED!!!]')
        exit('[Creating dds files - FAILED!!!]')

    print('[Creating dds files - done]')
    exit()


# # --------------------------------------------------------#
# # launch
if __name__ == '__main__':
    main()
