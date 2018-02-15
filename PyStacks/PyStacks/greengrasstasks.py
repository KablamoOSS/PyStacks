import json
import botocore
from botocore.exceptions import ParamValidationError
from random import randint
from greengrass import GreengrassAPI
from iot import IoTAPI
from s3tasks import upload_object, sanitise_bucket_name, s3tasks as S3Tasks

from logger import get_pystacks_log
log = get_pystacks_log()


class GGgroup:
    """Greengrass Group object

    The simplest usage pattern is on an existing group:
        >>> gg_group = GGgroup(session, gg_projectname)
        >>> gg_group.deploy()

    This will get a group instance. If the group exists already in your AWS IoT account the information required
    for a redeploy will be populated into the instance.  The second line redeploys the group with its existing
    configurations.

    You may modify a groups attributes with any of the following methods:
        >>> gg_group.define_devices(config)
        >>> gg_group.define_functions(config)
        >>> gg_group.define_subscriptions(config)
        >>> gg_group.define_logs(config)
        >>> gg_group.smart_deploy()

    The `config` object must be in the following form. Do what you need to get it there:

    config (dict):
        {
            'stackname':    # required for s3 bucket creation/location
            'region:        # required for s3 bucket creation/location
            'resources': {
                'greengrass': {
                    "name": "project_name",
                    "s3Bucket": "root-gg-project_bucket",           // must exist
                    'core': {
                        'ip': 'physical device addr',
                        **<thing attributes>
                    },
                    'devices': {            // Optional
                        'Device1': <thing attributes>
                    },
                    'subscriptions': [
                        {
                            "source": deviceName/'cloud',lambdaName,
                            "target": deviceName/'cloud',lambdaName,
                            "subject": <subject spec>                           // should be called 'topic'
                        },
                        {   // For subscriptions to or from 'shadow'
                            "source": "SwitchPy",
                            "subject": {
                                "device": "RobotArm",
                                "path": "update"
                            },
                            "target": "shadow"
                        },
                        ...
                    ],
                    'lambdas': {
                        'Lambda1': {
                            "configuration": {
                                "Pinned": "False",
                                "Executable": "uptimeLambda.uptime_handler",
                                "MemorySize": 128000,
                                "Timeout": 3
                            },
                            "arn": "arn:aws:lambda:ap-southeast-2:167464700695:function:RAuptime:GGRobotArmPY"
                        },
                        'Lambda2':
                        ...
                    },
                    "logging": [
                        {
                            "Component": "GreengrassSystem",
                            "Level": "INFO",
                            "Type": "FileSystem",
                            "Space": 5120
                        },
                        {
                            "Component": "Lambda",
                            "Level": "DEBUG",
                            "Type": "FileSystem",
                            "Space": 5120
                        }
                    ],
                }
            }
        }

        thing attributes (dict):
            'PolicyName'          # Must exist
            'syncShadow'          # Optional (defaults to true)
        subject spec (str/dict): if the target or subject is 'shadow' a dict should be used, otherwise str.
            {
                "device": "RobotArm",
                "path": "update",
            }
            OR:
            "/topic/state"
    """

    def __init__(self, session, project_name):
        """Initialise the Greengrass group object

        Args:
            session (<class 'boto3.session.Session'>):
            project_name (str):  If a project already exists, ensure this field is the same as the existing one.  This will be used in the naming of many group members to ensure uniquenss in the same account.  It is also used to identify whether or not the group already exists.

        Returns: None
        """

        self.session = session
        self.gg = GreengrassAPI(session)
        self.iot = IoTAPI(session)

        self.project_name = project_name
        self.group_name = self.project_name + '_Group'
        self.core_name = self.project_name + '_Core'
        # Group constituent properties
        self.device_arns = {}
        self.cert_arns = {}
        self.device_spec = []
        self.version_arns = {
            'CoreDefinitionVersionArn': None,
            'LoggerDefinitionVersionArn': None,
            'FunctionDefinitionVersionArn': None,
            'DeviceDefinitionVersionArn': None,
            'SubscriptionDefinitionVersionArn': None,
        }

        # Does this group already exist?
        self.group_info = self._get_group_info()
        if self.group_info:  # If so, get its constituent properties
            try:
                self.version_arns = self.gg.get_group_version(
                    group_id=self.group_info['Id'],
                    latest_version=self.group_info['LatestVersion'],
                )['Definition']
                self.device_spec = self.get_full_spec('Devices')
                self.cert_arns = {p['ThingArn'].split('/')[-1]: p['CertificateArn'] for p in self.device_spec}
                self.device_arns = {p['ThingArn'].split('/')[-1]: p['ThingArn'] for p in self.device_spec}
            except (KeyError, ParamValidationError) as err:
                log.warn("Half made group. Removing all parts before creation. Error: ", str(err))
                self._destroy_devices()
                self._remove_group()
                self.group_info = None

        # Class variables only filled during creation
        self.lambdas = None

    def _get_group_info(self):
        group_info = None
        for g in self.gg.list_groups()['Groups']:
            if g['Name'] == self.group_name:
                group_info = g
                break

        if not group_info:
            log.info("Group {} cannot be found".format(self.group_name))
        self.group_info = group_info
        return group_info

    def define_devices(self, config):
        """Define the devices that will be part of the greengrass group.
        This must include one and only one core.  It may optionally contain auxilliary devices.
        If the group already exists, the device specifications will be compared with those currently
        deployed.  Only the changes will be effected.

        Args:
            config (dict): See specication in class docs

        Returns: None
        """

        log.info("Creating and defining IoT things")

        kms_key = config['resources']['greengrass'].get('kmsKeyId')

        # Include project name in thing name for uniqueness.  Also accomodate deployment with no devices
        devices_config = {}
        for device, device_spec in config['resources']['greengrass'].get('devices', {}).items():
            devices_config[self.project_name + '_' + device] = device_spec
        # And finally, add in the core config
        devices_config[self.core_name] = config['resources']['greengrass']['core']

        # Pop out the 'Things' that already exist
        deployed_devices = {d['ThingArn'].split('/')[-1] for d in self.device_spec}
        devices_to_remove = deployed_devices.difference(set(devices_config))  # Store this before modifying
        for device in deployed_devices:
            devices_config.pop(device, None)

        # Create the unmade things
        new_device_arns, new_cert_arns = _make_things_upload_keys(
            self.session,
            project_name=self.project_name,
            devices_config=devices_config,
            save_to_s3=True,
            bucket_name=config['resources']['greengrass']['s3Bucket'],
            bucket_region=config['region'],
            kms_key=kms_key,
        )
        self.device_arns.update(new_device_arns)
        self.cert_arns.update(new_cert_arns)

        # Remove the old things now not required
        for device in devices_to_remove:
            log.info("Removing: " + device)
            self.device_arns.pop(device)
            self.cert_arns.pop(device)
            for d in self.device_spec:
                if device in d['ThingArn']:
                    self.device_spec.remove(d)

        self._destroy_devices(devices_to_remove)

        # Finally create 'Versions' to deploy the group with
        self._modify_device_versions(config, devices_config)

    def _modify_device_versions(self, config, devices_config=None):
        self.version_arns['CoreDefinitionVersionArn'] = self._create_core_version()

        # Save to core config to s3
        bucket = config['resources']['greengrass']['s3Bucket']
        dest_filename = '{project_name}/{project_name}_Core/config.json'.format(**self.__dict__)

        core_config = generate_core_config(self.session, self.device_arns[self.core_name], config['region'])
        upload_object(
            bucket=bucket,
            dest_filename=dest_filename,
            binary_contents=json.dumps(core_config, sort_keys=True, indent=4, separators=(',', ': ')).encode(),
            session=self.session,
        )
        log.info("Core config saved to:  s3://{bucket}/{dest_filename}".format(**locals()))

        if not devices_config:
            return

        self.version_arns['DeviceDefinitionVersionArn'] = self._create_device_version(config=devices_config)
        log.info("All devices created and version definition created")

    def define_functions(self, config):
        """Define lambda functions to run on the Greengrass deployment.  Optional.

        Args:
            config (dict): See specication in class docs

        Returns: None
        """

        if 'lambdas' not in config['resources']['greengrass'].keys():
            log.debug("No lambda specified for this group")
            return None

        log.info("Defining group lambda functions")
        self.lambdas = config['resources']['greengrass']['lambdas']

        self.version_arns['FunctionDefinitionVersionArn'] = self._create_lambda_version(
            config=self.lambdas,
            name=self.project_name + '_Functions',
        )

    def define_subscriptions(self, config):
        """Define the MQTT communication channels between all member of the Greengrassgroup. Optional.

        Args:
            config (dict): See specication in class docs

        Returns: None
        """

        if 'subscriptions' not in config['resources']['greengrass'].keys():
            log.debug("No subscriptions specified for this group")
            return None

        log.info("Defining group subscriptions")

        # Ensure devices have unique names with project names used
        # subscription_config=config['resources']['greengrass']['subscriptions'],

        self.version_arns['SubscriptionDefinitionVersionArn'] = self._create_subscription_version(
            subscription_config=config['resources']['greengrass']['subscriptions'],
            device_arns=self.device_arns,
            lambdas=self.lambdas,
            name=self.project_name + '_Subscriptions',
            project_name=self.project_name,
        )

    def define_logs(self, config):
        """Define the logging within the Greengrass group.  Optional.

        Args:
            config (dict): See specication in class docs

        Returns: None
        """

        if 'logging' not in config['resources']['greengrass'].keys():
            log.debug("No logging specified for this group")
            return None

        log.info("Defining group logging")

        self.version_arns['LoggerDefinitionVersionArn'] = self._create_logging_version(
            config=config['resources']['greengrass']['logging'],
            name=self.project_name + '_Functions',
        )

    def smart_deploy(self, config):
        """Deploy a Greengrass group.  Redeploy if deployment already exists.

        Args:
            config (dict): See specication in class docs

        Returns: None
        """

        log.info("Creating group")

        if not self.group_info:  # Group does not already exist
            self.group_info = self.gg.create_group(
                name=self.group_name,
            )
            log.info("Group {Name} created with Id: {Id}".format(**self.group_info))
        else:
            log.info("Group {Name} already exists. Updating ".format(**self.group_info))

        # Update group_info
        response = self.gg.create_group_version(self.group_info['Id'], self.version_arns)
        self.group_info['LatestVersion'], self.group_info['LatestVersionArn'] = response['Version'], response['Arn']

        update_connectivity_info_response = self.gg.update_connectivity_info(
            core_name=self.core_name,
            core_addr=config['resources']['greengrass']['core']['ip'],
        )
        log.debug("Connectivity info for core updated: ")

        return self.deploy()

    def deploy(self):
        """Triggers a Deploy/ReDeploy only"""

        if not self.group_info:
            log.error("Group does not exist.")
            return

        create_deployment_response = self.gg.create_deployment(
            deployment_type='NewDeployment',
            group_id=self.group_info['Id'],
            group_version=self.group_info['LatestVersion'],
        )
        log.info("Group {} deployed".format(self.group_name))
        return create_deployment_response

    def _remove_group(self):
        if self.group_info:
            log.info("Group '{group_name}' found.".format(**self.__dict__))
            try:
                reset_deployments_response = self.gg.reset_deployments(self.group_info['Id'])
                log.info("Group '{group_name}' successfully reset.".format(**self.__dict__))
            except botocore.exceptions.ClientError:
                log.warn("No deployed cores for group '{group_name}'.  It has probaly been reset already.".format(**self.__dict__))
            except Exception as e:
                log.error("Failed to reset deployment: {group_name}, Id: {group_id}".format(**self.__dict__))
                raise e

            # Delete Them
            delete_group_response = self.gg.delete_group(self.group_info['Id'])
            log.info("Group '{group_name}' successfully deleted.".format(**self.__dict__))
        else:
            log.warn("Group '{group_name}' not found ...".format(**self.__dict__))

    def _destroy_devices(self, things):
        """Certificates must be 'detached' before they are deleted."""

        detached_principles = self._remove_things(things)
        self._delete_certificates(detached_principles)

    def _remove_things(self, things):
        """'things' must be an itterable of thing names.  Do what you need to do to get it."""

        detached_principles = []
        for thing in things:
            log.info("deleting: {}".format(thing))
            detached_principles.extend(self.detach_thing_certificates(thing))
            self.iot.delete_thing(thing)

        return detached_principles

    def _delete_certificates(self, certificates):
        for cert in self.iot.list_certificates()['certificates']:
            if cert['certificateArn'] not in certificates:
                continue

            log.info("Deleting: {certificateId}".format(**cert))

            # First set to INACTIVE
            self.iot.update_certificate(
                cert_id=cert['certificateId'],
                new_status='INACTIVE',
            )

            # Next, detach policy
            for policy in self.iot.list_attached_policies(cert['certificateArn'])['policies']:
                log.debug("Detaching {} from: {}".format(policy['policyName'], cert['certificateId']))
                self.iot.detach_policy(
                    policy_name=policy['policyName'],
                    principal=cert['certificateArn'],
                )

            # Finally delete
            self.iot.delete_certificate(cert['certificateId'])

    def detach_thing_certificates(self, thing_name):
        detached_principles = []
        for principal in self.iot.list_thing_principals(thing_name)['principals']:
            log.debug("detaching principle:" + principal)
            self.iot.detach_thing_principal(
                thing_name=thing_name,
                principal=principal,
            )
            detached_principles.append(principal)
        return detached_principles

    def _create_core_version(self):
        coreSpecs = [
            {
                'CertificateArn': self.cert_arns[self.core_name],
                'SyncShadow': True,
                'Id': str(randint(1e5, 1e6)),
                'ThingArn': self.device_arns[self.core_name],
            },
        ]
        create_core_definition_results = self.gg.create_core_definition(name=self.core_name)
        create_core_definition_version_response = self.gg.create_core_definition_version(
            coreDefId=create_core_definition_results['Id'],
            coreSpecs=coreSpecs,
        )
        return create_core_definition_version_response['Arn']

    def _create_device_version(self, config):
        log.debug("Creating device version")

        for device, device_config in config.items():
            self.device_spec.append(
                {
                    "Id": device,
                    "CertificateArn": self.cert_arns[device],
                    "SyncShadow": device_config.get('syncShadow', True),
                    "ThingArn": self.device_arns[device],
                }
            )

        create_device_definition_response = self.gg.create_device_definition(self.project_name + '_Devices')
        create_device_definition_version_response = self.gg.create_device_definition_version(
            device_definition_id=create_device_definition_response['Id'],
            devices=self.device_spec,
        )

        return create_device_definition_version_response['Arn']

    def _create_lambda_version(self, config, name=None):
        name = name if name else self.project_name + '_Functions'

        function_definitions = []
        for name, func in config.items():
            function_definitions.append(
                {
                    'FunctionArn': func['arn'],
                    'FunctionConfiguration': func['configuration'],
                    'Id': name,
                }
            )

        create_function_definition_response = self.gg.create_function_definition(name=name)
        create_function_definition_version_response = self.gg.create_function_definition_version(
            funcDefId=create_function_definition_response['Id'],
            funcSpecs=function_definitions,
        )

        return create_function_definition_version_response['Arn']

    def _create_subscription_version(self, subscription_config, device_arns, lambdas, project_name, name):
        name = name if name else self.project_name + '_Subscriptions'

        log.info("Defining group functions")
        create_subscription_definition_response = self.gg.create_subscription_definition(name=name)
        create_subscription_definition_version_response = self.gg.create_subscription_definition_version(
            subDefId=create_subscription_definition_response['Id'],
            definitions=_write_subscription_definitions(subscription_config, device_arns, lambdas, self.project_name),
        )

        return create_subscription_definition_version_response['Arn']

    def _create_logging_version(self, config, name=None):
        name = name if name else self.project_name + '_Functions'

        # an Id parameter is required, give it random ints at this stage
        for l in config:
            l['Id'] = str(randint(1e5, 1e6))

        create_logger_definition_response = self.gg.create_logger_definition(name)
        create_logger_definition_version_response = self.gg.create_logger_definition_version(
            definition_id=create_logger_definition_response['Id'],
            config=config,
        )

        return create_logger_definition_version_response['Arn']

    def get_full_spec(self, attribute, arn=None):
        """Gain the existing specifications of an attribute of a greengrass group.

        Args:
            attribute (str):    One of: ['Subscriptions', 'Devices', 'Loggers', 'Functions', 'Cores']
            arn (str):          Provide an Arn of a defintion version or the latest one the group has will be used.

        Returns:
            list or dict of the specifcations of the attribute.  The format is the format required
            for input a `create_<attribute>_definition_version`
        """

        # Hash map would be better but this is more clear
        if attribute == 'Subscriptions':
            list_definitions = self.gg.list_subscription_definitions
            get_definition_version = self.gg.get_subscription_definition_version
            arn_key = 'SubscriptionDefinitionVersionArn'
        elif attribute == 'Devices':
            list_definitions = self.gg.list_device_definitions
            get_definition_version = self.gg.get_device_definition_version
            arn_key = 'DeviceDefinitionVersionArn'
        elif attribute == 'Loggers':
            list_definitions = self.gg.list_logger_definitions
            get_definition_version = self.gg.get_logger_definition_version
            arn_key = 'LoggerDefinitionVersionArn'
        elif attribute == 'Functions':
            list_definitions = self.gg.list_function_definitions
            get_definition_version = self.gg.get_function_definition_version
            arn_key = 'FunctionDefinitionVersionArn'
        elif attribute == 'Cores':
            list_definitions = self.gg.list_core_definitions
            get_definition_version = self.gg.get_core_definition_version
            arn_key = 'CoreDefinitionVersionArn'
        else:
            raise Exception("attribute not supported")

        if not arn:
            arn = self.version_arns[arn_key]

        def_info = None
        for sub_def in list_definitions()['Definitions']:
            if sub_def.get('LatestVersionArn') == arn:
                def_info = sub_def

        if not def_info:
            log.warn("No definition found for {attribute} with version Arn of: {arn}".format(**locals()))
            return None

        get_definition_version_response = get_definition_version(
            definition_id=def_info['Id'],
            latest_version=def_info['LatestVersion'],
        )

        return get_definition_version_response['Definition'][attribute]


