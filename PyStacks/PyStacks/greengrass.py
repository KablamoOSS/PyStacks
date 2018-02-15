from verification import ensure_http_success


class GreengrassAPI:
    def __init__(self, session):
        self.client = session.client('greengrass')

    @ensure_http_success
    def create_core_definition(self, name):
        return self.client.create_core_definition(Name=name)

    @ensure_http_success
    def list_groups(self):
        return self.client.list_groups()

    @ensure_http_success
    def create_core_definition_version(self, coreDefId, coreSpecs):
        return self.client.create_core_definition_version(
            CoreDefinitionId=coreDefId,
            Cores=coreSpecs,
        )

    @ensure_http_success
    def update_core_definition(self, coreid, name):
        return self.client.update_core_definition(
            CoreDefinitionId=coreid,
            Name=name,
        )

    @ensure_http_success
    def delete_core_definition(self, coreid):
        return self.client.delete_core_definition(
            CoreDefinitionId=coreid
        )

    @ensure_http_success
    def create_device_definition(self, name, token=None, version=None):
        params = {
            "AmznClientToken": token,
            "InitialVersion": version,
            "Name": name,
        }
        return self.client.create_device_definition(**{k: v for k, v in params.items() if v})

    @ensure_http_success
    def update_device_definition(self, deviceid, name):
        return self.client.update_device_definition(
            DeviceDefinitionId=deviceid,
            Name=name,
        )

    @ensure_http_success
    def delete_device_definition(self, deviceid):
        return self.client.delete_device_definition(
            DeviceDefinitionId=deviceid,
        )

    @ensure_http_success
    def create_function_definition(self, name):
        return self.client.create_function_definition(Name=name)

    @ensure_http_success
    def create_function_definition_version(self, funcDefId, funcSpecs):
        return self.client.create_function_definition_version(
            FunctionDefinitionId=funcDefId,
            Functions=funcSpecs,
        )

    @ensure_http_success
    def create_subscription_definition(self, name):
        return self.client.create_subscription_definition(Name=name)

    @ensure_http_success
    def create_subscription_definition_version(self, subDefId, definitions):
        return self.client.create_subscription_definition_version(
            SubscriptionDefinitionId=subDefId,
            Subscriptions=definitions,
        )

    @ensure_http_success
    def update_function_definition(self, functionid, name):
        return self.client.update_function_definition(
            FunctionDefinitionId=functionid,
            Name=name,
        )

    @ensure_http_success
    def delete_function_definition(self, functionid):
        return self.client.delete_function_definition(FunctionDefinitionId=functionid)

    @ensure_http_success
    def create_group(self, name):
        return self.client.create_group(Name=name)

    @ensure_http_success
    def create_group_version(self, group_id, version_arns):
        params = version_arns.copy()
        params['GroupId'] = group_id
        return self.client.create_group_version(**params)

    @ensure_http_success
    def update_group(self, groupid, name):
        return self.client.update_group(
            GroupId=groupid,
            Name=name,
        )

    @ensure_http_success
    def delete_group(self, group_id):
        return self.client.delete_group(
            GroupId=group_id,
        )

    @ensure_http_success
    def associate_role_to_group(self, groupid, rolearn):
        return self.client.associate_role_to_group(
            GroupId=groupid,
            RoleArn=rolearn,
        )

    @ensure_http_success
    def get_deployment_status(self, DeploymentId, GroupId):
        return self.client.get_deployment_status(
            DeploymentId=DeploymentId,
            GroupId=GroupId,
        )

    @ensure_http_success
    def reset_deployments(self, group_id, force=True):
        return self.client.reset_deployments(
            Force=force,
            GroupId=group_id,
        )

    @ensure_http_success
    def update_connectivity_info(self, core_name, core_addr):
        return self.client.update_connectivity_info(
            ConnectivityInfo=[
                {
                    'HostAddress': core_addr,
                    'Id': '0',
                    'Metadata': '',  # Not required
                    'PortNumber': 8883
                },
            ],
            ThingName=core_name,
        )

    @ensure_http_success
    def create_deployment(self, deployment_type, group_id, group_version):
        return self.client.create_deployment(
            DeploymentType=deployment_type,
            GroupId=group_id,
            GroupVersionId=group_version,
        )

    @ensure_http_success
    def create_device_definition_version(self, device_definition_id, devices):
        return self.client.create_device_definition_version(
            DeviceDefinitionId=device_definition_id,
            Devices=devices,
        )

    @ensure_http_success
    def create_logger_definition(self, name):
        return self.client.create_logger_definition(Name=name)

    @ensure_http_success
    def create_logger_definition_version(self, definition_id, config):
        return self.client.create_logger_definition_version(
            LoggerDefinitionId=definition_id,
            Loggers=config,
        )

    @ensure_http_success
    def get_group_version(self, group_id, latest_version):
        return self.client.get_group_version(
            GroupId=group_id,
            GroupVersionId=latest_version,
        )

    @ensure_http_success
    def get_core_definition_version(self, definition_id, latest_version):
        return self.client.get_core_definition_version(
            CoreDefinitionId=definition_id,
            CoreDefinitionVersionId=latest_version
        )

    @ensure_http_success
    def get_device_definition_version(self, definition_id, latest_version):
        return self.client.get_device_definition_version(
            DeviceDefinitionId=definition_id,
            DeviceDefinitionVersionId=latest_version
        )

    @ensure_http_success
    def get_logger_definition_version(self, definition_id, latest_version):
        return self.client.get_logger_definition_version(
            LoggerDefinitionId=definition_id,
            LoggerDefinitionVersionId=latest_version
        )

    @ensure_http_success
    def get_subscription_definition_version(self, definition_id, latest_version):
        return self.client.get_subscription_definition_version(
            SubscriptionDefinitionId=definition_id,
            SubscriptionDefinitionVersionId=latest_version
        )

    @ensure_http_success
    def get_function_definition_version(self, definition_id, latest_version):
        return self.client.get_function_definition_version(
            FunctionDefinitionId=definition_id,
            FunctionDefinitionVersionId=latest_version
        )

    @ensure_http_success
    def list_core_definitions(self, **kwargs):
        return self.client.list_core_definitions(**kwargs)

    @ensure_http_success
    def list_device_definitions(self, **kwargs):
        return self.client.list_device_definitions(**kwargs)

    @ensure_http_success
    def list_logger_definitions(self, **kwargs):
        return self.client.list_logger_definitions(**kwargs)

    @ensure_http_success
    def list_subscription_definitions(self, **kwargs):
        return self.client.list_subscription_definitions(**kwargs)

    @ensure_http_success
    def list_function_definitions(self, **kwargs):
        return self.client.list_function_definitions(**kwargs)
