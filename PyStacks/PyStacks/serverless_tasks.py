import auth
from cloudformation import stack
import sys
from pprint import pprint
from botocore.exceptions import ClientError
from datetime import datetime
import random
import string


class ServerlessTasks:
    def __init__(self, region='ap-southeast-2'):
        # TODO Pass in the stage names
        authentication = auth.authenticate(region)
        session = authentication.getSession()
        self.aliases = ["dev", "blue", "green"]  # Don't change this order
        self.live_base_path = "api"
        self.pvt_base_path = "pvt"
        # dev -> $LATEST
        # blue,green versioned code.
        self.api_client = session.client('apigateway')
        self.lambda_client = session.client('lambda')
        self.cloudformation_client = session.client('cloudformation')
        self.session = session

    def get_stack_account(self, stack_name):
        cf_stack = stack(self.session)
        stack_id = cf_stack.get_stack_account(stack_name)
        return stack_id

    def get_stack_lambdas(self, stack_name):
        cf_stack = stack(self.session)
        resources = cf_stack.get_stack_resources(stack_name, 'AWS::Lambda::Function')
        return resources

    def get_stack_restapi(self, stack_name):
        cf_stack = stack(self.session)
        resources = cf_stack.get_stack_resources(stack_name, 'AWS::ApiGateway::RestApi')
        # Todo Support for multiple REST APIs in a single stack
        return resources[0]

    def get_stack_domain_name(self, stack_name):
        """
        Gets the domain name in API Gateway Stack Template
        :param stack_name:
        :return:
        """
        cf_stack = stack(self.session)
        resources = cf_stack.get_stack_resources(stack_name, 'AWS::ApiGateway::DomainName')
        if not resources:
            return False
        return resources[0]

    def lambda_init_bg(self, stack_name):
        lambdas = self.get_stack_lambdas(stack_name)
        self.update_lambda_code(lambdas)

    def lambda_deploy_code(self, stack_name, code_key):
        # Get List of lambdas in stack
        lambda_name_array = self.get_stack_lambdas(stack_name)
        # Update the lambda tag with new s3 key
        for aws_lambda in lambda_name_array:
            # Get lambda arn
            function_arn = self.get_lambda_arn(aws_lambda)
            self.get_lambda_code_bucket_and_key(function_arn)
            self.update_lambda_code_key(function_arn, code_key)
        # Update the code
        self.update_lambda_code(lambda_name_array)

    def get_or_set_lambda_alias(self, function_name):

        for alias in self.aliases:
            try:
                self.lambda_client.get_alias(
                    FunctionName=function_name,
                    Name=alias
                )
            except ClientError:
                self.create_alias(function_name, alias)

    def get_or_set_dev_lambda_alias(self, function_name):
        try:
            self.lambda_client.get_alias(
                FunctionName=function_name,
                Name="dev"
            )
        except ClientError:
            self.create_alias(function_name, 'dev')

    def create_alias(self, function_name, alias):
        print "[INFO] Creating Alias %s for %s" % (alias, function_name)
        response = self.lambda_client.create_alias(
            FunctionName=function_name,
            Name=alias,
            FunctionVersion='$LATEST'
        )
        print response

    def get_lambda_arn(self, lambda_name):
        print "[INFO] Fetching lambda ARN for %s " % lambda_name
        response = self.lambda_client.get_function(
            FunctionName=lambda_name
        )
        return response['Configuration']['FunctionArn']

    def get_lambda_code_bucket_and_key(self, lambda_arn):
        print "[INFO] Fetching lambda code details for %s " % lambda_arn
        lambda_response = self.lambda_client.list_tags(
            Resource=lambda_arn
        )
        if 'code_bucket' not in lambda_response['Tags'] or 'code_key' not in lambda_response['Tags']:
            print "[FAIL] Missing code_bucket and code_key Tags in lambda %s " % lambda_arn
            sys.exit(1)

        return lambda_response['Tags']['code_bucket'], lambda_response['Tags']['code_key']

    def update_lambda_code_key(self, lambda_arn, code_key):
        print "[INFO] Updating lambda code key to %s for %s " % (code_key, lambda_arn)

        self.lambda_client.tag_resource(
            Resource=lambda_arn,
            Tags={
                'code_key': code_key
            }
        )

        return True

    def update_lambda_code(self, lambda_name_array):
        print "[INFO] Updating lambda code for %s " % str(lambda_name_array)

        for aws_lambda in lambda_name_array:
            self.get_or_set_lambda_alias(aws_lambda)
            function_arn = self.get_lambda_arn(aws_lambda)
            code_bucket, code_key = self.get_lambda_code_bucket_and_key(function_arn)

            print "[INFO] Updating lambda code for %s with bucket: %s & key: %s" % (
                aws_lambda, code_bucket, code_key)

            lambda_response = self.lambda_client.update_function_code(
                FunctionName=aws_lambda,
                S3Bucket=code_bucket,
                S3Key=code_key,
                # S3ObjectVersion='string', # TODO Soon!
                Publish=True
            )

            pprint(lambda_response)

    def copy_stage(self, stack_id, rest_api_id, from_stage, to_stage_name):
        """
        Creates a new stage from an existing stage.
        Replace lambda alias mapping to new stage name as lambda alias.
        :param rest_api_id: AWS Physical REST API ID
        :param from_stage: AWS Stage object of a RestAPI resource
        :param to_stage_name: stage name (string)
        :return: bool
        """
        to_stage_variables = {}

        # Add lambda alias as a suffix to stage variables
        for k, v in from_stage["variables"].iteritems():
            to_stage_variables[k] = v.replace(":%s" % from_stage["stageName"], ":%s" % to_stage_name)
            # if lambda function is a variable add permission to invoke
            if (":%s" % from_stage["stageName"]) in v:
                self.add_lambda_permission(function_name=to_stage_variables[k],
                                           region=self.session.region_name,
                                           account_id=stack_id,
                                           rest_api_id=rest_api_id
                                           )
        # Create New Stage
        self.api_client.create_stage(
            restApiId=rest_api_id,
            stageName=to_stage_name,
            deploymentId=from_stage['deploymentId'],
            description=to_stage_name,
            # cacheClusterEnabled=True|False,
            # cacheClusterSize='0.5'|'1.6'|'6.1'|'13.5'|'28.4'|'58.2'|'118'|'237',
            variables=to_stage_variables
            # documentationVersion='string'
        )

        return True

    def enable_metrics(self, rest_api_id, stage_name):
        """
        Enables metrics to stage
        Replace lambda alias mapping to new stage name as lambda alias.
        :param rest_api_id: AWS Physical REST API ID
        :param stage_name: stage name (string)
        :return: bool
        """
        print "[INFO] Enabling INFO Level Logs on stage %s" % stage_name
        self.api_client.update_stage(
            restApiId=rest_api_id,
            stageName=stage_name,
            patchOperations=[
                {
                    'op': 'replace',
                    'path': '/*/*/logging/loglevel',
                    'value': "INFO"
                },
            ]
        )
        print "[INFO] Enabling Detailed Metrics on stage %s" % stage_name
        self.api_client.update_stage(
            restApiId=rest_api_id,
            stageName=stage_name,
            patchOperations=[
                {
                    'op': 'replace',
                    'path': '/*/*/metrics/enabled',
                    'value': "true"
                },
            ]
        )
        print "[INFO] Enabling Datatrace on stage %s" % stage_name
        self.api_client.update_stage(
            restApiId=rest_api_id,
            stageName=stage_name,
            patchOperations=[
                {
                    'op': 'replace',
                    'path': '/*/*/logging/dataTrace',
                    'value': "true"
                },
            ]
        )

        return True

    def create_deployment(self, rest_api_id, stage_name, description):
        response = self.api_client.create_deployment(
            restApiId=rest_api_id,
            stageName="dev",
            # stageDescription='string',
            description=description,
            # cacheClusterEnabled=True | False,
            # cacheClusterSize='0.5' | '1.6' | '6.1' | '13.5' | '28.4' | '58.2' | '118' | '237',
            # variables={
            #     'string': 'string'
            # }
        )
        deployment_id = response["id"]

        if not deployment_id:
            print "[FAIL] Deployment Failed"
            return False

        # Update the stage with new set of variables
        response = self.api_client.update_stage(
            restApiId=rest_api_id,
            stageName=stage_name,
            patchOperations=[
                {
                    'op': 'replace',
                    'path': '/deploymentId',
                    'value': deployment_id
                },
            ]
        )
        if response["ResponseMetadata"]['HTTPStatusCode'] == 200:
            print "[INFO] Deployed to stage %s with Deployment ID %s" % (stage_name, deployment_id)
        else:
            print "[FAIL] Unable to copy stage variables"
            print response
            return False
        return True

    def update_stage(self, stack_id, rest_api_id, stage_name):
        stages = self.api_client.get_stages(
            restApiId=rest_api_id
        )
        dev_stage = None
        to_stage = None

        # Get the dev stage which is created with cloudformation
        for stage in stages["item"]:
            if stage["stageName"] == "dev":
                dev_stage = stage
            if stage["stageName"] == stage_name:
                to_stage = stage
        to_stage_variables = {}
        # Add lambda alias as a suffix to stage variables
        for k, v in dev_stage["variables"].iteritems():
            to_stage_variables[k] = v.replace(":%s" % dev_stage["stageName"], ":%s" % stage_name)
            # Check if its a new variable (lambda) then add permission for gateway to invoke
            if k not in to_stage["variables"]:
                self.add_lambda_permission(function_name=to_stage_variables[k],
                                           region=self.session.region_name,
                                           account_id=stack_id,
                                           rest_api_id=rest_api_id
                                           )
                # Update the stage with new set of variables
                response = self.api_client.update_stage(
                    restApiId=rest_api_id,
                    stageName=stage_name,
                    patchOperations=[
                        {
                            'op': 'replace',
                            'path': '/variables/%s' % k,
                            'value': v.replace(dev_stage["stageName"], stage_name)
                        },
                    ]
                )
                if response["ResponseMetadata"]['HTTPStatusCode'] == 200:
                    print "[INFO] Stage Variable %s Added" % v.replace(dev_stage["stageName"], stage_name)
                else:
                    print "[FAIL] Unable to copy stage variables"
                    print response

    def add_lambda_permission(self, function_name, region, account_id, rest_api_id):
        print "[INFO] Adding permission for rest api %s on region %s in account %s to invoke lambda %s" % (
            rest_api_id, region, account_id, function_name)
        response = self.lambda_client.add_permission(
            FunctionName=function_name,
            StatementId='%s%s%s' % (
                function_name.replace(':', ''), rest_api_id, ''.join(random.choice(string.ascii_lowercase) for i in range(6))),
            Action='lambda:InvokeFunction',
            Principal='apigateway.amazonaws.com',
            SourceArn="arn:aws:execute-api:%s:%s:%s/*" % (region, account_id, rest_api_id)
        )
        print "[INFO] Added Permission to Lambda %s" % response["Statement"]
        return True

    def get_live_stack(self, domain_name):
        """
        # Todo rename this function to get_live_stock.. Mooo...
        :param gateway_stack_name:
        :param domain_name:
        :return: string (blue or green)
        """
        response = self.api_client.get_base_path_mappings(
            domainName=domain_name,
        )

        live_stage = None
        for item in response["items"]:
            if item["basePath"] == self.live_base_path:
                live_stage = item["stage"]
                break

        if live_stage not in self.aliases:
            print "[FAIL] Stage name not supported must be one of %s" % str(self.aliases)
            sys.exit(1)

        print "[INFO] Current Live Colour %s" % live_stage
        return live_stage

    def switch_stages(self, domain_name, base_path, to_stage_name):
        response = self.api_client.update_base_path_mapping(
            domainName=domain_name,
            basePath=base_path,
            patchOperations=[
                {
                    'op': 'replace',
                    'path': '/stage',
                    'value': to_stage_name
                },
            ]
        )
        print response
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            print "[FAIL] Unable to switch stages"
            return False
        return True

    def serverless_lambda_deploy(self, gateway_stack_name, lambda_stack_name, code_key):
        """
        Checks if stack has a custom domain and deploys code to the non-active linked stage.
        :param gateway_stack_name:
        :param lambda_stack_name:
        :param code_key: s3 key
        :return:
        """

        domain_name = self.get_stack_domain_name(gateway_stack_name)

        if not domain_name:
            print "[WARN] Custom Domain not found. Depolying to $LATEST"
            self.lambda_deploy_code(lambda_stack_name, code_key)
            return True

        current_live_stage = self.get_live_stack(domain_name)

        to_alias = None

        if current_live_stage == 'green':
            to_alias = 'blue'
        elif current_live_stage == 'blue':
            to_alias = 'green'

        lambdas = self.get_stack_lambdas(lambda_stack_name)
        print "[INFO] Updating lambda code for %s " % str(lambdas)

        for aws_lambda in lambdas:

            self.get_or_set_lambda_alias(aws_lambda)
            function_arn = self.get_lambda_arn(aws_lambda)
            self.update_lambda_code_key(function_arn, code_key)
            code_bucket, code_key = self.get_lambda_code_bucket_and_key(function_arn)

            print "[INFO] Updating lambda code for %s with bucket: %s & key: %s" % (
                aws_lambda, code_bucket, code_key)

            self.lambda_client.update_function_code(
                FunctionName=aws_lambda,
                S3Bucket=code_bucket,
                S3Key=code_key,
                # S3ObjectVersion='string', # TODO Soon!
                Publish=True
            )

            response = self.lambda_client.publish_version(
                FunctionName=aws_lambda,
                Description=datetime.now().strftime("%A, %d. %B %Y %I:%M%p %S")
            )

            version = response["Version"]

            if not to_alias or not version:
                print "[FAIL] Unable to version deploy"

            self.lambda_client.update_alias(
                FunctionName=aws_lambda,
                Name=to_alias,
                FunctionVersion=version
            )

            print "[INFO] Function %s Updated to version %s linked to alias %s" % (aws_lambda, version, to_alias)

    def gateway_init_bg(self, gateway_stack_name):
        """

        :param gateway_stack_name: api gateway stack name (string)
        :return: bool
        """
        stack_id = self.get_stack_account(gateway_stack_name)
        rest_api_id = self.get_stack_restapi(gateway_stack_name)
        stages = self.api_client.get_stages(
            restApiId=rest_api_id
        )
        initial_stage = None

        # Get the dev stage which is created with cloudformation
        for stage in stages["item"]:
            if stage["stageName"] == "dev":
                initial_stage = stage
                break

        print "[INFO] Adding blue/green stages"
        # Create blue and green stages from dev stage
        self.copy_stage(stack_id, rest_api_id, initial_stage, "blue")
        self.copy_stage(stack_id, rest_api_id, initial_stage, "green")
        self.enable_metrics(rest_api_id, "blue")
        self.enable_metrics(rest_api_id, "green")

        return True

    def gateway_init_public(self, gateway_stack_name):
        """
        Link Base Path mappings to Blue Green Stage
        :param gateway_stack_name:
        :return:
        """
        rest_api_id = self.get_stack_restapi(gateway_stack_name)
        domain_name = self.get_stack_domain_name(gateway_stack_name)
        if not domain_name:
            print "[INFO] No custom domain found."
            return False

        # Link / to /blue
        self.api_client.create_base_path_mapping(
            domainName=domain_name,
            basePath="api",
            restApiId=rest_api_id,
            stage=self.aliases[1]
        )
        # Link /pvt to /green
        self.api_client.create_base_path_mapping(
            domainName=domain_name,
            basePath="pvt",
            restApiId=rest_api_id,
            stage=self.aliases[2]
        )

        return True

    def publish_stage_changes(self, gateway_stack_name, live=False):
        """
        Updates the non live stage to dev
        :param gateway_stack_name:
        :param live: bool - set to true to push to active stage
        :return:
        """
        rest_api_id = self.get_stack_restapi(gateway_stack_name)
        domain_name = self.get_stack_domain_name(gateway_stack_name)
        stack_id = self.get_stack_account(gateway_stack_name)
        if not domain_name:
            print "[FAIL] No custom domain found."
            return False
        current_live_stage = self.get_live_stack(domain_name)

        if current_live_stage == 'green':
            to_stage = 'blue'
        elif current_live_stage == 'blue':
            to_stage = 'green'
        else:
            print "[FAIL] Stage name not supported must be one of %s" % str(self.aliases)
            sys.exit(1)

        if not live:
            print "[INFO] Copying dev stage changes to pvt stage %s" % to_stage
            self.update_stage(stack_id, rest_api_id, to_stage)
            self.create_deployment(rest_api_id, to_stage, "Deployed by PyStacks")
        else:
            print "[INFO] Copying dev stage changes to live stage %s" % current_live_stage
            self.update_stage(stack_id, rest_api_id, current_live_stage)
            self.create_deployment(rest_api_id, current_live_stage, "Deployed by PyStacks")

    def serverless_blue_green_switch(self, gateway_stack_name):
        """
        Switch live base path between blue and green stage
        :param gateway_stack_name:
        :return:
        """
        domain_name = self.get_stack_domain_name(gateway_stack_name)
        current_live_stage = self.get_live_stack(domain_name)

        if current_live_stage == 'green':
            to_stage = 'blue'
        elif current_live_stage == 'blue':
            to_stage = 'green'
        else:
            print "[FAIL] Stage name not supported must be one of %s" % str(self.aliases)
            sys.exit(1)

        if self.switch_stages(domain_name, self.live_base_path, to_stage):
            self.switch_stages(domain_name, self.pvt_base_path, current_live_stage)
        else:
            print "[FAIL] Unable to switch stages"
            sys.exit(1)

        self.get_live_stack(domain_name)
