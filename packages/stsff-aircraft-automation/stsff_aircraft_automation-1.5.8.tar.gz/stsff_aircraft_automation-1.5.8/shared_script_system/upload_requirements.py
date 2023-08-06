#!/usr/bin/env python
# ----------------------------------------------------------------------------------#
# //////////////////////////////////////////////////////////////////////////////////#
# ----------------------------------------------------------------------------------#

import platform
from conans import ConanFile


class UploadingRequirements(ConanFile):

    def requirements(self):
        self.requires("X-Updater-Dev-Client/last@stsff/master")

    def imports(self):
        if platform.system() == 'Windows':
            self.copy('*', src='win', dst='xupd', root_package='X-Updater-Dev-Client')
        elif platform.system() == 'Linux':
            self.copy('*', src='lin', dst='xupd', root_package='X-Updater-Dev-Client')
        elif platform.system() == 'Darwin':
            self.copy('*', src='mac', dst='xupd', root_package='X-Updater-Dev-Client')