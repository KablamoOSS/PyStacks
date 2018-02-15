from invoke import task
import auth
import configs
import zonefile
import sys
import json
import database
import cloudformation
import cloudformationtasks
import pprint
import logging
import kmstasks
import apitasks
import lambdatasks
import configtasks
import ec2tasks
import s3tasks
import route53tasks
import beanstalktasks
import organizationstasks
import awsinputs
import ecs
from greengrasstasks import create_group_with_config

from random import randint
from serverless_tasks import ServerlessTasks
from botocore.exceptions import ClientError

from logger import get_pystacks_log
log = get_pystacks_log()


@task
def generateTemplate(ctx, stack, region, githash=None, environment=None, logoutput=None, outFile=None, customConfig=None):
    cftasks = cloudformationtasks.cloudformationtasks()
    cftasks.generateTemplate(stack=stack, region=region, githash=githash, environment=environment, logoutput=logoutput, outFile=outFile, customConfig=customConfig)


@task
def generateTemplateS3(ctx, stack, region, githash=None, environment=None, logoutput=None, outFile=None, customConfig=None):
    cftasks = cloudformationtasks.cloudformationtasks()
    cftasks.generateTemplateS3(stack=stack, region=region, githash=githash, environment=environment, logoutput=logoutput, outFile=outFile, customConfig=customConfig)


@task
def getStackExports(ctx, stack, region, githash=None, environment=None, logoutput=None):
    cftasks = cloudformationtasks.cloudformationtasks()
    cftasks.getStackExports(
        stack=stack, region=region, githash=githash, environment=environment, logoutput=logoutput)


@task
def getStackResources(ctx, stack, region, githash=None, environment=None, logoutput=None):
    cftasks = cloudformationtasks.cloudformationtasks()
    cftasks.getStackResources(
        stack=stack, region=region, githash=githash, environment=environment, logoutput=logoutput)


@task
def getStackStatus(ctx, stack, region, githash=None, environment=None, logoutput=None):
    cftasks = cloudformationtasks.cloudformationtasks()
    cftasks.getStackStatus(
        stack=stack, region=region, githash=githash, environment=environment, logoutput=logoutput)


@task
def upsertStackS3(ctx, stack, region, s3location, githash=None, environment=None, logoutput=None, customConfig=None):
    cftasks = cloudformationtasks.cloudformationtasks()
    cftasks.upsertS3Stack(
        stack=stack, s3location=s3location, region=region, githash=githash, environment=environment, logoutput=logoutput, customConfig=customConfig)


@task
def upsertStack(ctx, stack, region, githash=None, environment=None, logoutput=None, customConfig=None):
    cftasks = cloudformationtasks.cloudformationtasks()
    cftasks.upsertStack(
        stack=stack, region=region, githash=githash, environment=environment, logoutput=logoutput, customConfig=customConfig, iamcapable=[])


@task
def upsertIamStack(ctx, stack, region, githash=None, environment=None, logoutput=None, customConfig=None):
    cftasks = cloudformationtasks.cloudformationtasks()
    cftasks.upsertStack(
        stack=stack, region=region, githash=githash, environment=environment, logoutput=logoutput, customConfig=customConfig, iamcapable=['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM'])


@task
def deleteStack(ctx, stack, region, githash=None, environment=None, logoutput=None, customConfig=None):
    cftasks = cloudformationtasks.cloudformationtasks()
    cftasks.deleteStack(
        stack=stack, region=region, githash=githash, environment=environment, logoutput=logoutput, customConfig=customConfig)


@task
def upsertStackSets(ctx, stack, region, githash=None, environment=None, logoutput=None):
    cftasks = cloudformationtasks.cloudformationtasks()
    cftasks.upsertStackSet(
        stack=stack, region=region, githash=githash, environment=environment, logoutput=logoutput)


@task
def upsertIamStackSet(ctx, stack, region, githash=None, environment=None, logoutput=None):
    cftasks = cloudformationtasks.cloudformationtasks()
    cftasks.upsertIamStackSet(
        stack=stack, region=region, githash=githash, environment=environment, logoutput=logoutput)


@task
def deleteStackSet(ctx, stack, region, githash=None, environment=None, logoutput=None):
    cftasks = cloudformationtasks.cloudformationtasks()
    cftasks.deleteStackSet(
        stack=stack, region=region, githash=githash, environment=environment, logoutput=logoutput)


@task
def deleteCreateStack(ctx, stack, region, githash=None, environment=None, logoutput=None):
    cftasks = cloudformationtasks.cloudformationtasks()
    cftasks.deleteCreateStack(
        stack=stack, region=region, githash=githash, environment=environment, logoutput=logoutput)


