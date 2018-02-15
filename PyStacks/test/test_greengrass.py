import unittest
from mock import MagicMock

from PyStacks.PyStacks.greengrass import GreengrassAPI


class TestGreengrass(unittest.TestCase):

    def setUp(self):
        self.mocksession = MagicMock()
        self.mockggclient = MagicMock()
        self.mocksession.client.return_value = self.mockggclient
        self.gg = GreengrassAPI(self.mocksession)

    def test_ensure_required_config(self):
        """Require the correct config form"""
        pass

    def test_no_devices(self):
        """Allow group creation without devices."""
        pass

    def test_no_functions(self):
        """Allow group creation without functions."""
        pass

    def test_no_subscriptions(self):
        """Allow group creation without subscriptions."""
        pass

    def test_no_logs(self):
        """Allow group creation without logs."""
        pass

    def test_create_core_definition_success(self):
        self.mockggclient.create_core_definition.return_value = {
            'Arn': 'arn123',
            'CreationTimestamp': '10-10-2012',
            'Id': 'unique_id',
            'LastUpdatedTimestamp': '10-11-2013',
            'LatestVersion': 'object here',
            'LatestVersionArn': 'arn234',
            'Name': 'gg-test',
            "ResponseMetadata": {
                "RetryAttempts": 0,
                "HTTPStatusCode": 201,
            },
        }
        call_params = {
            'name': 'gg-test'
        }
        result = self.gg.create_core_definition(
            name=call_params['name']
        )
        assert result == self.mockggclient.create_core_definition.return_value

        self.mockggclient.create_core_definition.assert_called_with(
            Name=call_params['name']
        )

    def test_create_core_definition_fail(self):
        pass

    def test_update_core_definition(self):
        self.mockggclient.update_core_definition.return_value = {
            "ResponseMetadata": {
                "RetryAttempts": 0,
                "HTTPStatusCode": 201,
            },
        }
        call_params = {
            'coreid': 'test-core',
            'name': 'gg-test'
        }
        result = self.gg.update_core_definition(
            coreid=call_params['coreid'],
            name=call_params['name']
        )
        assert result == self.mockggclient.update_core_definition.return_value

        self.mockggclient.update_core_definition.assert_called_with(
            CoreDefinitionId=call_params['coreid'],
            Name=call_params['name']
        )

    def test_delete_core_definition(self):
        self.mockggclient.delete_core_definition.return_value = {
            "ResponseMetadata": {
                "RetryAttempts": 0,
                "HTTPStatusCode": 201,
            },
        }
        coreid = 'test-core'

        result = self.gg.delete_core_definition(coreid)
        assert result == self.mockggclient.delete_core_definition.return_value

        self.mockggclient.delete_core_definition.assert_called_with(
            CoreDefinitionId=coreid
        )

    def test_create_device_definition(self):
        self.mockggclient.create_device_definition.return_value = {
            'Arn': 'arn657',
            'CreationTimestamp': '10-10-2014',
            'Id': 'unique_id',
            'LastUpdatedTimestamp': '10-11-2015',
            'LatestVersion': 'object here',
            'LatestVersionArn': 'arn23445',
            'Name': 'gg-device-test',
            "ResponseMetadata": {
                "RetryAttempts": 0,
                "HTTPStatusCode": 201,
            },
        }
        call_params = {
            'token': 'token123',
            'version': {'Devices': [{}]},
            'name': 'gg-device-test'
        }
        result = self.gg.create_device_definition(
            token=call_params['token'],
            version=call_params['version'],
            name=call_params['name']
        )
        assert result == self.mockggclient.create_device_definition.return_value

        self.mockggclient.create_device_definition.assert_called_with(
            AmznClientToken=call_params['token'],
            InitialVersion=call_params['version'],
            Name=call_params['name']
        )

    def test_update_device_definition(self):
        self.mockggclient.update_device_definition.return_value = {
            "ResponseMetadata": {
                "RetryAttempts": 0,
                "HTTPStatusCode": 201,
            },
        }
        call_params = {
            'deviceid': 'test-device',
            'name': 'gg-test'
        }
        result = self.gg.update_device_definition(
            deviceid=call_params['deviceid'],
            name=call_params['name']
        )
        assert result == self.mockggclient.update_device_definition.return_value

        self.mockggclient.update_device_definition.assert_called_with(
            DeviceDefinitionId=call_params['deviceid'],
            Name=call_params['name']
        )

    def test_delete_device_definition(self):
        self.mockggclient.delete_device_definition.return_value = {
            "ResponseMetadata": {
                "RetryAttempts": 0,
                "HTTPStatusCode": 201,
            },
        }
        deviceid = 'test-device'

        result = self.gg.delete_device_definition(deviceid)
        assert result == self.mockggclient.delete_device_definition.return_value

        self.mockggclient.delete_device_definition.assert_called_with(
            DeviceDefinitionId=deviceid
        )

    def test_create_function_definition(self):
        self.mockggclient.create_function_definition.return_value = {
            'Arn': 'arn657',
            'CreationTimestamp': '12-09-2014',
            'Id': 'unique_id',
            'LastUpdatedTimestamp': '10-11-2015',
            'LatestVersion': 'object here',
            'LatestVersionArn': 'arn23445',
            "ResponseMetadata": {
                "RetryAttempts": 0,
                "HTTPStatusCode": 201,
            },
            'Name': 'gg-function-test',
        }
        call_params = {
            'name': 'gg-function-test'
        }
        result = self.gg.create_function_definition(
            name=call_params['name']
        )
        assert result == self.mockggclient.create_function_definition.return_value

        self.mockggclient.create_function_definition.assert_called_with(
            Name=call_params['name']
        )

    def test_update_function_definition(self):
        self.mockggclient.update_function_definition.return_value = {
            "ResponseMetadata": {
                "RetryAttempts": 0,
                "HTTPStatusCode": 201,
            },
        }
        call_params = {
            'functionid': 'test-function',
            'name': 'gg-test'
        }
        result = self.gg.update_function_definition(
            functionid=call_params['functionid'],
            name=call_params['name']
        )
        assert result == self.mockggclient.update_function_definition.return_value

        self.mockggclient.update_function_definition.assert_called_with(
            FunctionDefinitionId=call_params['functionid'],
            Name=call_params['name']
        )

    def test_delete_function_definition(self):
        self.mockggclient.delete_function_definition.return_value = {
            "ResponseMetadata": {
                "RetryAttempts": 0,
                "HTTPStatusCode": 201,
            },
        }
        functionid = 'test-function'

        result = self.gg.delete_function_definition(functionid)
        assert result == self.mockggclient.delete_function_definition.return_value

        self.mockggclient.delete_function_definition.assert_called_with(
            FunctionDefinitionId=functionid
        )

    def test_create_group_success(self):
        self.mockggclient.create_group.return_value = {
            'Arn': 'arn657',
            'CreationTimestamp': '12-09-2014',
            'Id': 'unique_id',
            'LastUpdatedTimestamp': '10-11-2015',
            'LatestVersion': 'object here',
            'LatestVersionArn': 'arn23445',
            'Name': 'gg-group-test',
            "ResponseMetadata": {
                "RetryAttempts": 0,
                "HTTPStatusCode": 201,
            },
        }

        call_params = {'name': 'gg-group-test'}

        result = self.gg.create_group(**call_params)

        assert result == self.mockggclient.create_group.return_value

        self.mockggclient.create_group.assert_called_with(
            Name=call_params['name'],
        )

    def test_create_group_fail(self):
        pass

    def test_update_group(self):
        self.mockggclient.update_group.return_value = {
            "ResponseMetadata": {
                "RetryAttempts": 0,
                "HTTPStatusCode": 201,
            },
        }
        call_params = {
            'groupid': 'test-group',
            'name': 'gg-test'
        }
        result = self.gg.update_group(
            groupid=call_params['groupid'],
            name=call_params['name']
        )
        assert result == self.mockggclient.update_group.return_value

        self.mockggclient.update_group.assert_called_with(
            GroupId=call_params['groupid'],
            Name=call_params['name']
        )

    def test_delete_group(self):
        self.mockggclient.delete_group.return_value = {
            "ResponseMetadata": {
                "RetryAttempts": 0,
                "HTTPStatusCode": 201,
            },
        }
        groupid = 'test-group'

        result = self.gg.delete_group(groupid)
        assert result == self.mockggclient.delete_group.return_value

        self.mockggclient.delete_group.assert_called_with(
            GroupId=groupid
        )

    def test_associate_role_to_group(self):
        self.mockggclient.associate_role_to_group.return_value = {
            'AssociatedAt': '2017-01-12-10:17:23',
            "ResponseMetadata": {
                "RetryAttempts": 0,
                "HTTPStatusCode": 201,
            },
        }
        call_params = {
            'groupid': 'test-group',
            'rolearn': 'arn::role::123'
        }
        result = self.gg.associate_role_to_group(
            groupid=call_params['groupid'],
            rolearn=call_params['rolearn']
        )
        assert result == self.mockggclient.associate_role_to_group.return_value

        self.mockggclient.associate_role_to_group.assert_called_with(
            GroupId=call_params['groupid'],
            RoleArn=call_params['rolearn']
        )
