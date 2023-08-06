#!/usr/bin/env python
# ----------------------------------------------------------------------------------#
# //////////////////////////////////////////////////////////////////////////////////#
# ----------------------------------------------------------------------------------#


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


class UploadEntry:
    def __init__(self, serverAlias, customArchiveName=None,
                 remotePathPrefix=b'.',
                 additionalFilesToUpload=None, onlyAdditionalFiles=False):
        if additionalFilesToUpload is None:
            additionalFilesToUpload = []
        self.serverAlias = serverAlias
        self.customArchiveName = customArchiveName
        self.remotePathPrefix = remotePathPrefix
        self.additionalFilesToUpload = additionalFilesToUpload
        self.onlyAdditionalFiles = onlyAdditionalFiles


class FtpUploadEntry(UploadEntry):
    # as backward compatible class name
    pass


class ProductDefinitionFile:
    # product version string, like "1.2.3" or "1.0.0-snapshot"
    version = None
    # product id, like "B752FPDS"
    id = None
    # product name, like "Boeing 757-200 FPDS"
    name = None

    # creating some files automatically
    # if set will create a file with actual git revision
    gitRevisionFile = None
    # if set will create a file with product version in format like 1.2.3 -> 010203
    versionFile = None

    # release type
    releaseType = ReleaseType.alpha

    # packaging, you should define ALL these three parameters if you want to enable the step!
    # a txt file with list of files should be copied into result package
    productionList = None
    # a txt file with list of files should be excluded from result package if the release type is Release.
    releaseExcludeList = None
    # config for replacing eol
    eolConf = None

    # sasl protection
    # sasl protector version or none for no protection step
    saslProtector = SaslProtector.none
    # product id in sasl system
    saslProductId = -1

    # uploading to x-updater
    # if both parameters are set, will upload to the x-updater system
    xupdProductId = None
    # a dict with release types as keys and txt files paths as values
    # the file for actual release type will be used as a commit description
    # Example:
    # xupdCommitDesc = {ReleaseType.alpha: "path/to/file_for_alpha.txt",
    #                   ReleaseType.release: "path/to/file_for_release.txt"}
    xupdCommitDesc = None

    # legacy uploading to ftp
    # this is legacy stuff, do NOT use this please
    ftpServer = None
    ftpArchiveName = {}
    betaFtpServer = None
    betaFtpArchiveName = {}

    # uploading to ftp
    # ftp servers dict
    # where an alias as key and address as value
    # example:
    # ftpServers = {"ORG": "ftp.keycdn.com", "TEST": "ftp.test.server.loc"}
    ftpServers = {}
    # Example:
    # ftpUploads = {
    #     ReleaseType.release: [
    #         FtpUploadEntry("ORG"),
    #         FtpUploadEntry("ORG", additionalFilesToUpload=["DOCs/changelog.txt"]),
    #     ],
    #     ReleaseType.beta: [
    #         FtpUploadEntry("ORG", name + "-BETA"),
    #         FtpUploadEntry("ORG", name + "-BETA", additionalFilesToUpload=["DOCs/changelog.txt"]),
    #         FtpUploadEntry("ORG", name + "-BETA", additionalFilesToUpload={"DOCs/changelog.txt": "custom_target_name.txt"}),
    #     ],
    # }
    ftpUploads = {}

    sshServers = {}
    sshUploads = {}

    # callbacks to customize some steps
    def onCopyingFiles(self, isBefore, inWorkDir, inTargetDir):
        print("[INFO] onCopyingFiles() step is not defined for %s." % self.id)

    def onProtectingFiles(self, isBefore, inWorkDir, inTargetDir, inTmpSourceDir, inTmpResultDir):
        print("[INFO] onProtectingFiles() step is not defined for %s." % self.id)

# ----------------------------------------------------------------------------------#
# //////////////////////////////////////////////////////////////////////////////////#
# ----------------------------------------------------------------------------------#