@task
def validateStack(ctx, stack, region, logoutput=None):
    cftasks = cloudformationtasks.cloudformationtasks()
    cftasks.validateStack(
        stack=stack, region=region, logoutput=logoutput)


@task
def createChangeSet(ctx, stack, region, githash=None, environment=None):
    cftasks = cloudformationtasks.cloudformationtasks()
    pprint.pprint(cftasks.createChangeSet(
        stack=stack, region=region, githash=githash, environment=environment))


@task
def getRRset(ctx, zonename, region='ap-southeast-2'):
    session = getBaseSession(region)
    dnsclient = route53tasks.route53tasks()
    dnsclient.getRRset(
        session=session, zonename=zonename)


@task
def createDNSDelegationSet(ctx, region='ap-southeast-2', logoutput=None):
    session = getBaseSession(region)
    dnsclient = route53tasks.route53tasks()
    dnsclient.createDNSDelegationSet(
        session=session, region=region, logoutput=logoutput)


@task
def createDNSzone(ctx, folder='dns', zonename=None, region='ap-southeast-2', logoutput=None):
    session = getBaseSession(region)
    dnsclient = route53tasks.route53tasks()
    dnsclient.createDNSzone(
        session=session, folder=folder, zonename=zonename, logoutput=logoutput)


@task
def createDNSzoneFile(ctx, region='ap-southeast-2', zonename=None, logoutput=None):
    session = getBaseSession(region)
    dnsclient = route53tasks.route53tasks()
    dnsclient.createDNSzoneFile(
        session=session, zonename=zonename, logoutput=logoutput)


@task
def upsertJSONzoneFile(ctx, zonename, comment, region='ap-southeast-2', noop=True, logoutput=None, delete=False):
    session = getBaseSession(region)
    dnsclient = route53tasks.route53tasks()
    dnsclient.upsertJSONzoneFile(
        zonename=zonename, comment=comment, session=session, noop=noop, logoutput=logoutput, delete=delete)


@task
def readBINDzoneFile(ctx, zonename, region='dns', logoutput=None):
    dnsclient = route53tasks.route53tasks()
    dnsclient.readBINDzoneFile(
        zonename=zonename, region=region, logoutput=logoutput)


@task
def upsertBINDzoneFile(ctx, zonename=None, folder='dns', region='ap-southeast-2', logoutput=None):
    session = getBaseSession(region)
    dnsclient = route53tasks.route53tasks()
    dnsclient.upsertBINDzoneFile(
        session=session, zonename=zonename, folder=folder, logoutput=logoutput)


@task
def validateNameServers(ctx, zonename, region='ap-southeast-2'):
    session = getBaseSession(region)
    dnsclient = route53tasks.route53tasks()
    dnsclient.validateNameServers(
        zone=zonename, session=session)


@task
def validateJSONZoneFiles(ctx, path="ci", schema="route53.schema.json", zone=None, logoutput=None):
    dnsclient = route53tasks.route53tasks()
    dnsclient.validateJSONZoneFiles(
        path=path, schema=schema, zone=None, logoutput=logoutput)


@task
def cnameSwap(ctx, name, value1, value2, zonename, comment, ttl=300, region='ap-southeast-2'):
    session = getBaseSession(region)
    dnsclient = route53tasks.route53tasks()
    dnsclient.cnameSwap(
        name=name, value1=value1, value2=value2, zonename=zonename, session=session, comment=comment, ttl=ttl)


# Beanstalk Tasks

@task
def createBeanstalkApplication(ctx, stack, region, logoutput=None):
    session, config = configtasks.getConfig(region, stack)
    bsclient = beanstalktasks.beanstalktasks()
    bsclient.createApplication(
        session=session, config=config, logoutput=logoutput)


def createBeanstalkApplicationVersion(ctx, stack, region, logoutput=None):
    session, config = configtasks.getConfig(region, stack)
    bsclient = beanstalktasks.beanstalktasks()
    bsclient.createApplicationVersion(
        session=session, config=config, logoutput=logoutput)

# RDS Tasks


@task
def createDatabaseSnapshot(ctx, stack, region, githash=None, environment=None):
    session, config = configtasks.getConfig(region, stack, githash, environment)
    cftasks = cloudformationtasks.cloudformationtasks()
    rds = database.rds(session)
    cfstackname = cftasks.generateStackName(config["stackname"], githash, environment)
    resources = cftasks.getStackResources(stackname=cfstackname)
    rds.SnapshotfromResources(stackresources=resources)


