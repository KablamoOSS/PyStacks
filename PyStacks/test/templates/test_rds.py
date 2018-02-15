import unittest

from PyStacks.PyStacks.template import templateCF


class TestTemplate(unittest.TestCase):

    def test_templateCF_RDSParameterGroup(self):
        resources = {
            'rdsparamsgroup': {
                'TestRDSParamGroup': {
                    'description': 'Some Description...',
                    'family': 'MySQL5.1',
                    'parameters': {
                        'testparamkey1': 'testparamval1',
                        'testparamkey2': 'testparamval2'
                    },
                    'tags': {
                        'testtagkey1': 'testtagval1',
                        'testtagkey2': 'testtagval2'
                    }
                }
            }
        }
        expected = {
            'TestRDSParamGroup': {
                'Type': 'AWS::RDS::DBParameterGroup',
                'Properties': {
                    'Description': 'Some Description...',
                    'Family': 'MySQL5.1',
                    'Parameters': {
                        'testparamkey1': 'testparamval1',
                        'testparamkey2': 'testparamval2'
                    },
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

    def test_templateCF_RDSSubnet(self):
        resources = {
            'rdssubnet': {
                'TestRDSSubnet': {
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
            'TestRDSSubnet': {
                'Type': 'AWS::RDS::DBSubnetGroup',
                'Properties': {
                    'DBSubnetGroupDescription': 'Some Description...',
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

    def test_templateCF_RDS(self):
        resources = {
            'rds': {
                'SimpleRDS': {
                    'allocatedstorage': '100',
                    'allowmajorupgrade': True,
                    'allowminorupgrade': True,
                    'multiaz': True,
                    'databasename': 'SimpleRDSName',
                    'instanceclass': 'db.r3.large',
                    'rdssubnetgroup': 'rdsubnet',
                    'engine': 'postgres',
                    'engineversion': '9.4.7',
                    'port': '5432',
                    'backupwindow': '19:30-20:00',
                    'maintenancewindow': '21:30-22:00',
                    'storageencryption': 'False',
                    'storagetype': 'standard',
                    'secgroups': [
                        'securityGroup1'
                    ]
                },
                'ComplexRDS': {
                    'allocatedstorage': '200',
                    'allowmajorupgrade': False,
                    'allowminorupgrade': False,
                    'multiaz': False,
                    'az': 'b',
                    'backupretention': 7,
                    'databasename': 'SimpleRDSName',
                    'dbname': 'SimpleDBName',
                    'iops': 3000,
                    'kmskeyid': 'kmskeyidtest',
                    'DBSnapshotIdentifier': 'snapshotidtest',
                    'monitoringarn': 'monitoringarntest',
                    'monitoringinterval': 5,
                    'instanceclass': 'db.r3.large',
                    'rdssubnetgroup': 'rdsubnet',
                    'engine': 'postgres',
                    'engineversion': '9.4.7',
                    'port': '5432',
                    'backupwindow': '19:30-20:00',
                    'maintenancewindow': '21:30-22:00',
                    'storageencryption': False,
                    'storagetype': 'standard',
                    'secgroups': [
                        'securityGroup1',
                        'securityGroup2'
                    ],
                    'tags': {
                        'testtagkey1': 'testtagval1',
                        'testtagkey2': 'testtagval2'
                    }
                }
            }
        }
        expected = {
            'SimpleRDS': {
                'Type': 'AWS::RDS::DBInstance',
                'Properties': {
                    'AllocatedStorage': '100',
                    'AllowMajorVersionUpgrade': 'true',
                    'AutoMinorVersionUpgrade': 'true',
                    'MultiAZ': 'true',
                    'CopyTagsToSnapshot': 'true',
                    'DBInstanceIdentifier': 'SimpleRDSName',
                    'DBInstanceClass': 'db.r3.large',
                    'DBSubnetGroupName': {
                        'Fn::ImportValue': {
                            'Fn::Sub': [
                                '${RDSSubnetStack}-RDS-rdsubnet-Subnet',
                                {
                                    'RDSSubnetStack':
                                    {
                                        'Ref': 'RDSSubnetStack'
                                    }
                                }
                            ]
                        }
                    },
                    'Engine': 'postgres',
                    'EngineVersion': '9.4.7',
                    'MasterUserPassword': {'Ref': 'DBPassword'},
                    'Port': '5432',
                    'PreferredBackupWindow': '19:30-20:00',
                    'PreferredMaintenanceWindow': '21:30-22:00',
                    'PubliclyAccessible': 'false',
                    'StorageEncrypted': 'false',
                    'StorageType': 'standard',
                    'VPCSecurityGroups': [
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
            },
            'ComplexRDS': {
                'Type': 'AWS::RDS::DBInstance',
                'Properties': {
                    'AllocatedStorage': '200',
                    'AllowMajorVersionUpgrade': 'false',
                    'AutoMinorVersionUpgrade': 'false',
                    'BackupRetentionPeriod': '7',
                    'MultiAZ': 'false',
                    'AvailabilityZone': {
                        'Fn::Join': [
                            '',
                            [
                                {
                                    'Ref': 'AWS::Region'
                                },
                                'b'
                            ]
                        ]
                    },
                    'CopyTagsToSnapshot': 'true',
                    'DBInstanceIdentifier': 'SimpleRDSName',
                    'DBInstanceClass': 'db.r3.large',
                    'DBName': 'SimpleDBName',
                    'DBSubnetGroupName': {
                        'Fn::ImportValue': {
                            'Fn::Sub': [
                                '${RDSSubnetStack}-RDS-rdsubnet-Subnet',
                                {
                                    'RDSSubnetStack':
                                    {
                                        'Ref': 'RDSSubnetStack'
                                    }
                                }
                            ]
                        }
                    },
                    'DBSnapshotIdentifier': 'snapshotidtest',
                    'Engine': 'postgres',
                    'EngineVersion': '9.4.7',
                    'Iops': '3000',
                    'KmsKeyId': 'kmskeyidtest',
                    'Port': '5432',
                    'PreferredBackupWindow': '19:30-20:00',
                    'PreferredMaintenanceWindow': '21:30-22:00',
                    'PubliclyAccessible': 'false',
                    'StorageEncrypted': 'false',
                    'StorageType': 'standard',
                    'VPCSecurityGroups': [
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
                        },
                        {
                            'Fn::ImportValue': {
                                'Fn::Sub': [
                                    '${SecurityStack}-SecGroup-securityGroup2',
                                    {
                                        'SecurityStack': {
                                            'Ref': 'SecurityStack'
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
