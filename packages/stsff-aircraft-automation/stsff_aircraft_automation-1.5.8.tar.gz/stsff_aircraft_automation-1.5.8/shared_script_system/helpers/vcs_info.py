#!/usr/bin/env python
# ----------------------------------------------------------------------------------#
# //////////////////////////////////////////////////////////////////////////////////#
# ----------------------------------------------------------------------------------#

# DO NOT remove this import! It is for backward compatibility.
from stsff_automation.vcs_info import *

__author__ = 'StepToSky'

# this hack is for backward compatibility


class VcsInfo(VcsInfo):
    def __init__(self, workingDir='', vcsInfoFile='automation/tmp/vcs_info'):
        super(VcsInfo, self).__init__(working_dir=workingDir, vcs_info_file=vcsInfoFile)