def generate_core_config(session, core_thing_Arn, region):
    return {
        "coreThing": {
            "caPath": "root.ca.pem",
            "certPath": "cloud.pem.crt",
            "keyPath": "cloud.pem.key",
            "thingArn": core_thing_Arn,
            "iotHost": IoTAPI(session).describe_endpoint()['endpointAddress'],
            "ggHost": "greengrass.iot.{region}.amazonaws.com".format(region=region),
            "keepAlive": 600
        },
        "runtime": {
            "cgroup": {
                "useSystemd": "yes"
            }
        },
        "system": {
            "shadowSyncTimeout": 10
        }
    }


def _make_thing(session, group_name, device_name, device_config):
    iot = IoTAPI(session)  # consider passing this in instead of 'session'. (save on object instantiation)

    create_thing_response = iot.create_thing(device_name, attributes={'group': group_name})
    log.info(device_name + " created ...")
    create_keys_and_certificate_response = iot.create_keys_and_certificate()

    # TODO: consider appending project name to each device here to ensure uniquness
    attach_thing_principal_results = iot.attach_thing_principal(
        device_name,
        create_keys_and_certificate_response['certificateArn'],
    )

    # Give the cert a pre-existing policy
    attach_policy_response = iot.attach_policy(
        policyName=device_config['policyName'],  # Let this raise its own Exception if empty (for now)
        certArn=create_keys_and_certificate_response['certificateArn']
    )
    log.debug("Policy '{}' attached to certificate ID: {}".format(device_config['policyName'], create_keys_and_certificate_response['certificateId']))

    return (create_thing_response['thingArn'],
            create_keys_and_certificate_response['certificateArn'],
            create_keys_and_certificate_response['certificatePem'],
            create_keys_and_certificate_response['keyPair'],
            )