@task
def restoreDatabaseClusterFromSnapshot(ctx, region, cluster, snapshot, engine):
    session = getBaseSession(region)
    rds = database.rds(session)
    rds.restoreClusterFromSnapshot(
        cluster=cluster, snapshot=snapshot, engine=engine)


@task
def listDatabases(ctx, region):
    session = getBaseSession(region)
    rds = database.rds(session)
    pprint.pprint(rds.listDatabases())


@task
def listTagsForDatabase(ctx, region, arn):
    session = getBaseSession(region)
    rds = database.rds(session)
    pprint.pprint(rds.listTags(arn))


@task
def addTagToDatabase(ctx, region, arn, key, value):
    session = getBaseSession(region)
    rds = database.rds(session)
    rds.addTag(arn, key, value)


def getConfig(region, stack, githash=None, environment=None):
    conf = configs.loadConfig(stack, region, githash, environment)
    kmsclient = kmstasks.kmstasks()
    authentication = auth.authenticate(conf["region"])
    session = authentication.getSession()
    if 'secrets' in conf:
        conf['secrets'] = kmsclient.decrypt_secrets(session, **conf['secrets'])
        for k, v in conf['secrets'].iteritems():
            param = {'NoEcho': True, 'Description': k, 'Type': 'String', 'Default': v}
            conf['parameters'][k] = param
    # print json.dumps(conf, sort_keys=True, indent=4, separators=(',', ': '))
    return session, conf


def getZoneFile(region, stack):
    conf = zonefile.loadZoneFile(stack, region)
    authentication = auth.authenticate("ap-southeast-2")
    session = authentication.getSession()
    return session, conf


def getBaseSession(region='ap-southeast-2'):
    authentication = auth.authenticate(region)
    session = authentication.getSession()
    return session


# Secret Tasks


@task
def encrypt(ctx, string, region, key_alias):
    session = getBaseSession(region)
    kmsclient = kmstasks.kmstasks()
    kmsclient.encrypt(string=string, session=session, key_alias=key_alias)

# API Tasks


@task
def createAPIDomain(ctx, domain, certname, region):
    session = getBaseSession(region)
    api = apitasks.apitasks()
    api.createAPIDomain(domain=domain, certarn=certname, session=session)


def deleteAPIDomain(ctx, domain, region="ap-southeast-2"):
    session = getBaseSession(region)
    api = apitasks.apitasks()
    api.deleteAPIDomain(domain=domain, session=session)


@task
def createAPIBasePathMapping(ctx, domain, basePath, restApiId, stage, region):
    session = getBaseSession(region)
    api = apitasks.apitasks()
    api.createAPIBasePathMapping(domain=domain, basePath=basePath, restApiId=restApiId, stage=stage, session=session)


@task
def deleteAPIBasePathMapping(ctx, domain, basePath, region):
    session = getBaseSession(region)
    api = apitasks.apitasks()
    api.deleteAPIBasePathMapping(domain=domain, basePath=basePath, session=session)


@task
def queryDomain(self, domain):
    api = apitasks.apitasks()
    records = api.queryDomain(domain=domain)
    pprint.pprint(records)


@task
def findBlueGreenStack(self, domain, cloudfrontBlue, cloudfrontGreen):
    api = apitasks.apitasks()
    inactiveStack = api.findBlueGreenStack(domain=domain, cloudfrontBlue=cloudfrontBlue, cloudfrontGreen=cloudfrontGreen)
    pprint.pprint(inactiveStack)


# ACM Tasks


@task
def requestCert(ctx, domain, certname, region):
    session = getBaseSession(region)
    api = apitasks.apitasks()
    api.createAPIDomain(domain=domain, certarn=certname, session=session)

# ECS tasks


@task
def deployEnvironment(ctx, version, environment):
    ecs.template_configs(VERSION=version, ENVIRONMENT=environment)
    authentication = auth.authenticate('ap-southeast-2')
    session = authentication.getSession()
    conf = ecs.loadServiceConfigs()
    task = ecs.task(session)
    contDef = task.createContDef()
    taskArn = task.registerTaskDef(contDef, version)
    print conf.deploy
    cftemplate = json.loads(ecs.template_service_cf(taskArn, **conf.deploy))
    cf = cloudformation.stack(session)
    cfstackname = conf.deploy['service']['serviceName']
    status = cf.describeStack(stackname=cfstackname)
    try:
        cf.validateTemplate(cftemplate=cftemplate)
    except ClientError as err:
        logging.warn(err)
        # print "Template validation failed!"
        # pprint.pprint(json.dumps(cftemplate))
        sys.exit(1)
    if status:
        try:
            cf.updateStack(cftemplate, stackname=cfstackname)
            state, status = cf.statusPoller(stackname=cfstackname)

            if state != 0:
                sys.exit(1)
            else:
                pprint.pprint(cf.getStackResources(stackname=cfstackname))
        except ClientError as err:
            logging.warn(err)
            if 'No updates are to be performed' in str(err):
                sys.exit(0)
            sys.exit(1)
    else:
        try:
            cf.createStack(cftemplate, stackname=cfstackname)
            state, status = cf.statusPoller(stackname=cfstackname)

            if state != 0:
                sys.exit(1)
            else:
                pprint.pprint(cf.getStackResources(stackname=cfstackname))
        except ClientError as err:
            logging.warn(err)
            if 'already exists' in str(err):
                sys.exit(0)
            sys.exit(1)

