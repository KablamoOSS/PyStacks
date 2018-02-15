import unittest

from PyStacks.PyStacks.template import templateCF

API_NAME = 'TestAPI'

DEFAULT_API = {
    'Type': 'AWS::ApiGateway::RestApi',
    'Properties': {
        'Name': API_NAME,
    },
}

DEFAULT_API_DEPLOYMENT = {
    'Type': 'AWS::ApiGateway::Deployment',
    'Properties': {
        'RestApiId': {'Ref': 'testapi'},
    },
}


class TestTemplate(unittest.TestCase):

    def test_templateCF_RestAPI(self):
        resources = {
            'apigateway': {
                'testapi': {
                    'name': API_NAME,
                    'description': 'test description',
                    'failOnWarnings': True,
                    'deployments': {
                        'deployment': {},
                    },
                }
            }
        }
        expected = {
            'testapi': {
                'Type': 'AWS::ApiGateway::RestApi',
                'Properties': {
                    'Description': 'test description',
                    'FailOnWarnings': 'true',
                    'Name': API_NAME,
                },
            },
            'deployment': DEFAULT_API_DEPLOYMENT,
        }
        actual = templateCF(resources, 'resources')
        self.assertDictEqual(actual, expected)

    def test_templateCF_Methods(self):
        method = {
            'apiKeyRequired': True,
            'authorizationType': 'NONE',
            'authorizerId': 'authID',
            'httpMethod': 'ANY',
            'resource': 'testResource',
        }
        resources = {
            'apigateway': {
                'testapi': {
                    'name': API_NAME,
                    'methods': {
                        'testGetMethod': method,
                    },
                    'deployments': {
                        'deployment': {},
                    },
                }
            }
        }
        expected = {
            'testapi': DEFAULT_API,
            'deployment': DEFAULT_API_DEPLOYMENT,
            'testGetMethod': {
                'Type': "AWS::ApiGateway::Method",
                'Properties': {
                    'ApiKeyRequired': 'true',
                    'AuthorizationType': method['authorizationType'],
                    'AuthorizerId': method['authorizerId'],
                    'HttpMethod': method['httpMethod'],
                    'ResourceId': {'Ref': method['resource']},
                    'RestApiId': {'Ref': 'testapi'},
                }
            }
        }
        actual = templateCF(resources, 'resources')
        self.assertDictEqual(actual, expected)

    def test_templateCF_LambdaIntegration(self):
        integration = {
            'cacheKeyParameters': ['key1', 'key2'],
            'cacheNamespace': 'cacheNamespace',
            'credentials': 'credentials',
            'integrationHttpMethod': 'GET',
            'passthroughBehavior': 'passThrough',
            'type': 'AWS',
            'lambda': 'testLambda',
        }
        resources = {
            'apigateway': {
                'testapi': {
                    'name': API_NAME,
                    'methods': {
                        'testGetMethod': {
                            'integration': integration,
                        },
                    },
                    'deployments': {
                        'deployment': {},
                    },
                }
            }
        }
        expected = {
            'testapi': DEFAULT_API,
            'deployment': DEFAULT_API_DEPLOYMENT,
            'testGetMethod': {
                'Type': "AWS::ApiGateway::Method",
                'Properties': {
                    'ResourceId': {'Fn::GetAtt': ['testapi', 'RootResourceId']},
                    'RestApiId': {'Ref': 'testapi'},
                    'Integration': {
                        'CacheKeyParameters': integration['cacheKeyParameters'],
                        'CacheNamespace': integration['cacheNamespace'],
                        'IntegrationHttpMethod': integration['integrationHttpMethod'],
                        'PassthroughBehavior': integration['passthroughBehavior'],
                        'Type': integration['type'],
                        'Uri': {'Fn::Join': [
                            '',
                            [
                                'arn:aws:apigateway:',
                                {'Ref': 'AWS::Region'},
                                ':lambda:path/2015-03-31/functions/',
                                {'Fn::GetAtt': [integration['lambda'], 'Arn']},
                                '/invocations',
                            ],
                        ]},
                        'Credentials': integration['credentials'],
                    },
                }
            }
        }
        actual = templateCF(resources, 'resources')
        self.assertDictEqual(actual, expected)

    def test_templateCF_Outputs(self):
        resources = {
            'apigateway': {
                'testapi': {},
            }
        }
        expected = {
            'testapi': {
                'Export': {'Name': {'Fn::Sub': '${AWS::StackName}-API-testapi'}},
                'Value': {'Ref': 'testapi'},
                'Description': 'testapi API gateway',
            },
        }
        actual = templateCF(resources, 'outputs')
        self.assertDictEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
