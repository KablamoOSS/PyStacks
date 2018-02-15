import auth
import sys
import json
import cloudformation
import configtasks
import pprint
import configs
import template
import output
from botocore.exceptions import ClientError
from cloudformation_helpers import init_cf_action, final_cf_action, handle_cf_error
import autoscaling
import ec2

from logger import get_pystacks_log
log = get_pystacks_log()


class cloudformationtasks:

    def __init__(self):
        pass

    def generateTemplate(ctx, stack, region, githash=None, environment=None, logoutput=None, outFile=None, customConfig=''):
        '''Generates a template given stack name and region USAGE generateTemplate STACK REGION'''
        config = configs.loadConfig(stack, region, githash, environment, customConfig)
        cftemplate = template.voltron(stack, **config)
        if len(json.dumps(cftemplate)) >= 51200:
            print output.whalesay(text='Your generated Cloudformation Template is over the max allowable size.\nYou will need to reduce the size, split the template or upload into S3.')
        if len(json.dumps(cftemplate)) >= 460800:
            print output.piesay(text='Your generated Cloudformation Template is over the max allowable size.')
            sys.exit(1)
        name = outFile if outFile else stack
        template.writecompiled(cftemplate, name, region)

    def generateTemplateS3(ctx, stack, region, githash=None, environment=None, logoutput=None, outFile=None, customConfig=None):
        '''Generates a template that needs to be uploaded to S3. Must run on
        the build agents as it will decrypt the secrets using KMS. Otherwise usage
        is the same as generateTemplate'''
        session, config = configtasks.getConfig(region, stack, githash, environment, customConfig)
        cftemplate = template.voltron(stack, **config)
        if len(json.dumps(cftemplate)) >= 51200:
            print output.whalesay(text='Your generated Cloudformation Template is over the max allowable size.\nYou will need to reduce the size, split the template or upload into S3.')
        if len(json.dumps(cftemplate)) >= 460800:
            print output.piesay(text='Your generated Cloudformation Template is over the max allowable size.')
            sys.exit(1)
        name = outFile if outFile else stack
        template.writecompiled(cftemplate, name, region)

    def getStackExports(self, stack, region, githash=None, environment=None, logoutput=None):
        session, config = configtasks.getConfig(region, stack, githash, environment)
        cf = cloudformation.stack(session)
        cfstackname = self.generateStackName(config["stackname"], githash, environment)
        exports = cf.describeExports(stackname=cfstackname)
        print "EXPORTS"
        print json.dumps(exports, sort_keys=True, indent=4, separators=(',', ': '))

    def getStackResources(self, stack, region='ap-southeast-2', githash=None, environment=None, logoutput=None):
        session = self.getBaseSession(region)
        cf = cloudformation.stack(session)
        cfstackname = self.generateStackName(stack, githash, environment)
        resources = cf.getStackResources(stackname=cfstackname)
        return resources

    def getStackStatus(self, stack, region, githash=None, environment=None, logoutput=None):
        session, config = configtasks.getConfig(region, stack, githash, environment)
        cf = cloudformation.stack(session)
        cfstackname = self.generateStackName(config["stackname"], githash, environment)
        status = cf.getStackStatus(stackname=cfstackname)
        print "STATUS"
        print json.dumps(status, sort_keys=True, indent=4, separators=(',', ': '))

    def upsertS3Stack(self, stack, s3location, region, githash=None, environment=None, logoutput=None, customConfig=None):
        self.optOut(stack)
        session, config = configtasks.getConfig(region, stack, githash, environment, customConfig)
        cftemplate = template.voltron(stack, **config)
        cfstackname = self.generateStackName(config["stackname"], githash, environment)
        template.writecompiled(data=cftemplate, name=stack, region=region, logoutput=logoutput)
        cf = cloudformation.stack(session)
        status = cf.describeStack(stackname=cfstackname)
        if status:
            try:
                response = cf.updateStack(cftemplate=s3location, stackname=cfstackname)
                if logoutput:
                    print json.dumps(response, sort_keys=True, indent=4, separators=(',', ': '))
                state, status = cf.statusPoller(stackname=cfstackname)

                if logoutput:
                    print json.dumps(cf.getStackResources(stackname=cfstackname), default=str, sort_keys=True, indent=4, separators=(',', ': '))

                if state != 0:
                    sys.exit(1)
            except ClientError as err:
                log.warn(err)
                if 'No updates are to be performed' in str(err):
                    sys.exit(0)
                sys.exit(1)
        else:
            try:
                response = cf.createStack(cftemplate=s3location, stackname=cfstackname)
                if logoutput:
                    print json.dumps(response, sort_keys=True, indent=4, separators=(',', ': '))
                state, status = cf.statusPoller(stackname=cfstackname)

                if logoutput:
                    print json.dumps(cf.getStackResources(stackname=cfstackname), default=str, sort_keys=True, indent=4, separators=(',', ': '))

                if state != 0:
                    sys.exit(1)
            except ClientError as err:
                log.warn(err)
                if 'already exists' in str(err):
                    sys.exit(0)
                sys.exit(1)

    def upsertStack(self, stack, region, githash=None, environment=None, logoutput=None, customConfig=None, iamcapable=[]):
        self.optOut(stack)
        session, config = configtasks.getConfig(region, stack, githash, environment, customConfig)
        cftemplate = template.voltron(stack, **config)
        cfstackname = self.generateStackName(config["stackname"], githash, environment)
        template.writecompiled(data=cftemplate, name=stack, region=region, logoutput=logoutput)
        cf = cloudformation.stack(session)
        try:
            cf.validateTemplate(cftemplate=cftemplate)
        except ClientError as err:
            log.warn(err)
            sys.exit(1)
        status = cf.describeStack(stackname=cfstackname)
        if status:
            try:
                response = cf.updateStack(cftemplate, stackname=cfstackname, iamcapable=iamcapable)
                if logoutput:
                    print json.dumps(response, sort_keys=True, indent=4, separators=(',', ': '))
                state, status = cf.statusPoller(stackname=cfstackname)

                if logoutput:
                    print json.dumps(cf.getStackResources(stackname=cfstackname), default=str, sort_keys=True, indent=4, separators=(',', ': '))

                if state != 0:
                    sys.exit(1)
            except ClientError as err:
                log.warn(err)
                if 'No updates are to be performed' in str(err):
                    return 'No updates are to be performed'
                raise ClientError(err)
        else:
            try:
                response = cf.createStack(cftemplate, stackname=cfstackname, iamcapable=iamcapable)
                if logoutput:
                    print json.dumps(response, sort_keys=True, indent=4, separators=(',', ': '))
                state, status = cf.statusPoller(stackname=cfstackname)

                if logoutput:
                    print json.dumps(cf.getStackResources(stackname=cfstackname), default=str, sort_keys=True, indent=4, separators=(',', ': '))

                if state != 0:
                    sys.exit(1)
            except ClientError as err:
                log.warn(err)
                if 'already exists' in str(err):
                    return 'No updates are to be performed'
                raise ClientError(err)

    def deleteStack(self, stack, region, githash=None, environment=None, logoutput=None, customConfig=None):
        '''Deletes a stack given a name and region USAGE deleteStack STACK REGION'''
        self.optOut(stack)
        session, config = configtasks.getConfig(region, stack, githash, environment, customConfig)
        cfstackname = self.generateStackName(config["stackname"], githash, environment)
        cf = cloudformation.stack(session)
        try:
            cf.deleteStack(stackname=cfstackname)
            state, status = cf.statusPoller(stackname=cfstackname)

            if state != 0:
                sys.exit(1)
        except ClientError as err:
            print err
            sys.exit(1)

    def upsertStackSet(self, stack, region, githash=None, environment=None, logoutput=None):
        self.optOut(stack)
        session, config = configtasks.getConfig(region, stack, githash, environment)
        cftemplate = template.voltron(stack, **config)
        cfstackname = self.generateStackName(config["stackname"], githash, environment)
        template.writecompiled(data=cftemplate, name=stack, region=region, logoutput=logoutput)
        cf = cloudformation.stack(session)
        try:
            cf.validateTemplate(cftemplate=cftemplate)
        except ClientError as err:
            log.warn(err)
            # print "Template validation failed!"
            # pprint.pprint(json.dumps(cftemplate))
            sys.exit(1)
        status = cf.describeStackSet(stackname=cfstackname)
        if status:
            try:
                response = cf.updateStackSet(cftemplate=cftemplate, stackname=cfstackname)
                if logoutput:
                    print json.dumps(response, sort_keys=True, indent=4, separators=(',', ': '))
                state, status = cf.statusPoller(stackname=cfstackname)

                if logoutput:
                    print json.dumps(cf.getStackResources(stackname=cfstackname), default=str, sort_keys=True, indent=4, separators=(',', ': '))

                if state != 0:
                    sys.exit(1)
            except ClientError as err:
                log.warn(err)
                if 'No updates are to be performed' in str(err):
                    sys.exit(0)
                sys.exit(1)
        else:
            try:
                response = cf.createStackSet(cftemplate=cftemplate, stackname=cfstackname)
                if logoutput:
                    print json.dumps(response, sort_keys=True, indent=4, separators=(',', ': '))
                state, status = cf.statusPoller(stackname=cfstackname)

                if logoutput:
                    print json.dumps(cf.getStackResources(stackname=cfstackname), default=str, sort_keys=True, indent=4, separators=(',', ': '))

                if state != 0:
                    sys.exit(1)
            except ClientError as err:
                log.warn(err)
                if 'already exists' in str(err):
                    sys.exit(0)
                sys.exit(1)

    def upsertIamStackSet(self, stack, region, githash=None, environment=None, logoutput=None):
        self.optOut(stack)
        session, config = configtasks.getConfig(region, stack, githash, environment)
        cftemplate = template.voltron(stack, **config)
        cfstackname = self.generateStackName(config["stackname"], githash, environment)
        template.writecompiled(data=cftemplate, name=stack, region=region, logoutput=logoutput)
        cf = cloudformation.stack(session)
        try:
            cf.validateTemplate(cftemplate=cftemplate)
        except ClientError as err:
            log.warn(err)
            # print "Template validation failed!"
            # pprint.pprint(json.dumps(cftemplate))
            sys.exit(1)
        status = cf.describeStackSet(stackname=cfstackname)
        if status:
            try:
                response = cf.updateStackSet(cftemplate=cftemplate, stackname=cfstackname, iamcapable=['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM'])
                if logoutput:
                    print json.dumps(response, sort_keys=True, indent=4, separators=(',', ': '))
                state, status = cf.statusPoller(stackname=cfstackname)

                if logoutput:
                    print json.dumps(cf.getStackResources(stackname=cfstackname), default=str, sort_keys=True, indent=4, separators=(',', ': '))

                if state != 0:
                    sys.exit(1)
            except ClientError as err:
                log.warn(err)
                if 'No updates are to be performed' in str(err):
                    sys.exit(0)
                sys.exit(1)
        else:
            try:
                response = cf.createStackSet(cftemplate=cftemplate, stackname=cfstackname, iamcapable=['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM'])
                if logoutput:
                    print json.dumps(response, sort_keys=True, indent=4, separators=(',', ': '))
                state, status = cf.statusPoller(stackname=cfstackname)

                if logoutput:
                    print json.dumps(cf.getStackResources(stackname=cfstackname), default=str, sort_keys=True, indent=4, separators=(',', ': '))

                if state != 0:
                    sys.exit(1)
            except ClientError as err:
                log.warn(err)
                if 'already exists' in str(err):
                    sys.exit(0)
                sys.exit(1)

    def deleteStackSet(self, stack, region, githash=None, environment=None, logoutput=None):
        '''Deletes a stack given a name and region USAGE deleteStack STACK REGION'''
        self.optOut(stack)
        session, config = configtasks.getConfig(region, stack, githash, environment)
        cfstackname = self.generateStackName(config["stackname"], githash, environment)
        cf = cloudformation.stack(session)
        try:
            cf.deleteStackSet(stackname=cfstackname)
            state, status = cf.statusPoller(stackname=cfstackname)

            if state != 0:
                sys.exit(1)
        except ClientError as err:
            print err
            sys.exit(1)

    def deleteCreateStack(self, stack, region, githash=None, environment=None, logoutput=None):
        '''Deletes a stack then creates it again'''
        self.optOut(stack)
        session, config = configtasks.getConfig(region, stack, githash, environment)
        cftemplate = template.voltron(stack, **config)
        template.writecompiled(cftemplate, stack, region)
        cf = cloudformation.stack(session)

        try:
            cf.validateTemplate(cftemplate)
        except:
            print "Template validation failed!"
            print json.dumps(cftemplate, sort_keys=True, indent=4, separators=(',', ': '))
            sys.exit(1)

        try:
            cf.deleteStack(config["stackname"])
            cf.statusPoller(stackname=config["stackname"])
        except ClientError as err:
            print err
            sys.exit(1)

        try:
            cf.createStack(cftemplate, config["stackname"])
            cf.statusPoller(stackname=config["stackname"])
        except ClientError as err:
            log.warn(err)
            sys.exit(1)

    def validateStack(self, stack, region, logoutput=None):
        session, config = configtasks.getConfig(region, stack)
        cftemplate = template.voltron(stack, **config)
        template.writecompiled(data=cftemplate, name=stack, region=region)
        cf = cloudformation.stack(session)
        validationstatus = cf.validateTemplate(cftemplate)
        return validationstatus

    def createChangeSet(self, stack, region, githash, environment):
        session, config = configtasks.getConfig(region, stack, githash, environment)
        cftemplate = template.voltron(stack, **config)
        template.writecompiled(data=cftemplate, name=stack, region=region)
        cf = cloudformation.stack(session)
        cfstackname = self.generateStackName(stack, githash, environment)
        changes = cf.createChangeSet(cftemplate, cfstackname)
        return changes

    def generateStackName(self, stackname, githash, environment):
        name = stackname
        if environment:
            name += "-" + environment
        if githash:
            name += "-" + githash
        return name

    def optOut(self, stack):
        if stack == 'DONOTHING':
            print 'DONOTHING stack name detected, bailing out cleanly'
            sys.exit(0)

    def getBaseSession(self, region='ap-southeast-2'):
        authentication = auth.authenticate(region)
        session = authentication.getSession()
        return session
