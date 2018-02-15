import unittest

from PyStacks.PyStacks.template import templateCF


class TestTemplate(unittest.TestCase):

    def test_templateCF_RedshiftSubnetGroup(self):
        resources = {
            'redshift_subnetgroup': {
                'testsubnetgroup': {
                    'description': 'somesubnetgroup',
                    'subnets': [
                        'subnet1',
                        'subnet2'
                    ]
                }
            }
        }
        expected = {
            'testsubnetgroup': {
                'Type': 'AWS::Redshift::ClusterSubnetGroup',
                'Properties': {
                    'Description': 'somesubnetgroup',
                    'SubnetIds': [
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
                    ]
                }
            }
        }

        actual = templateCF(resources, 'resources')
        self.assertDictEqual(actual, expected)

    def test_templateCF_RedshiftParametersGroup(self):
        resources = {
            'redshift_paramsgroup': {
                'testparamgroup': {
                    'description': 'someparamgroup',
                    'groupfamily': 'aurora5.6',
                    'parameters': {
                        'testparamname1': 'testparamval1',
                        'testparamname2': 'testparamval2'
                    }
                }
            }
        }
        expected = {
            'testparamgroup': {
                'Type': 'AWS::Redshift::ClusterParameterGroup',
                'Properties': {
                    'Description': 'someparamgroup',
                    'ParameterGroupFamily': 'aurora5.6',
                    'Parameters': [
                        {
                            'ParameterName': 'testparamname1',
                            'ParameterValue': 'testparamval1'
                        },
                        {
                            'ParameterName': 'testparamname2',
                            'ParameterValue': 'testparamval2'
                        }
                    ]
                }
            }
        }

        actual = templateCF(resources, 'resources')
        self.assertDictEqual(actual, expected)

    def test_templateCF_RedshiftCluster(self):
        resources = {
            'redshift': {
                'simplecluster': {
                    'clustersubnetgroupname': 'testclustersubnetgroupname',
                    'dbname': 'testdbname',
                    'masterusername': 'myuser',
                    'nodetype': 'dw.hs1.xlarge',
                    'maintenancewindow': '21:30-22:00',
                    'secgroupid': [
                        'sg-1234567'
                    ]
                },
                'complexcluster': {
                    'allowupgrade': True,
                    'automatedsnapshotretentionperiod': 300,
                    'az': 'ap-southeast-2c',
                    'clusterparamsgroup': 'testclusterparamsgroup',
                    'clustersubnetgroupname': 'testclustersubnetgroupname',
                    'clustertype': 'multi-node',
                    'clusterversion': '1.2.3',
                    'dbname': 'testdbname',
                    'eip': '1.2.3.4',
                    'encrypted': False,
                    'hsmclientcertificateidentifier': 'testhsmclientcertid',
                    'hsmconfigurationidentifier': 'testhsmconfigid',
                    'iamroles': [
                        'iamrole1',
                        'iamrole2'
                    ],
                    'kmskeyid': 'testkmskeyid',
                    'masterusername': 'myuser',
                    'nodetype': 'dw.hs1.xlarge',
                    'numberofnodes': 4,
                    'owneraccount': '123456789012',
                    'port': '45439',
                    'maintenancewindow': '21:30-22:00',
                    'public': True,
                    'snapshotidentifier': 'snap-12345678',
                    'snapshotclusteridentifier': 'snap-87654321',
                    'secgroupid': [
                        'sg-1234567',
                        'sg-7654321'
                    ]
                }
            }
        }
        expected = {
            'simplecluster': {
                'Type': 'AWS::Redshift::Cluster',
                'Properties': {
                    'ClusterSubnetGroupName': {
                        'Fn::ImportValue': {
                            'Fn::Sub': [
                                '${RedshiftSubnetGroupStack}-Subnet-testclustersubnetgroupname',
                                {
                                    'RedshiftSubnetGroupStack': {
                                        'Ref': 'RedshiftSubnetGroupStack'
                                    }
                                }
                            ]
                        }
                    },
                    'DBName': 'testdbname',
                    'Encrypted': 'true',
                    'MasterUsername': 'myuser',
                    'MasterUserPassword': {'Ref': 'DBPassword'},
                    'NodeType': 'dw.hs1.xlarge',
                    'Port': 5439,
                    'PreferredMaintenanceWindow': '21:30-22:00',
                    'PubliclyAccessible': 'false',
                    'VpcSecurityGroupIds': [
                        'sg-1234567'
                    ]
                }
            },
            'complexcluster': {
                'Type': 'AWS::Redshift::Cluster',
                'Properties': {
                    'AllowVersionUpgrade': 'true',
                    'AutomatedSnapshotRetentionPeriod': '300',
                    'AvailabilityZone': 'ap-southeast-2c',
                    'ClusterParameterGroupName': {
                        'Fn::ImportValue': {
                            'Fn::Sub': [
                                '${RedshiftParamsGroupStack}-ParamsGroup-testclusterparamsgroup',
                                {
                                    'RedshiftParamsGroupStack': {
                                        'Ref': 'RedshiftParamsGroupStack'
                                    }
                                }
                            ]
                        }
                    },
                    'ClusterSubnetGroupName': {
                        'Fn::ImportValue': {
                            'Fn::Sub': [
                                '${RedshiftSubnetGroupStack}-Subnet-testclustersubnetgroupname',
                                {
                                    'RedshiftSubnetGroupStack': {
                                        'Ref': 'RedshiftSubnetGroupStack'
                                    }
                                }
                            ]
                        }
                    },
                    'ClusterType': 'multi-node',
                    'ClusterVersion': '1.2.3',
                    'DBName': 'testdbname',
                    'ElasticIp': '1.2.3.4',
                    'Encrypted': 'false',
                    'HsmClientCertificateIdentifier': 'testhsmclientcertid',
                    'HsmConfigurationIdentifier': 'testhsmconfigid',
                    'IamRoles': [
                        {
                            "Fn::ImportValue": {
                                "Fn::Sub": [
                                    "${IAMRoleStack}-iamrole1",
                                    {
                                        "IAMRoleStack": {
                                            "Ref": "IAMRoleStack"
                                        }
                                    }
                                ]
                            }
                        },
                        {
                            "Fn::ImportValue": {
                                "Fn::Sub": [
                                    "${IAMRoleStack}-iamrole2",
                                    {
                                        "IAMRoleStack": {
                                            "Ref": "IAMRoleStack"
                                        }
                                    }
                                ]
                            }
                        }
                    ],
                    'KmsKeyId': {
                        'Fn::ImportValue': {
                            'Fn::Sub': [
                                '${KMSStack}-KMS-testkmskeyid',
                                {
                                    'KMSStack': {
                                        'Ref': 'KMSStack'
                                    }
                                }
                            ]
                        }
                    },
                    'MasterUsername': 'myuser',
                    'MasterUserPassword': {'Ref': 'DBPassword'},
                    'NodeType': 'dw.hs1.xlarge',
                    'NumberOfNodes': 4,
                    'OwnerAccount': '123456789012',
                    'Port': 45439,
                    'PreferredMaintenanceWindow': '21:30-22:00',
                    'PubliclyAccessible': 'true',
                    'SnapshotClusterIdentifier': 'snap-87654321',
                    'SnapshotIdentifier': 'snap-12345678',
                    'VpcSecurityGroupIds': [
                        'sg-1234567',
                        'sg-7654321'
                    ]
                }
            }
        }

        actual = templateCF(resources, 'resources')
        self.assertDictEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