def _make_things_upload_keys(session, project_name, devices_config, save_to_s3=False, bucket_name=None, bucket_region=None, kms_key=None):
    """Creates IoT things, returns a their certificate Arn and IoT thing Arn

    Args:
        session (aws session object): Obtain from the auth module `getBaseSession`
        config (dict): See specication in class docs
        save_to_s3 (bool: optional): Default True. Saves keys to and s3 bucket named after the project name

    Returns:
        device_arns (dict):
        cert_arns (dict):
    """

    if save_to_s3:
        if not bucket_region or not bucket_name:
            raise Exception("a bucket_region and bucket_name must be specified if 'save_to_s3' is True")

        log.debug("Getting bucket to save keys and certificates in ")
        s3tasks = S3Tasks(session)
        bucket = s3tasks.get_bucket(sanitise_bucket_name(bucket_name), bucket_region, create=True)

    device_arns = {}
    cert_arns = {}
    for device, device_config in devices_config.items():
        log.debug("creating " + device)
        device_arns[device], cert_arns[device], device_cert_pem, device_keypair = _make_thing(session, project_name, device, device_config)
        if save_to_s3:
            upload_object(bucket, project_name + '/' + device + '/cloud.pem.crt', device_cert_pem.encode(), kms_key)
            upload_object(bucket, project_name + '/' + device + '/cloud.pem.key', device_keypair['PrivateKey'].encode(), kms_key)
        log.info("Certificate and private key saved to: s3://{bucket.name}/{project_name}/{device}/".format(**locals()))
    return device_arns, cert_arns


