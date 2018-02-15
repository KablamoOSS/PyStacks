import unittest

from PyStacks.PyStacks.template import templateCF


class TestTemplate(unittest.TestCase):

    def test_templateCF_EFSMount(self):
        resources = {
            'efsmount': {
                'testefsmount': {
                    'filesystemid': 'testfsid',
                    'ipaddress': '1.2.3.4',
                    'securitygroupid': 'sg-1234567',
                    'subnetid': 'sub-1234567'
                }
            }
        }
        expected = {
            'testefsmount': {
                'Type': 'AWS::EFS::MountTarget',
                'Properties': {
                    'FileSystemId': {
                        'Fn::ImportValue': {
                            'Fn::Sub': [
                                '${EFSStack}-EFS-testfsid',
                                {
                                    'EFSStack': {
                                        'Ref': 'EFSStack'
                                    }
                                }
                            ]
                        }
                    },
                    'IpAddress': '1.2.3.4',
                    'SecurityGroups': [
                        {
                            'Fn::ImportValue': {
                                'Fn::Sub': [
                                    '${SecurityStack}-SecGroup-sg-1234567',
                                    {
                                        'SecurityStack': {
                                            'Ref': 'SecurityStack'
                                        }
                                    }
                                ]
                            }
                        }
                    ],
                    'SubnetId': {
                        'Fn::ImportValue': {
                            'Fn::Sub': [
                                '${VPCStack}-Subnet-sub-1234567',
                                {
                                    'VPCStack': {
                                        'Ref': 'VPCStack'
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        }

        actual = templateCF(resources, 'resources')
        self.assertDictEqual(actual, expected)

    def test_templateCF_EFS(self):
        resources = {
            'efs': {
                'testefs': {
                    'tags': {
                        'tagname1': 'tagval1',
                        'tagname2': 'tagval2'
                    },
                    'performancemode': 'generalPurpose'
                }
            }
        }
        expected = {
            'testefs': {
                'Type': 'AWS::EFS::FileSystem',
                'Properties': {
                    'FileSystemTags': [
                        {
                            'Key': 'tagname2',
                            'Value': 'tagval2'
                        },
                        {
                            'Key': 'tagname1',
                            'Value': 'tagval1'
                        }
                    ],
                    'PerformanceMode': 'generalPurpose'
                }
            }
        }

        actual = templateCF(resources, 'resources')
        self.assertDictEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
