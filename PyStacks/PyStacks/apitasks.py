import sys
import logging
import apigateway
import dns.resolver
from botocore.exceptions import ClientError


class apitasks:

    def __init__(self):
        pass

    def createAPIDomain(self, domain, certarn, session):
        api = apigateway.apigateway(session)
        try:
            api.createCustomDomain(domain=domain, certarn=certarn)
        except ClientError as err:
            logging.warn(err)
            sys.exit(1)

    def deleteAPIDomain(self, domain, certarn, session):
        api = apigateway.apigateway(session)
        try:
            api.deleteCustomDomain(domain=domain)
        except ClientError as err:
            logging.warn(err)
            sys.exit(1)

    def createAPIStage(self, config, session):
        api = apigateway.apigateway(session)
        apiconfig = config["apigateway"]
        try:
            api.createStage(restapiid=apiconfig["restapiid"], stage=apiconfig["stage"], deploymentid=apiconfig["deploymentid"], description=apiconfig["description"], cacheclusterenabled=apiconfig["cacheclusterenabled"], cachesize=apiconfig["cachesize"], variables=apiconfig["variables"], version=apiconfig["version"])
        except ClientError as err:
            logging.warn(err)
            sys.exit(1)

    def updateAPIStage(self, config, session):
        api = apigateway.apigateway(session)
        apiconfig = config["apigateway"]
        try:
            api.createStage(restapiid=apiconfig["restapiid"], stage=apiconfig["stage"], deploymentid=apiconfig["deploymentid"], description=apiconfig["description"], cacheclusterenabled=apiconfig["cacheclusterenabled"], cachesize=apiconfig["cachesize"], variables=apiconfig["variables"], version=apiconfig["version"])
        except ClientError as err:
            logging.warn(err)
            sys.exit(1)

    def createAPIBasePathMapping(self, domain, basePath, restApiId, stage, session):
        api = apigateway.apigateway(session)
        try:
            api.createBasePathMapping(domain=domain, basePath=basePath, restApiId=restApiId, stage=stage)
        except ClientError as err:
            logging.warn(err)
            sys.exit(1)

    def deleteAPIBasePathMapping(self, domain, basePath, session):
        api = apigateway.apigateway(session)
        try:
            api.deleteBasePathMapping(domain=domain, basePath=basePath)
        except ClientError as err:
            logging.warn(err)
            sys.exit(1)

    def generatePatchOperationsfromConfig(self, config):
        pathops = []
        pathops["op"] = config["op"]
        pathops["path"] = config["path"]
        pathops["value"] = config["value"]

        return pathops

    def generatePatchOperationsfromVar(self, op, path, value):
        pathops = []
        pathops["op"] = op
        pathops["path"] = path
        pathops["value"] = value

        return pathops

    def queryDomain(self, domain):
        try:
            records = dns.resolver.query(domain, 'CNAME')
        except:
            records = []
            print("No records for this search")
        return [str(x.target) for x in records]

    def findBlueGreenStack(self, domain, cloudfrontBlue, cloudfrontGreen):
        records = self.queryDomain(domain)
        # return the non-live stack name based on the active dns
        if cloudfrontGreen in records:
            return 'Blue'
        elif cloudfrontBlue in records:
            return 'Green'
        else:
            raise Exception('No active stack found')
