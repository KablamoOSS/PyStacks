import unittest

from PyStacks.PyStacks.template import templateCF


class TestTemplate(unittest.TestCase):

    def test_templateCF_ElastiCacheSubnet(self):
        resources = {
            'elasticachesubnet': {
                'TestElastiCacheSubnet': {
                    'name': 'Some Name',
                    'description': 'Some Description...',
                    'subnets': [
                        'testsubnet1',
                        'testsubnet2'
                    ]
                }
            }
        }
        expected = {
            'TestElastiCacheSubnet': {
                'Type': 'AWS::ElastiCache::SubnetGroup',
                'Properties': {
                    'CacheSubnetGroupName': 'Some Name',
                    'Description': 'Some Description...',
                    'SubnetIds': [
                        {
                            "Fn::ImportValue": {
                                "Fn::Sub": [
                                    "${VPCStack}-Subnet-testsubnet1",
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
                                    "${VPCStack}-Subnet-testsubnet2",
                                    {
                                        "VPCStack": {
                                            "Ref": "VPCStack"
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        }

        actual = templateCF(resources, 'resources')
        self.assertDictEqual(actual, expected)

    def test_templateCF_ElastiCache(self):
        resources = {
            'elasticache': {
                'SimpleElastiCache': {
                    'name': 'some redis',
                    'cacheSubnetGroup': 'subnetGroup1',
                    'secgroups': [
                        'securityGroup1'
                    ]
                }
            }
        }
        expected = {
            'SimpleElastiCache': {
                'Type': 'AWS::ElastiCache::CacheCluster',
                'Properties': {
                    'CacheNodeType': 'cache.t2.micro',
                    'ClusterName': 'some redis',
                    'Engine': 'redis',
                    'NumCacheNodes': 1,
                    'CacheSubnetGroupName': {
                        'Fn::ImportValue': {
                            'Fn::Sub': [
                                '${CacheSubnetStack}-ElastiCache-subnetGroup1-Subnet',
                                {
                                    'CacheSubnetStack':
                                    {
                                        'Ref': 'CacheSubnetStack'
                                    }
                                }
                            ]
                        }
                    },
                    'VpcSecurityGroupIds': [
                        {
                            'Fn::ImportValue': {
                                'Fn::Sub': [
                                    '${SecurityStack}-SecGroup-securityGroup1',
                                    {
                                        'SecurityStack': {
                                            'Ref': 'SecurityStack'
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        }

        actual = templateCF(resources, 'resources')
        self.assertDictEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
