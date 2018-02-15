import unittest

from PyStacks.PyStacks.template import templateCF


class TestTemplate(unittest.TestCase):

    def test_templateCF_ELB(self):
        resources = {
            'elb': {
                'complextestelb': {
                    'instances': [
                        'i-1234567',
                        'i-7654321'
                    ],
                    'scheme': 'internal',
                    'listeners': {
                        'listener1': {
                            'port': '443',
                            'instanceport': '80',
                            'protocol': 'HTTPS',
                            'certid': 'somecertid',
                            'instanceprotocol': 'HTTP'
                        },
                        'listener2': {
                            'port': '22',
                            'instanceport': '22',
                            'protocol': 'TCP',
                            'instanceprotocol': 'TCP'
                        }
                    },
                    'healthcheck': {
                        'target': 'HTTPS:443/',
                        'healthythreshold': '5',
                        'unhealthythreshold': '3',
                        'interval': '30',
                        'timeout': '600'
                    },
                    'sslsecurity': 'refsecpolicy',
                    'subnets': [
                        'subnet1',
                        'subnet2'
                    ],
                    'securitygroupid': 'sg-1234567',
                    'tags': {
                        'testtagkey1': 'testtagval1',
                        'testtagkey2': 'testtagval2'
                    }
                }
            }
        }
        expected = {
            'complextestelb': {
                'Type': 'AWS::ElasticLoadBalancing::LoadBalancer',
                'Properties': {
                    'Instances': [
                        {
                            'Ref': 'i1234567'
                        },
                        {
                            'Ref': 'i7654321'
                        }
                    ],
                    'Scheme': 'internal',
                    'CrossZone': 'true',
                    'ConnectionSettings': {
                        'IdleTimeout': 10
                    },
                    'Listeners': [
                        {
                            'LoadBalancerPort': '443',
                            'InstancePort': '80',
                            'Protocol': 'HTTPS',
                            'SSLCertificateId': 'somecertid',
                            'InstanceProtocol': 'HTTP'
                        },
                        {
                            'LoadBalancerPort': '22',
                            'InstancePort': '22',
                            'Protocol': 'TCP',
                            'InstanceProtocol': 'TCP'
                        }
                    ],
                    'HealthCheck': {
                        'Target': 'HTTPS:443/',
                        'HealthyThreshold': '5',
                        'UnhealthyThreshold': '3',
                        'Interval': '30',
                        'Timeout': '600'
                    },
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
                    'SecurityGroups': [
                        {
                            "Fn::ImportValue": {
                                "Fn::Sub": [
                                    "${SecurityStack}-SecGroup-sg-1234567",
                                    {
                                        "SecurityStack": {
                                            "Ref": "SecurityStack"
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
                    ]
                }
            }
        }

        actual = templateCF(resources, 'resources')
        self.assertDictEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