# Lambda Tasks


@task
def invokeLambdaFunction(ctx, function, payload, region):
    session = getBaseSession(region)
    lambdaTasks = lambdatasks.lambdatasks()
    lambdaTasks.invokeLambda(function, payload, session)


@task
def upsertLambdaAlias(ctx, stack, region, githash=None, environment=None, customConfig=None):
    """Idempotent"""
    session, config = configtasks.getConfig(region, stack, githash, environment, customConfig)

    for lambda_name in config['resources']['lambda']:
        func_config = config['resources']['lambda'][lambda_name]
        lambdatasks.upsert_alias(
            session,
            function_name=func_config['functionName'],
            alias_name=func_config['alias'],
            alias_desc=func_config['aliasDescription'],
        )

# GreenGrass Tasks


@task
def upsertGGDeployment(ctx, stack, region, githash=None, environment=None, customConfig=None):
    session, config = configtasks.getConfig(region, stack, githash, environment, customConfig)
    return create_group_with_config(session, config)


# S3 Tasks


@task
def checkS3ForFile(ctx, bucket, key, region):
    session = getBaseSession(region)
    s3 = s3tasks.S3tasks()
    s3.checkForFile(bucket=bucket, key=key)


@task
def uploadFileS3(ctx, filename, bucket, key, region):
    session = getBaseSession(region)
    s3 = s3tasks.S3tasks()
    s3.uploadFile(session=session, filename=filename, bucket=bucket, key=key)


# EC2/VPC Tasks

@task
def getVPCs(ctx, vpcid=[], region='ap-southeast-2', noop=False, logoutput=None):
    session = getBaseSession(region)
    ec2client = ec2tasks.ec2tasks()
    ec2client.getVPCs(session=session, vpcids=vpcid, noop=noop, logoutput=logoutput)


@task
def getRoutetables(ctx, routetableid=[], region='ap-southeast-2', noop=False, logoutput=None):
    session = getBaseSession(region)
    ec2client = ec2tasks.ec2tasks()
    ec2client.getRoutetables(session=session, routetableids=routetableid, noop=noop, logoutput=logoutput)


@task
def getSubnets(ctx, subnetid=None, region='ap-southeast-2', noop=False, logoutput=None):
    session = getBaseSession(region)
    ec2client = ec2tasks.ec2tasks()
    ec2client.getSubnets(session=session, subnetids=subnetid, noop=noop, logoutput=logoutput)


@task
def getVPNConnections(ctx, vpnids=None, region='ap-southeast-2', noop=False, logoutput=None):
    session = getBaseSession(region)
    ec2client = ec2tasks.ec2tasks()
    ec2client.getVPNConnections(session=session, vpnids=vpnids, noop=noop, logoutput=logoutput)


@task
def getVPNGateways(ctx, vpngwids=None, region='ap-southeast-2', noop=False, logoutput=None):
    session = getBaseSession(region)
    ec2client = ec2tasks.ec2tasks()
    ec2client.getVPNGateways(session=session, vpngwids=vpngwids, noop=noop, logoutput=logoutput)


@task
def createVPNConnections(ctx, stackname, region, noop=False, logoutput=None):
    session, config = configtasks.getConfig(region, stackname)
    ec2client = ec2tasks.ec2tasks()
    ec2client.createVPNConnections(session=session, config=config, noop=noop, logoutput=logoutput)


@task
def createVPCPeering(ctx, stackname, region, noop=False, logoutput=None):
    session, config = configtasks.getConfig(region, stackname)
    ec2client = ec2tasks.ec2tasks()
    ec2client.createVPCPeering(session=session, config=config, noop=noop, logoutput=logoutput)


