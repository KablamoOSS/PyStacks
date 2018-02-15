import unittest

from PyStacks.PyStacks.template import templateCF


class TestTemplate(unittest.TestCase):

    def test_templateCF_SQS(self):
        resources = {
            'sqs': {
                'testQueue': {
                    'name': 'testQueueName',
                    'delay': 20,
                    'maxsize': 10,
                    'retention': 1024,
                    'waittime': 30,
                    'redirectpolicy': {
                        'deadletterqueue': 'abc',
                        'count': 3
                    },
                    'visibilitytimeout': 60
                }
            }
        }
        expected = {
            "testQueue": {
                "Type": "AWS::SQS::Queue",
                "Properties": {
                    "DelaySeconds": "20",
                    "MaximumMessageSize": "10",
                    "MessageRetentionPeriod": "1024",
                    "QueueName": "testQueueName",
                    "ReceiveMessageWaitTimeSeconds": "30",
                    "RedrivePolicy": {
                        "deadLetterTargetArn": {"Fn::GetAtt": ["abc", "Arn"]},
                        "maxReceiveCount": "3"
                    },
                    "VisibilityTimeout": "60"
                }
            }
        }

        actual = templateCF(resources, 'resources')
        self.assertDictEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
