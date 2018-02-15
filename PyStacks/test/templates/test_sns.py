import unittest

from PyStacks.PyStacks.template import templateCF


class TestTemplate(unittest.TestCase):

    def test_templateCF_SNSTopicPolicy(self):
        resources = {
            'snstopic': {
                'test1': {
                    'policy': 'snsTopicPolicyDocument1',
                    'topics': [
                        'topic1',
                        'topic2'
                    ]
                }
            }
        }
        expected = {
            'test1': {
                'Type': 'AWS::SNS::TopicPolicy',
                'Properties': {
                    'PolicyDocument': 'snsTopicPolicyDocument1',
                    'Topics': [{
                        'Fn::ImportValue': {
                            'Fn::Sub': [
                                '${SNSStack}-SNS-topic1', {
                                    'SNSStack': {
                                        'Ref': 'SNSStack'
                                    }
                                }
                            ]
                        }
                    }, {
                        'Fn::ImportValue': {
                            'Fn::Sub': [
                                '${SNSStack}-SNS-topic2', {
                                    'SNSStack': {
                                        'Ref': 'SNSStack'
                                    }
                                }
                            ]
                        }
                    }]
                }
            }
        }

        self.maxDiff = None
        actual = templateCF(resources, 'resources')
        self.assertDictEqual(actual, expected)

    def test_templateCF_SNS(self):
        resources = {
            'sns': {
                'test1': {
                    'displayname': 'displayNameTest1',
                    'subscription': [{
                        'endpointtype': 'export',
                        'protocol': 'lambda',
                        'value': 'valueTest1-1'
                    }],
                    'topicname': 'topicNameTest1'
                },
                'test2': {
                    'displayname': 'displayNameTest2',
                    'subscription': [{
                        'endpointtype': 'export',
                        'protocol': 'lambda',
                        'value': 'valueTest2-1'
                    }, {
                        'endpointtype': 'export',
                        'protocol': 'sqs',
                        'value': 'valueTest2-2'
                    }, {
                        'endpointtype': 'notused',
                        'protocol': 'sqs',
                        'value': 'valueTest2-3'
                    }],
                    'topicname': 'topicNameTest2'
                }
            }
        }
        expected = {
            'test1': {
                'Type': 'AWS::SNS::Topic',
                'Properties': {
                    'DisplayName': 'displayNameTest1',
                    'Subscription': [{
                        'Endpoint': {
                            'Fn::ImportValue': {
                                'Fn::Sub': [
                                    '${LambdaStack}-Lambda-valueTest1-1-ARN',
                                    {
                                        'LambdaStack': {
                                            'Ref': 'LambdaStack'
                                        }
                                    }
                                ]
                            }
                        },
                        'Protocol': 'lambda'
                    }],
                    'TopicName': 'topicNameTest1'
                }
            },
            'test2': {
                'Type': 'AWS::SNS::Topic',
                'Properties': {
                    'DisplayName': 'displayNameTest2',
                    'Subscription': [{
                        'Endpoint': {
                            'Fn::ImportValue': {
                                'Fn::Sub': [
                                    '${LambdaStack}-Lambda-valueTest2-1-ARN',
                                    {
                                        'LambdaStack': {
                                            'Ref': 'LambdaStack'
                                        }
                                    }
                                ]
                            }
                        },
                        'Protocol': 'lambda'
                    }, {
                        'Endpoint': {
                            'Fn::ImportValue': {
                                'Fn::Sub': [
                                    '${SQSStack}-SQS-valueTest2-2-ARN',
                                    {
                                        'SQSStack': {
                                            'Ref': 'SQSStack'
                                        }
                                    }
                                ]
                            }
                        },
                        'Protocol': 'sqs'
                    }, {
                        'Endpoint': {
                            'Ref': 'valueTest2-3'
                        },
                        'Protocol': 'sqs'
                    }],
                    'TopicName': 'topicNameTest2'
                }
            }
        }

        self.maxDiff = None
        actual = templateCF(resources, 'resources')
        self.assertDictEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
