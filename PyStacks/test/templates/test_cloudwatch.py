import unittest

from PyStacks.PyStacks.template import templateCF


class TestTemplate(unittest.TestCase):

    def test_templateCF_CloudWatch(self):
        resources = {
            'cloudwatch': {
                'simplealarm': {
                    'comparisonoperator': 'GreaterThanThreshold',
                    'evalationperiods': 5,
                    'metricname': 'testmetric',
                    'namespace': 'testnamespace',
                    'period': '60',
                    'statistic': 'Sum',
                    'threshold': '10'
                },
                'complexalarm': {
                    'actionsenabled': True,
                    'alarmactions': [
                        'alarmaction1',
                        'alarmaction2'
                    ],
                    'alarmdescription': 'testalarmdescription',
                    'alarmname': 'testalarmname',
                    'comparisonoperator': 'GreaterThanThreshold',
                    'dimensions': {
                        'Currency': 'USD',
                        'InstanceId': 'i-12345678'
                    },
                    'evalationperiods': 5,
                    'insufficientdataactions': [
                        'insuffdataaction1',
                        'insuffdataaction2'
                    ],
                    'metricname': 'testmetric',
                    'namespace': 'testnamespace',
                    'okactions': [
                        'okaction1',
                        'okaction2'
                    ],
                    'period': '60',
                    'statistic': 'Sum',
                    'threshold': '10',
                    'unit': 'Bytes'
                }
            }
        }
        expected = {
            'simplealarm': {
                'Type': 'AWS::CloudWatch::Alarm',
                'Properties': {
                    'ComparisonOperator': 'GreaterThanThreshold',
                    'EvaluationPeriods': '5',
                    'MetricName': 'testmetric',
                    'Namespace': 'testnamespace',
                    'Period': '60',
                    'Statistic': 'Sum',
                    'Threshold': '10'
                }
            },
            'complexalarm': {
                'Type': 'AWS::CloudWatch::Alarm',
                'Properties': {
                    'ActionsEnabled': 'true',
                    'AlarmActions': [
                        {
                            "Ref": "alarmaction1"
                        },
                        {
                            "Ref": "alarmaction2"
                        }
                    ],
                    'AlarmDescription': 'testalarmdescription',
                    'AlarmName': 'testalarmname',
                    'ComparisonOperator': 'GreaterThanThreshold',
                    'Dimensions': [
                        {
                            'Name': 'InstanceId',
                            'Value': 'i-12345678'
                        },
                        {
                            'Name': 'Currency',
                            'Value': 'USD'
                        }
                    ],
                    'InsufficientDataActions': [
                        'insuffdataaction1',
                        'insuffdataaction2'
                    ],
                    'MetricName': 'testmetric',
                    'Namespace': 'testnamespace',
                    'OKActions': [
                        'okaction1',
                        'okaction2'
                    ],
                    'EvaluationPeriods': '5',
                    'Period': '60',
                    'Statistic': 'Sum',
                    'Threshold': '10',
                    'Unit': 'Bytes'
                }
            }
        }

        actual = templateCF(resources, 'resources')
        self.assertDictEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
