import unittest

from PyStacks.PyStacks.template import templateCF


class TestTemplate(unittest.TestCase):

    def test_templateCF_ConfigRule(self):
        resources = {
            'config_rule': {
                'ConfigPublicPortCheck': {
                    'name': 'ConfigPublicPortCheck',
                    'description': 'Check for Public Ports on Security Groups',
                    'inputparams': {
                        "AllowedPorts": [80, 443]
                    },
                    'maxfrequency': 'One_Hour',
                    'source': {
                        'owner': 'CUSTOM_LAMBDA',
                        'details': {
                            'aws.config': {
                                'frequency': 'One_Hour',
                                'messagetype': 'ScheduledNotification'
                            }
                        },
                        'sourceid': 'configpublicportscheck'
                    }
                }
            }
        }
        expected = {
            "ConfigPublicPortCheck": {
                "Properties": {
                    "ConfigRuleName": "ConfigPublicPortCheck",
                    "Description": "Check for Public Ports on Security Groups",
                    "InputParameters": {
                        "AllowedPorts": [
                            80,
                            443
                        ]
                    },
                    "MaximumExecutionFrequency": "One_Hour",
                    "Source": {
                        "Owner": "CUSTOM_LAMBDA",
                        "SourceDetails": [
                            {
                                "EventSource": "aws.config",
                                "MaximumExecutionFrequency": "One_Hour",
                                "MessageType": "ScheduledNotification"
                            }
                        ],
                        "SourceIdentifier": "configpublicportscheck"
                    }
                },
                "Type": "AWS::Config::ConfigRule"
            }
        }

        actual = templateCF(resources, 'resources')
        self.assertDictEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