@task
def getVPCPeering(ctx, vpcpeerid=None, region='ap-southeast-2', noop=False):
    session = getBaseSession(region)
    ec2client = ec2tasks.ec2tasks()
    ec2client.getVPCPeering(session=session, vpcpeerid=vpcpeerid, noop=noop)


@task
def acceptVPCPeering(ctx, vpcpeerid=None, region='ap-southeast-2', noop=False, logoutput=None):
    session = getBaseSession(region)
    ec2client = ec2tasks.ec2tasks()
    ec2client.acceptVPCPeering(session=session, vpcpeerid=vpcpeerid, noop=noop, logoutput=logoutput)


@task
def verifyVPCPeering(ctx, vpcpeerid=None, region='ap-southeast-2', noop=False, logoutput=None):
    session = getBaseSession(region)
    ec2client = ec2tasks.ec2tasks()
    ec2client.verifyVPCPeering(session=session, vpcpeerid=vpcpeerid, noop=noop, logoutput=logoutput)


@task
def get_organization_chart(ctx, region='ap-southeast-2', depth=None, logoutput=None):
    session = getBaseSession(region)
    org_client = organizationstasks.organizationstasks()
    org_client.organization_tree(session=session, depth=depth, logoutput=logoutput)


@task
def upsert_org_account(ctx, stackname, region_folder, noop=True, logoutput=None):
    session, config = configtasks.getConfig(region=region_folder, stack=stackname)
    org_client = organizationstasks.organizationstasks()
    org_client.upsert_org_account(session=session, config=config, noop=noop, logoutput=logoutput)


@task
def upsert_org_unit(ctx, stackname, region_folder, logoutput=None):
    session, config = configtasks.getConfig(region=region_folder, stack=stackname)
    org_client = organizationstasks.organizationstasks()
    org_client.upsert_org_unit(session=session, config=config, logoutput=logoutput)


@task(name="lambda-init-bg")
def lambda_init_bg(context, stack_name, region):
    """
    Creates a version of latest for lambda
    Creates blue and green alias for lambda
    :param context:
    :param stack_name: stack name containing lambdas
    :return:
    """

    serverless_tasks = ServerlessTasks(region=region)
    serverless_tasks.lambda_init_bg(stack_name)


@task(name="gateway-init-bg")
def gateway_init_bg(context, stack_name, region):
    """
    If API Stack has DomainName this will create blue green stages.
    Creates a version of latest for lambda
    Creates blue and green alias for lambda
    :param context:
    :param stack_name: stack name containing api gateway domain name
    :return:
    """

    serverless_tasks = ServerlessTasks(region=region)
    # Add Blue Stage and Green Stage
    serverless_tasks.gateway_init_bg(stack_name)
    # Add Links from Blue stage and Green stage to Gateway Domain's base paths (if found)
    serverless_tasks.gateway_init_public(stack_name)


@task(name="lambda-deploy-code")
def lambda_deploy_code(context, stack_name, code_key, region):
    """
    Given a stack of lambdas. this will update the code on all lambdas.
    Only supports single package and different handler
    :param context:
    :param stack_name: stack name containing lambdas
    :param code_key: s3 bucket's key which is the lambda zip/jar
    :param region: ap-southeast-2
    :return:
    """

    serverless_tasks = ServerlessTasks(region=region)
    serverless_tasks.lambda_deploy_code(stack_name, code_key)


@task(name="lambda-bg-deploy-code")
def lambda_bg_deploy_code(context, gateway_stack_name, lambda_stack_name, code_key, region):
    """
    # Release branch deploy code to lambda
    Code is deployed to non-live stage linked lambda
    :param context:
    :param lambda_stack_name:
    :param gateway_stack_name:
    :param region:
    :return:
    """

    serverless_tasks = ServerlessTasks(region=region)
    serverless_tasks.serverless_lambda_deploy(gateway_stack_name, lambda_stack_name, code_key)


@task(name="serverless-blue-green-switch")
def serverless_blue_green_switch(context, stack_name, region):
    """
    # Release branch deploy
    :param context:
    :param lambda_stack_name:
    :param gateway_stack_name:
    :param region:
    :return:
    """

    serverless_tasks = ServerlessTasks(region=region)
    serverless_tasks.serverless_blue_green_switch(gateway_stack_name=stack_name)


@task(name="gateway-update-code")
def gateway_update_code(context, stack_name, region, live=False):
    """
    # This should happen post stack update.
    :param context:
    :param lambda_stack_name:
    :param gateway_stack_name:
    :param region:
    :param live:
    :return:
    """

    serverless_tasks = ServerlessTasks(region=region)
    serverless_tasks.publish_stage_changes(gateway_stack_name=stack_name, live=live)
