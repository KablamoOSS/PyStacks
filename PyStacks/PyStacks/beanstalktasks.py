import sys
import logging
import beanstalk
import s3tasks
from botocore.exceptions import ClientError


class beanstalktasks:

    def __init__(self):
        pass

    def createApplication(self, session, config, logoutput=None):
        bs = beanstalk.beanstalk(session)
        try:
            bs.createApplication(appname=config["appname"], description=config["description"], resourcelifecycle=config["resourcelifecycle"])
        except ClientError as err:
            print "Error setting Resolver to Delegation Set."
            logging.warn(err)
            sys.exit(1)

    def createApplicationVersion(self, session, config, logoutput=None):
        bs = beanstalk.beanstalk(session)
        if config["sourcebuld"]["Type"] == "S3":
            sourcebuild = self.SourceBuildInformationZip(session=session, config=config["sourcebuld"])
        else:
            sourcebuild = self.SourceBuildInformationGit(config=config["sourcebuld"])
        buildconfig = self.BuildConfiguration(config=config["BuildConfig"])
        try:
            bs.createApplicationVersion(appname=config["appname"], version=config["version"], description=config["description"], sourcebuild=sourcebuild, buildconfig=buildconfig)
        except ClientError as err:
            print "Error setting Resolver to Delegation Set."
            logging.warn(err)
            sys.exit(1)

    def SourceBuildInformationZip(self, session, config):
        buildinfo = {}
        sourceinfo = []
        sourceinfo["SourceType"] = "Zip"
        sourceinfo["SourceType"] = "S3"
        s3 = s3tasks.S3tasks()
        s3.uploadFile(session, config["filename"], config["bucket"], key=config["project"] + config["filename"])
        response = s3.checkForFileV2(filename=config["filename"], bucket=config["bucket"])
        if response:
            sourceinfo["SourceLocation"] = config["bucket"] + config["project"] + config["filename"]
        buildinfo.append(sourceinfo)

        return buildinfo

    def SourceBuildInformationGit(self, config):
        buildinfo = {}
        sourceinfo = []
        sourceinfo["SourceType"] = "Git"
        sourceinfo["SourceType"] = "CodeCommit"
        sourceinfo["SourceLocation"] = config["projectname"]
        buildinfo.append(sourceinfo)

        return buildinfo

    def BuildConfiguration(self, config):
        buildconfig = {}
        configvar = []
        configvar['CodeBuildServiceRole'] = config["BuildRole"]
        configvar['ComputeType'] = 'BUILD_GENERAL1_MEDIUM'
        configvar['Image'] = config["Image"]
        configvar['TimeoutInMinutes'] = 10
        buildconfig.append(configvar)

        return buildconfig
