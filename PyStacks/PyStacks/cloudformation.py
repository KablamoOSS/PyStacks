import json
import os
import logging
import time
import sys
import auth
import string
import random

from time import sleep

from botocore.exceptions import ClientError


class stack:

    def __init__(self, session):
        self.cfClient = session.client('cloudformation')
        self.cfStack = session.resource('cloudformation')

    def loadTemplate(self, file):
        currentdir = os.path.dirname(__file__)
        fileloc = os.path.join(
            currentdir, '../configs/cf_templates/{file}'.format(file=file))
        with open(fileloc) as data_file:
            template = json.load(data_file)
        return template

    def createStack(self, cftemplate, stackname,
                    timeout=180,
                    onfailure='ROLLBACK',
                    iamcapable=None):
        if iamcapable:
            if cftemplate and not isinstance(cftemplate, dict) and cftemplate.startswith('https://s3'):
                response = self.cfClient.create_stack(
                    StackName=stackname,
                    TemplateURL=cftemplate,
                    TimeoutInMinutes=timeout,
                    OnFailure=onfailure,
                    Capabilities=iamcapable
                )
            else:
                response = self.cfClient.create_stack(
                    StackName=stackname,
                    TemplateBody=json.dumps(cftemplate),
                    TimeoutInMinutes=timeout,
                    OnFailure=onfailure,
                    Capabilities=iamcapable
                )
        else:
            if cftemplate and not isinstance(cftemplate, dict) and cftemplate.startswith('https://s3'):
                response = self.cfClient.create_stack(
                    StackName=stackname,
                    TemplateURL=cftemplate,
                    TimeoutInMinutes=timeout,
                    OnFailure=onfailure
                )
            else:
                response = self.cfClient.create_stack(
                    StackName=stackname,
                    TemplateBody=json.dumps(cftemplate),
                    TimeoutInMinutes=timeout,
                    OnFailure=onfailure
                )

        return response

    def deleteStack(self, stackname):
        self.cfClient.delete_stack(
            StackName=stackname
        )

    def createStackSet(self, cftemplate, stackname, iamcapable=None):
        if iamcapable:
            if cftemplate and not isinstance(cftemplate, dict) and cftemplate.startswith('https://s3'):
                response = self.cfClient.create_stack_set(
                    StackSetName=stackname,
                    TemplateURL=cftemplate,
                    Capabilities=iamcapable
                )
            else:
                response = self.cfClient.create_stack_set(
                    StackSetName=stackname,
                    TemplateBody=json.dumps(cftemplate),
                    Capabilities=iamcapable
                )
        else:
            if cftemplate and not isinstance(cftemplate, dict) and cftemplate.startswith('https://s3'):
                response = self.cfClient.create_stack_set(
                    StackSetName=stackname,
                    TemplateURL=cftemplate
                )
            else:
                response = self.cfClient.create_stack_set(
                    StackSetName=stackname,
                    TemplateBody=json.dumps(cftemplate)
                )

        return response

    def updateStackSet(self, cftemplate, stackname, iamcapable=None):
        if iamcapable:
            if cftemplate and not isinstance(cftemplate, dict) and cftemplate.startswith('https://s3'):
                response = self.cfClient.update_stack(
                    StackSetName=stackname,
                    TemplateURL=cftemplate,
                    Capabilities=iamcapable
                )
            else:
                response = self.cfClient.update_stack(
                    StackSetName=stackname,
                    TemplateBody=json.dumps(cftemplate),
                    Capabilities=iamcapable
                )
        else:
            if cftemplate and not isinstance(cftemplate, dict) and cftemplate.startswith('https://s3'):
                response = self.cfClient.update_stack(
                    StackSetName=stackname,
                    TemplateURL=cftemplate,
                )
            else:
                response = self.cfClient.update_stack(
                    StackSetName=stackname,
                    TemplateBody=json.dumps(cftemplate),
                )

    def deleteStackSet(self, stackname):
        self.cfClient.delete_stack_set(
            StackSetName=stackname
        )

    def createChangeSet(self, cftemplate, stackname, skipsleep=False, timeoutseconds=60):
        if self.describeStack(stackname) is None:
            return []
        changeSetName = stackname + str(int(time.time()))
        if cftemplate and not isinstance(cftemplate, dict) and cftemplate.startswith('https://s3'):
            self.cfClient.create_change_set(
                StackName=stackname,
                TemplateURL=cftemplate,
                ChangeSetType='UPDATE',
                ChangeSetName=changeSetName
            )
        else:
            self.cfClient.create_change_set(
                StackName=stackname,
                TemplateBody=json.dumps(cftemplate),
                ChangeSetType='UPDATE',
                ChangeSetName=changeSetName
            )

        counter = 0
        while True:
            counter = counter + 1
            if counter > timeoutseconds / 5:
                print("Timeout")
                sys.exit(1)
            if not skipsleep:
                sleep(5)
            response = self.cfClient.describe_change_set(
                ChangeSetName=changeSetName,
                StackName=stackname
            )
            if response['Status'] == 'FAILED':
                return []
            if response['ExecutionStatus'] != 'UNAVAILABLE':
                break

        return response['Changes']

    def updateStack(self, cftemplate, stackname,
                    iamcapable=None):
        if iamcapable:
            if cftemplate and not isinstance(cftemplate, dict) and cftemplate.startswith('https://s3'):
                response = self.cfClient.update_stack(
                    StackName=stackname,
                    TemplateURL=cftemplate,
                    Capabilities=iamcapable
                )
            else:
                response = self.cfClient.update_stack(
                    StackName=stackname,
                    TemplateBody=json.dumps(cftemplate),
                    Capabilities=iamcapable
                )
        else:
            if cftemplate and not isinstance(cftemplate, dict) and cftemplate.startswith('https://s3'):
                response = self.cfClient.update_stack(
                    StackName=stackname,
                    TemplateURL=cftemplate,
                )
            else:
                response = self.cfClient.update_stack(
                    StackName=stackname,
                    TemplateBody=json.dumps(cftemplate),
                )

    def validateTemplate(self, cftemplate):
        validationStatus = self.cfClient.validate_template(
            TemplateBody=json.dumps(cftemplate)
        )
        return validationStatus

    def describeStackSet(self, stackname):
        try:
            response = self.cfClient.describe_stack_set(
                StackSetName=stackname
            )
        except ClientError as err:
            if 'does not exist' in str(err):
                return None
            else:
                raise err
        return response['StackSet']['Status']

    def describeStack(self, stackname):
        try:
            status = self.cfClient.describe_stacks(
                StackName=stackname
            )
        except ClientError as err:
            if 'does not exist' in str(err):
                return None
            else:
                raise err
        return status['Stacks'][0]['StackStatus']

    def describeExports(self, stackname):
        stack = self.cfStack.Stack(stackname)
        stack.load()
        exports = stack.outputs
        return exports

    def getStackStatus(self, stackname):
        try:
            status = self.cfClient.describe_stacks(
                StackName=stackname
            )
        except Exception as err:
            if 'security token included in the request is expired' in str(err):
                print("Expired token, refreshing...")
                authentication = auth.authenticate('ap-southeast-2')
                session = authentication.getSession()
                self.cfClient = session.client('cloudformation')
                self.cfStack = session.resource('cloudformation')
                print("Reattempting with refreshed token")
                return self.getStackStatus(stackname)
            raise err
        return status['Stacks'][0]['StackStatus']

    def getStackResources(self, stackname):
        response = self.cfClient.describe_stack_resources(
            StackName=stackname
        )
        return response['StackResources']

    def stackStatusChecker(self, stackname):
        status = self.getStackStatus(stackname)
        stati = {
            'CREATE_COMPLETE': 0,
            'CREATE_IN_PROGRESS': 2,
            'CREATE_FAILED': 1,
            'DELETE_FAILED': 1,
            'DELETE_IN_PROGRESS': 2,
            'REVIEW_IN_PROGRESS': 2,
            'ROLLBACK_COMPLETE': 1,
            'ROLLBACK_FAILED': 1,
            'ROLLBACK_IN_PROGRESS': 2,
            'UPDATE_COMPLETE': 0,
            'UPDATE_COMPLETE_CLEANUP_IN_PROGRESS': 2,
            'UPDATE_IN_PROGRESS': 2,
            'UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS': 2,
            'UPDATE_ROLLBACK_FAILED': 1,
            'UPDATE_ROLLBACK_IN_PROGRESS': 2,
        }
        return stati.get(status, "INVALID CF STATUS"), status

    def statusPoller(self, stackname, sleeptime=5, output=True):
        state = 2
        count = 0
        while state == 2 and count < 720:
            count += 1

            try:
                state, status = self.stackStatusChecker(stackname)
            except Exception as err:
                logging.warn(err)
                if 'does not exist' in str(err):
                    output = False
                    state = 0
                    return state, 'DELETE_COMPLETE'
                else:
                    raise err

            if output:
                print status
                sys.stdout.flush()
            sleep(sleeptime)

        return state, status

    def list_stack_resources(self, stackname):
        resources = []
        response = self.cfStack.list_stack_resources(
            StackName=stackname
        )
        resources.extend(response["StackResourceSummaries"])
        while 'NextToken' in response:
            response = self.cfStack.list_stack_resources(
                StackName=stackname,
                NextToken=response["NextToken"]
            )
            resources.extend(response["StackResourceSummaries"])

        return resources
