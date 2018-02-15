import unittest

from PyStacks.PyStacks.template import templateCF


class TestTemplate(unittest.TestCase):

    def test_templateCF_NLB(self):
        # self.maxDiff = None
        resources = {
            'nlb': {
                'complextestnlb': {
                    'scheme': 'internet-facing',
                    'subnets': [
                        'subnet1',
                        'subnet2'
                    ],
                    'tags': {
                        'testtagkey1': 'testtagval1',
                        'testtagkey2': 'testtagval2'
                    },
                    'listeners': {
                        'listener1': {
                            'port': '443',
                            'targetgroup': 'http'
                        },
                        'listener2': {
                            'port': '80',
                            'targetgroup': 'http'
                        }
                    },
                    'targetgroups': {
                        'http': {
                            'port': 80,
                            'protocol': 'HTTP',
                            'healthcheckprotocol': 'HTTP',
                            'httpcode': 200,
                            'path': '/',
                            'interval': 30,
                            'timeout': 600,
                            'healthythreshold': 5,
                            'unhealthythreshold': 3,
                            'targets': [
                                {
                                    'refid': 'MyEC2Inst',
                                    'port': 80
                                },
                                {
                                    'id': 'i-12345678901',
                                    'port': 80
                                }
                            ],
                            'targettype': 'instance'
                        }
                    }
                }
            }
        }
        expected = {
            'complextestnlb': {
                'Type': 'AWS::ElasticLoadBalancingV2::LoadBalancer',
                'Properties': {
                    'Name': 'complextestnlb',
                    'Scheme': 'internet-facing',
                    'Subnets': [
                        {
                            "Fn::ImportValue": {
                                "Fn::Sub": [
                                    "${VPCStack}-Subnet-subnet1",
                                    {
                                        "VPCStack": {
                                            "Ref": "VPCStack"
                                        }
                                    }
                                ]
                            }
                        },
                        {
                            "Fn::ImportValue": {
                                "Fn::Sub": [
                                    "${VPCStack}-Subnet-subnet2",
                                    {
                                        "VPCStack": {
                                            "Ref": "VPCStack"
                                        }
                                    }
                                ]
                            }
                        }
                    ],
                    'Tags': [
                        {
                            'Key': 'testtagkey1',
                            'Value': 'testtagval1'
                        },
                        {
                            'Key': 'testtagkey2',
                            'Value': 'testtagval2'
                        }
                    ],
                    'Type': 'network'
                }
            },
            'listener1NlbListener': {
                'Type': 'AWS::ElasticLoadBalancingV2::Listener',
                'Properties': {
                    "DefaultActions": [
                        {
                            "TargetGroupArn": {
                                "Ref": "httpNlbTg"
                            },
                            "Type": "forward"
                        }
                    ],
                    "LoadBalancerArn": {
                        "Ref": "complextestnlb"
                    },
                    "Port": 443,
                    "Protocol": "TCP"
                },
                "DependsOn": [
                    "complextestnlb",
                    "httpNlbTg"
                ]
            },
            'listener2NlbListener': {
                'Type': 'AWS::ElasticLoadBalancingV2::Listener',
                'Properties': {
                    "DefaultActions": [
                        {
                            "TargetGroupArn": {
                                "Ref": "httpNlbTg"
                            },
                            "Type": "forward"
                        }
                    ],
                    "LoadBalancerArn": {
                        "Ref": "complextestnlb"
                    },
                    "Port": 80,
                    "Protocol": "TCP"
                },
                "DependsOn": [
                    "complextestnlb",
                    "httpNlbTg"
                ]
            },
            "httpNlbTg": {
                "Type": "AWS::ElasticLoadBalancingV2::TargetGroup",
                "Properties": {
                    "Name": "http",
                    "Port": 80,
                    "Protocol": "HTTP",
                    "HealthCheckProtocol": "HTTP",
                    "Matcher": {
                        "HttpCode": 200
                    },
                    "HealthCheckPath": "/",
                    "HealthCheckIntervalSeconds": 30,
                    "HealthCheckTimeoutSeconds": 600,
                    "HealthyThresholdCount": 5,
                    "UnhealthyThresholdCount": 3,
                    "Targets": [
                        {
                            "Id": {
                                "Ref": "MyEC2Inst"
                            },
                            "Port": 80
                        },
                        {
                            "Id": "i-12345678901",
                            "Port": 80
                        }
                    ],
                    "TargetType": "instance",
                    "VpcId": {
                        "Fn::ImportValue": {
                            "Fn::Sub": [
                                "${VPCStack}-VPCid",
                                {
                                    "VPCStack": {
                                        "Ref": "VPCStack"
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        }

        actual = templateCF(resources, 'resources')
        self.maxDiff = None
        self.assertDictEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
