
class beanstalk:

    def __init__(self, session):
        self.bsClient = session.client('elasticbeanstalk')

    def createApplication(self, appname, description, resourcelifecycle):
        self.bsClient.create_application(
            ApplicationName=appname,
            Description=description,
            ResourceLifecycleConfig=resourcelifecycle
        )

    def createApplicationVersion(self, appname, version, description, sourcebuild, buildconfig, autocreate=True, process=True):
        self.bsClient.create_application_version(
            ApplicationName=appname,
            VersionLabel=version,
            Description=description,
            SourceBuildInformation=sourcebuild,
            BuildConfiguration=buildconfig,
            AutoCreateApplication=autocreate,
            Process=process
        )
