class apigateway:

    def __init__(self, session):
        self.apiClient = session.client('apigateway')

    def createCustomDomain(self, domain, certarn):
        self.apiClient.create_domain_name(
            domainName=domain,
            certificateArn=certarn
        )

    def deleteCustomDomain(self, domain):
        self.apiClient.delete_domain_name(
            domainName=domain
        )

    def getBasePathbyName(self, domain, basePath):
        self.apiClient.get_base_path_mapping(
            domainName=domain,
            basePath=basePath
        )

    def getBasePaths(self, domain, position=None):
        self.apiClient.get_base_path_mappings(
            domainName=domain,
            position=position,
            limit=500
        )

    def createStage(self, config):
        self.apiClient.create_stage(
            restApiId=config["restapiid"],
            stageName=config["stage"],
            deploymentId=config["deploymentid"],
            description=config["description"],
            cacheClusterEnabled=config["cacheclusterenabled"],
            cacheClusterSize=config["cachesize"],
            variables=config["variables"],
            documentationVersion=config["version"]
        )

    def updateStage(self, domain, stage, patchoperations):
        self.apiClient.update_stage(
            domainName=domain,
            stage=stage,
            patchoperations=patchoperations
        )

    def deleteStage(self, restapiid, stage):
        self.apiClient.update_stage(
            restApiId=restapiid,
            stageName=stage
        )

    def createBasePathMapping(self, domain, basePath, restApiId, stage):
        self.apiClient.create_base_path_mapping(
            domainName=domain,
            basePath=basePath,
            restApiId=restApiId,
            stage=stage
        )

    def updateBasePathMapping(self, domain, basepath, patchoperations):
        self.apiClient.update_base_path_mapping(
            domainName=domain,
            basePath=basepath,
            patchOperations=patchoperations
        )

    def deleteBasePathMapping(self, domain, basePath):
        self.apiClient.delete_base_path_mapping(
            domainName=domain,
            basePath=basePath
        )