def _write_subscription_definitions(subscription_config, device_arns, lambdas, project_name):
    subscription_definitions = []

    def interpret_endpoint(endpoint, subscription):
        s_or_t = None
        ept = subscription[endpoint].strip()

        if ept == 'cloud':
            s_or_t = 'cloud'
        elif ept == 'shadow':
            s_or_t = 'GGShadowService'
        elif ept in lambdas:
            s_or_t = lambdas[ept]['arn']
        elif project_name + '_' + ept in device_arns:
            s_or_t = device_arns[project_name + '_' + ept]
        else:
            raise Exception("Allowed values: ['cloud', 'shadow', <lambda_name>, <device_name>]. The lambda/device is not defined: '{}'".format(ept))
        return s_or_t

    def interpret_subject(subject):
        if isinstance(subject, basestring):
            return project_name + "/" + subject.strip("/")
        elif isinstance(subject, dict):
            return "$aws/things/" + subject['device'] + "/shadow/" + subject['path'].strip("/")
        else:
            msg = "yaml subject format is incorrect {}".format(subject)
            log.error(msg)
            raise Exception(msg)

    for subscription in subscription_config:
        subscription_definitions.append(
            {
                'Id': str(randint(0, 1e9)),
                'Source': interpret_endpoint('source', subscription),
                'Subject': interpret_subject(subscription['subject']),
                'Target': interpret_endpoint('target', subscription),
            }
        )

    return subscription_definitions


def remove_group_with_config(session, config):
    project_name = config['resources']['greengrass']['name']
    log.info("Removing project: " + project_name)
    gg_group = GGgroup(session, project_name)

    log.debug("Looking for 'things' with attribute: 'group': '{}'".format(gg_group.project_name))
    group_things = [thing['thingName'] for thing in gg_group.iot.list_things()['things'] if thing['attributes'].get('group', 'has no group') == gg_group.project_name]

    gg_group._destroy_devices(group_things)
    gg_group._remove_group()


def create_group_with_config(session, config):
    """Should only ever be called by the CLI.  A good example of how to create a GreenGrass group
    using the library"""

    # 1. Instantiate the group
    project_name = config['resources']['greengrass']['name']
    gg_group = GGgroup(session, project_name)

    # 2. Define the group characteristics
    gg_group.define_devices(config)
    gg_group.define_functions(config)
    gg_group.define_subscriptions(config)
    gg_group.define_logs(config)

    # 3.  Finish
    gg_group.smart_deploy(config)
