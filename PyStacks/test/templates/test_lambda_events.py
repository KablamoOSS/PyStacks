import unittest

from PyStacks.PyStacks.template import templateCF


class TestTemplate(unittest.TestCase):

    def test_templateCF_GenericLambdaEvents(self):
        resources = {
            'lambda_events': {
                'testLambdaEvent': {
                    'batchsize': '100',
                    'enabled': 'true',
                    'sourcearn': 'someArn',
                    'lambda': 'lambdaFunctionName',
                    'startingposition': "LATEST",
                },
            },
        }
        expected = {
            "testLambdaEvent": {
                "Type": "AWS::Lambda::EventSourceMapping",
                "Properties": {
                    "BatchSize": "100",
                    "Enabled": "true",
                    "EventSourceArn": "someArn",
                    "FunctionName": "lambdaFunctionName",
                    "StartingPosition": "LATEST"
                }
            }
        }

        actual = templateCF(resources, 'resources')
        self.maxDiff = None
        self.assertDictEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
