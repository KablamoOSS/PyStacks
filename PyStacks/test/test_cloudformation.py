import unittest
import json

from mock import MagicMock

from botocore.exceptions import ClientError

from PyStacks.PyStacks.cloudformation import stack


class TestCloudFormationSetup(unittest.TestCase):
    def setUp(self):
        self.mocksession = MagicMock()
        self.mockcfClient = MagicMock()
        self.mockcfStack = MagicMock()
        self.getStackStatus = MagicMock()

        self.mocksession.client.return_value = self.mockcfClient
        self.mocksession.resource.return_value = self.mockcfStack
        self.mocksession.getStackStatus = self.getStackStatus

        self.cloudformation = stack(self.mocksession)


class TestCloudFormation(TestCloudFormationSetup):

    def test_validate_invalid_session(self):
        with self.assertRaises(AttributeError):
            stack(None)

    def test_validate_template_with_none(self):
        self.mocksession.resource.return_value = self.mockcfStack
        self.mockcfClient.validate_template.return_value = False

        result = self.cloudformation.validateTemplate(cftemplate=None)

        self.assertFalse(result)
        self.mockcfClient.validate_template.assert_called_with(
            TemplateBody='null')

    def test_validate_template_with_array_is_jsoned(self):
        self.mockcfClient.validate_template.return_value = True

        result = self.cloudformation.validateTemplate(cftemplate=json.dumps(
            [1, 2, 3]))

        self.assertTrue(result)
        self.mockcfClient.validate_template.assert_called_with(
            TemplateBody='"[1, 2, 3]"')

    def test_describe_exports(self):
        mockstackExport = MagicMock()

        self.mockcfStack.Stack.return_value = mockstackExport
        self.cloudformation.describeExports('myStack')

        self.mockcfStack.Stack.assert_called_with('myStack')

    def test_create_stack_check_params(self):
        self.cloudformation.createStack(
            cftemplate=None, stackname='MyLittleStack')

        self.mockcfClient.create_stack.assert_called_with(
            StackName='MyLittleStack',
            TimeoutInMinutes=180,
            OnFailure='ROLLBACK',
            TemplateBody='null', )

    def test_create_stack_check_params_dict(self):
        self.cloudformation.createStack(
            cftemplate={'Terry': 'WasHere'}, stackname='MyLittleStack')

        self.mockcfClient.create_stack.assert_called_with(
            StackName='MyLittleStack',
            TimeoutInMinutes=180,
            OnFailure='ROLLBACK',
            TemplateBody='{"Terry": "WasHere"}', )

    def test_create_stack_check_override_params(self):
        self.cloudformation.createStack(
            cftemplate=None,
            stackname='MyLittleStack',
            timeout=60,
            onfailure='SOMETHING')

        self.mockcfClient.create_stack.assert_called_with(
            StackName='MyLittleStack',
            TimeoutInMinutes=60,
            OnFailure='SOMETHING',
            TemplateBody='null', )

    def test_create_stack_s3_stack(self):
        self.cloudformation.createStack(
            cftemplate='https://s3-ap-southeast-2.amazonaws.com/test/Stack.json',
            stackname='MyLittleStack')

        self.mockcfClient.create_stack.assert_called_with(
            StackName='MyLittleStack',
            TimeoutInMinutes=180,
            OnFailure='ROLLBACK',
            TemplateURL='https://s3-ap-southeast-2.amazonaws.com/test/Stack.json', )

    def test_create_stack_iam_capable(self):
        self.cloudformation.createStack(
            cftemplate='null',
            stackname='MyLittleStack',
            onfailure='ROLLBACK',
            iamcapable=True)

        self.mockcfClient.create_stack.assert_called_with(
            StackName='MyLittleStack',
            TimeoutInMinutes=180,
            OnFailure='ROLLBACK',
            TemplateBody='"null"',
            Capabilities=True, )

    def test_create_stack_iam_capable_dict(self):
        self.cloudformation.createStack(
            cftemplate={'Terry': 'WasHere'},
            stackname='MyLittleStack',
            onfailure='ROLLBACK',
            iamcapable=True)

        self.mockcfClient.create_stack.assert_called_with(
            StackName='MyLittleStack',
            TimeoutInMinutes=180,
            OnFailure='ROLLBACK',
            TemplateBody='{"Terry": "WasHere"}',
            Capabilities=True, )

    def test_create_stack_iam_capable_s3(self):
        self.cloudformation.createStack(
            cftemplate='https://s3-ap-southeast-2.amazonaws.com/test/Stack.json',
            stackname='MyLittleStack',
            onfailure='ROLLBACK',
            iamcapable=True)

        self.mockcfClient.create_stack.assert_called_with(
            StackName='MyLittleStack',
            TimeoutInMinutes=180,
            OnFailure='ROLLBACK',
            TemplateURL='https://s3-ap-southeast-2.amazonaws.com/test/Stack.json',
            Capabilities=True, )

    def test_delete_stack(self):
        self.cloudformation.deleteStack(stackname='MyLittleStack')

        self.mockcfClient.delete_stack.assert_called_with(
            StackName='MyLittleStack', )

    def test_update_stack(self):
        self.cloudformation.updateStack(
            cftemplate=None, stackname='MyLittleStack')

        self.mockcfClient.update_stack.assert_called_with(
            StackName='MyLittleStack',
            TemplateBody='null', )

    def test_update_stack_dict(self):
        self.cloudformation.updateStack(
            cftemplate={'Terry': 'WasHere'}, stackname='MyLittleStack')

        self.mockcfClient.update_stack.assert_called_with(
            StackName='MyLittleStack',
            TemplateBody='{"Terry": "WasHere"}', )

    def test_update_stack_s3(self):
        self.cloudformation.updateStack(
            cftemplate='https://s3-ap-southeast-2.amazonaws.com/test/Stack.json',
            stackname='MyLittleStack')

        self.mockcfClient.update_stack.assert_called_with(
            StackName='MyLittleStack',
            TemplateURL='https://s3-ap-southeast-2.amazonaws.com/test/Stack.json', )

    def test_update_stack_iam_capable(self):
        self.cloudformation.updateStack(
            cftemplate=None, stackname='MyLittleStack', iamcapable=True)

        self.mockcfClient.update_stack.assert_called_with(
            StackName='MyLittleStack', TemplateBody='null', Capabilities=True)

    def test_update_stack_iam_capable_dict(self):
        self.cloudformation.updateStack(
            cftemplate={'Terry': 'WasHere'},
            stackname='MyLittleStack',
            iamcapable=True)

        self.mockcfClient.update_stack.assert_called_with(
            StackName='MyLittleStack',
            TemplateBody='{"Terry": "WasHere"}',
            Capabilities=True)

    def test_update_stack_iam_capable_s3(self):
        self.cloudformation.updateStack(
            cftemplate='https://s3-ap-southeast-2.amazonaws.com/test/Stack.json',
            stackname='MyLittleStack',
            iamcapable=True)

        self.mockcfClient.update_stack.assert_called_with(
            StackName='MyLittleStack',
            TemplateURL='https://s3-ap-southeast-2.amazonaws.com/test/Stack.json',
            Capabilities=True)

    def test_describeStack(self):
        self.mockcfClient.describe_stacks.return_value = {
            'Stacks': [{
                'StackStatus': 'MyLittleStatus'
            }]
        }

        result = self.cloudformation.describeStack(stackname='MyLittleStack')

        self.assertEqual('MyLittleStatus', result)
        self.mockcfClient.describe_stacks.assert_called_with(
            StackName='MyLittleStack', )

    def test_describeStack_clientError(self):
        self.mockcfClient.describe_stacks.return_value = {
            'Stacks': [{
                'StackStatus': 'MyLittleStatus'
            }]
        }
        self.mockcfClient.describe_stacks.side_effect = ClientError(
            {
                'Error': {
                    'Code': '100',
                    'Message': 'MyLittleError',
                }
            },
            'op_name'
        )

        with self.assertRaises(Exception):
            self.cloudformation.describeStack(stackname='MyLittleStack')

    def test_describeStack_clientError_not_exist(self):
        self.mockcfClient.describe_stacks.return_value = {
            'Stacks': [{
                'StackStatus': 'MyLittleStatus'
            }]
        }
        self.mockcfClient.describe_stacks.side_effect = ClientError(
            {
                'Error': {
                    'Code': '100',
                    'Message': 'MyLittleError does not exist',
                }
            },
            'op_name'
        )

        result = self.cloudformation.describeStack(stackname='MyLittleStack')

        self.assertEqual(None, result)
        self.mockcfClient.describe_stacks.assert_called_with(
            StackName='MyLittleStack', )

    def test_get_stack_status(self):
        self.mockcfClient.describe_stacks.return_value = {
            'Stacks': [{
                'StackStatus': 'mystackstatus'
            }]
        }

        result = self.cloudformation.getStackStatus(stackname='MyLittleStack')

        self.assertEqual('mystackstatus', result)
        self.mockcfClient.describe_stacks.assert_called_with(
            StackName='MyLittleStack', )

    def test_get_stack_resources(self):
        self.mockcfClient.describe_stack_resources.return_value = {
            'StackResources': 'MyLittleResource'
        }

        result = self.cloudformation.getStackResources(stackname='MyLittleStack')

        self.assertEqual('MyLittleResource', result)
        self.mockcfClient.describe_stack_resources.assert_called_with(
            StackName='MyLittleStack', )

    def test_stackStatusChecker(self):

        # 'INVALID CF STATUS': 0,
        self.mockcfClient.describe_stacks.return_value = {
            'Stacks': [{
                'StackStatus': 'Im not your real status'
            }]
        }

        stati = self.cloudformation.stackStatusChecker(
            stackname='MyLittleStack'
        )
        self.assertEqual(stati[0], 'INVALID CF STATUS')
        self.assertEqual(stati[1], 'Im not your real status')

        # 'CREATE_COMPLETE': 0,
        self.mockcfClient.describe_stacks.return_value = {
            'Stacks': [{
                'StackStatus': 'CREATE_COMPLETE'
            }]
        }

        stati = self.cloudformation.stackStatusChecker(
            stackname='MyLittleStack'
        )
        self.assertEqual(stati[0], 0)
        self.assertEqual(stati[1], 'CREATE_COMPLETE')

        # 'CREATE_IN_PROGRESS': 2,
        self.mockcfClient.describe_stacks.return_value = {
            'Stacks': [{
                'StackStatus': 'CREATE_IN_PROGRESS'
            }]
        }

        stati = self.cloudformation.stackStatusChecker(
            stackname='MyLittleStack'
        )
        self.assertEqual(stati[0], 2)
        self.assertEqual(stati[1], 'CREATE_IN_PROGRESS')

        # 'CREATE_FAILED': 1,
        self.mockcfClient.describe_stacks.return_value = {
            'Stacks': [{
                'StackStatus': 'CREATE_FAILED'
            }]
        }

        stati = self.cloudformation.stackStatusChecker(
            stackname='MyLittleStack'
        )
        self.assertEqual(stati[0], 1)
        self.assertEqual(stati[1], 'CREATE_FAILED')

        # 'DELETE_FAILED': 1,
        self.mockcfClient.describe_stacks.return_value = {
            'Stacks': [{
                'StackStatus': 'DELETE_FAILED'
            }]
        }

        stati = self.cloudformation.stackStatusChecker(
            stackname='MyLittleStack'
        )
        self.assertEqual(stati[0], 1)
        self.assertEqual(stati[1], 'DELETE_FAILED')

        # 'DELETE_IN_PROGRESS': 2,
        self.mockcfClient.describe_stacks.return_value = {
            'Stacks': [{
                'StackStatus': 'DELETE_IN_PROGRESS'
            }]
        }

        stati = self.cloudformation.stackStatusChecker(
            stackname='MyLittleStack'
        )
        self.assertEqual(stati[0], 2)
        self.assertEqual(stati[1], 'DELETE_IN_PROGRESS')

        # 'REVIEW_IN_PROGRESS': 2,
        self.mockcfClient.describe_stacks.return_value = {
            'Stacks': [{
                'StackStatus': 'REVIEW_IN_PROGRESS'
            }]
        }

        stati = self.cloudformation.stackStatusChecker(
            stackname='MyLittleStack'
        )
        self.assertEqual(stati[0], 2)
        self.assertEqual(stati[1], 'REVIEW_IN_PROGRESS')

        # 'ROLLBACK_COMPLETE': 1,
        self.mockcfClient.describe_stacks.return_value = {
            'Stacks': [{
                'StackStatus': 'ROLLBACK_COMPLETE'
            }]
        }

        stati = self.cloudformation.stackStatusChecker(
            stackname='MyLittleStack'
        )
        self.assertEqual(stati[0], 1)
        self.assertEqual(stati[1], 'ROLLBACK_COMPLETE')

        # 'ROLLBACK_FAILED': 1,
        self.mockcfClient.describe_stacks.return_value = {
            'Stacks': [{
                'StackStatus': 'ROLLBACK_FAILED'
            }]
        }

        stati = self.cloudformation.stackStatusChecker(
            stackname='MyLittleStack'
        )
        self.assertEqual(stati[0], 1)
        self.assertEqual(stati[1], 'ROLLBACK_FAILED')

        # 'ROLLBACK_IN_PROGRESS': 2,
        self.mockcfClient.describe_stacks.return_value = {
            'Stacks': [{
                'StackStatus': 'ROLLBACK_IN_PROGRESS'
            }]
        }

        stati = self.cloudformation.stackStatusChecker(
            stackname='MyLittleStack'
        )
        self.assertEqual(stati[0], 2)
        self.assertEqual(stati[1], 'ROLLBACK_IN_PROGRESS')

        # 'UPDATE_COMPLETE': 0,
        self.mockcfClient.describe_stacks.return_value = {
            'Stacks': [{
                'StackStatus': 'UPDATE_COMPLETE'
            }]
        }

        stati = self.cloudformation.stackStatusChecker(
            stackname='MyLittleStack'
        )
        self.assertEqual(stati[0], 0)
        self.assertEqual(stati[1], 'UPDATE_COMPLETE')

        # 'UPDATE_COMPLETE_CLEANUP_IN_PROGRESS': 2,
        self.mockcfClient.describe_stacks.return_value = {
            'Stacks': [{
                'StackStatus': 'UPDATE_COMPLETE_CLEANUP_IN_PROGRESS'
            }]
        }

        stati = self.cloudformation.stackStatusChecker(
            stackname='MyLittleStack'
        )
        self.assertEqual(stati[0], 2)
        self.assertEqual(stati[1], 'UPDATE_COMPLETE_CLEANUP_IN_PROGRESS')

        # 'UPDATE_IN_PROGRESS': 2,
        self.mockcfClient.describe_stacks.return_value = {
            'Stacks': [{
                'StackStatus': 'UPDATE_IN_PROGRESS'
            }]
        }

        stati = self.cloudformation.stackStatusChecker(
            stackname='MyLittleStack'
        )
        self.assertEqual(stati[0], 2)
        self.assertEqual(stati[1], 'UPDATE_IN_PROGRESS')

        # 'UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS': 2,
        self.mockcfClient.describe_stacks.return_value = {
            'Stacks': [{
                'StackStatus': 'UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS'
            }]
        }

        stati = self.cloudformation.stackStatusChecker(
            stackname='MyLittleStack'
        )
        self.assertEqual(stati[0], 2)
        self.assertEqual(stati[1], 'UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS')

        # 'UPDATE_ROLLBACK_FAILED': 1,
        self.mockcfClient.describe_stacks.return_value = {
            'Stacks': [{
                'StackStatus': 'UPDATE_ROLLBACK_FAILED'
            }]
        }

        stati = self.cloudformation.stackStatusChecker(
            stackname='MyLittleStack'
        )
        self.assertEqual(stati[0], 1)
        self.assertEqual(stati[1], 'UPDATE_ROLLBACK_FAILED')

        # 'UPDATE_ROLLBACK_IN_PROGRESS': 2,
        self.mockcfClient.describe_stacks.return_value = {
            'Stacks': [{
                'StackStatus': 'UPDATE_ROLLBACK_IN_PROGRESS'
            }]
        }

        stati = self.cloudformation.stackStatusChecker(
            stackname='MyLittleStack'
        )
        self.assertEqual(stati[0], 2)
        self.assertEqual(stati[1], 'UPDATE_ROLLBACK_IN_PROGRESS')

    def test_stackStatusChecker_invalid(self):
        mockgetstatus = MagicMock()
        mockgetstatus.return_value = 'I am invalid'
        self.getStackStatus = mockgetstatus

        stati, status = self.cloudformation.stackStatusChecker(
            stackname='MyLittleStack'
        )
        self.assertEqual(stati, 'INVALID CF STATUS')

    def test_status_poller(self):
        mockstatuschecker = MagicMock()
        mockstatuschecker.return_value = 0, 'UPDATE_COMPLETE'

        self.cloudformation.stackStatusChecker = mockstatuschecker

        state, status = self.cloudformation.statusPoller(
            stackname='MyLittleStack', sleeptime=0.001, output=False)

        self.assertEqual(state, 0)
        self.assertEqual(status, 'UPDATE_COMPLETE')

    def test_status_poller_count(self):
        mockstatuschecker = MagicMock()
        mockstatuschecker.return_value = 2, 'CREATE_IN_PROGRESS'

        self.cloudformation.stackStatusChecker = mockstatuschecker

        state, status = self.cloudformation.statusPoller(
            stackname='MyLittleStack', sleeptime=0.001, output=False)

        self.assertEqual(state, 2)
        self.assertEqual(status, 'CREATE_IN_PROGRESS')

    def test_status_poller_output(self):
        mockstatuschecker = MagicMock()
        mockstatuschecker.return_value = 2, 'CREATE_IN_PROGRESS'

        self.cloudformation.stackStatusChecker = mockstatuschecker

        state, status = self.cloudformation.statusPoller(
            stackname='MyLittleStack', sleeptime=0.001, output=False)

        self.assertEqual(state, 2)
        self.assertEqual(status, 'CREATE_IN_PROGRESS')

    def test_status_poller_exception(self):
        mockstatuschecker = MagicMock()
        mockstatuschecker.side_effect = Exception('MyLittleFailure')

        self.cloudformation.stackStatusChecker = mockstatuschecker

        with self.assertRaises(Exception):
            state, status = self.cloudformation.statusPoller(
                stackname='MyLittleStack', sleeptime=0.001, output=False)

    def test_status_poller_exception_delete_complete(self):
        mockstatuschecker = MagicMock()
        mockstatuschecker.side_effect = Exception('Success does not exist')
        mockstatuschecker.return_value = 2, 'SOMETHING'

        self.cloudformation.stackStatusChecker = mockstatuschecker

        state, status = self.cloudformation.statusPoller(
            stackname='MyLittleStack', sleeptime=0.001, output=False)

        self.assertEqual(state, 0)
        self.assertEqual(status, 'DELETE_COMPLETE')


if __name__ == '__main__':
    unittest.main()
