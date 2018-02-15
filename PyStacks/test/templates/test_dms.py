import unittest

from PyStacks.PyStacks.template import templateCF


class TestTemplate(unittest.TestCase):

    def test_templateCF_DMSInstance(self):
        resources = {
            'dms_instance': {
                'myDMS': {
                    'replicationinstanceclass': 'dms.t2.small'
                },
            },
        }
        expected = {
            "myDMSInstance": {
                "Type": "AWS::DMS::ReplicationInstance",
                "Properties": {
                    "ReplicationInstanceClass": "dms.t2.small"
                }
            }
        }

        actual = templateCF(resources, 'resources')
        self.assertDictEqual(actual, expected)

    def test_templateCF_DMSSubnet(self):
        resources = {
            'dms_subnetgroup': {
                'TestDMSSubnetGroup': {
                    'description': 'Some Description...',
                    'subnets': [
                        'testsubnet1',
                        'testsubnet2'
                    ],
                    'tags': {
                        'testtagkey1': 'testtagval1',
                        'testtagkey2': 'testtagval2'
                    }
                }
            }
        }
        expected = {
            'TestDMSSubnetGroup': {
                'Type': 'AWS::DMS::ReplicationSubnetGroup',
                'Properties': {
                    'ReplicationSubnetGroupIdentifier': 'TestDMSSubnetGroup',
                    'ReplicationSubnetGroupDescription': 'Some Description...',
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
