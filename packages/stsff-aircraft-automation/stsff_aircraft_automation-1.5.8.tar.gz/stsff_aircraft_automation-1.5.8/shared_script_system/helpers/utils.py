#!/usr/bin/env python
# ----------------------------------------------------------------------------------#
# //////////////////////////////////////////////////////////////////////////////////#
# ----------------------------------------------------------------------------------#

# DO NOT remove this import!, it is for backward compatibility.
from stsff_automation.utils import *

__author__ = 'StepToSky'

# just leaved this classes here for backward compatibility


class SaslProtector:
    none = ""
    sasl2 = "protector.jar"
    sasl3 = "SASL3Protector.jar"


class ReleaseType:
    alpha = "alpha"
    beta = "beta"
    private_beta = "beta"
    release = "release"


class Context:
    developing = "developing"
    packaging = "packaging"
    context = developing

    def __init__(self, inContext=''):
        if not inContext:
            self.context = self.developing
        elif inContext == self.developing:
            self.context = self.developing
        elif inContext == self.packaging:
            self.context = self.packaging
        else:
            raise Exception('[ERROR] Unknown conan context: %s' % inContext)


# # --------------------------------------------------------#
# # launch
if __name__ == '__main__':
    # print ('result: ' + Utils.get_version_string_from_file('757.ini'))
    exit()
