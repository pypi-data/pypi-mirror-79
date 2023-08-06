#!/usr/bin/env python
# ----------------------------------------------------------------------------------#
# //////////////////////////////////////////////////////////////////////////////////#
# ----------------------------------------------------------------------------------#

import platform

__author__ = 'StepToSky'


class MyUtils:

    @staticmethod
    def fixCommandLine(inCmdLine):
        if platform.system() == "Windows":
            return '"' + inCmdLine + '"'
        else:
            return inCmdLine
