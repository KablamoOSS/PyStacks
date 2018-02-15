import unittest
from dateutil.tz import tzlocal
import datetime
from PyStacks.PyStacks.cloudformation_helpers import load_cf_params_from_string, load_stack_file, display_cf_events


class TestConfig(unittest.TestCase):
    def test_load_cf_params_from_string_value_error(self):
        with self.assertRaises(IndexError):
            load_cf_params_from_string("bar=baz,foo:far")

    def test_load_cf_params_from_string(self):
        actual = load_cf_params_from_string("bar=baz,foo=far")
        self.assertTrue(len(actual) == 2)

    def test_load_cf_params_from_string_previous(self):
        actual = load_cf_params_from_string("bar=baz,foo=UsePreviousValue")
        self.assertTrue(actual == [{'ParameterValue': 'baz', 'ParameterKey': 'bar'}, {'UsePreviousValue': True, 'ParameterKey': 'foo'}])

    def test_load_stack_file_io_error(self):
        with self.assertRaises(IOError):
            load_stack_file("missing_stack_file", "ap-southeast-2")

    def test_display_cf_events(self):
        events = [{u'StackId': 'arn:aws:cloudformation:ap-southeast-2:686755470412:stack/googlechat-gateway-dev/55410590-991f-11e7-ba9a-50fae94fac4a', u'EventId': '901386f0-9cd7-11e7-9320-50fae94fac82', u'ResourceStatus': 'UPDATE_ROLLBACK_COMPLETE', u'ResourceType': 'AWS::CloudFormation::Stack', u'Timestamp': datetime.datetime(2017, 9, 19, 1, 12, 10, 680000, tzinfo=tzlocal()), u'StackName': 'googlechat-gateway-dev', u'PhysicalResourceId': 'arn:aws:cloudformation:ap-southeast-2:686755470412:stack/googlechat-gateway-dev/55410590-991f-11e7-ba9a-50fae94fac4a', u'LogicalResourceId': 'googlechat-gateway-dev'}, {u'StackId': 'arn:aws:cloudformation:ap-southeast-2:686755470412:stack/googlechat-gateway-dev/55410590-991f-11e7-ba9a-50fae94fac4a', u'EventId': 'AGDeployment-e6b6d880-9aba-4dbb-8061-f89a4801f13e', u'ResourceStatus': 'DELETE_COMPLETE', u'ResourceType': 'AWS::ApiGateway::Deployment', u'Timestamp': datetime.datetime(2017, 9, 19, 1, 12, 10, 72000, tzinfo=tzlocal()), u'StackName': 'googlechat-gateway-dev', u'PhysicalResourceId': '7u0xsk', u'LogicalResourceId': 'AGDeployment'}, {u'StackId': 'arn:aws:cloudformation:ap-southeast-2:686755470412:stack/googlechat-gateway-dev/55410590-991f-11e7-ba9a-50fae94fac4a', u'EventId': 'AGDeployment-2ebf0b9b-e526-4240-8a40-732c6d8ce29c', u'ResourceStatus': 'DELETE_IN_PROGRESS', u'ResourceType': 'AWS::ApiGateway::Deployment', u'Timestamp': datetime.datetime(2017, 9, 19, 1, 12, 9, 555000, tzinfo=tzlocal()), u'StackName': 'googlechat-gateway-dev', u'PhysicalResourceId': '7u0xsk', u'LogicalResourceId': 'AGDeployment'}]
        actual = display_cf_events(events)
        self.assertTrue(actual)

    def test_display_cf_events_zero(self):
        actual = display_cf_events([])
        self.assertFalse(actual)


if __name__ == '__main__':
    unittest.main()
