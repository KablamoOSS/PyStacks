import unittest

from PyStacks.PyStacks.template import templateCF


class TestTemplate(unittest.TestCase):

    def test_templateCF_IAMPolicies(self):
        resources = {
            'iam_policies': {
                'Policies': [
                    {
                        'Name': 'SimplePolicy',
                        'PolicyDocument': "{\n    \"Effect\": \"Allow\",\n    \"Action\": \"*\",\n    \"Resource\": \"*\"\n}"
                    },
                    {
                        'Name': 'ComplexPolicy',
                        'PolicyDocument': "{\n    \"Effect\": \"Allow\",\n    \"Action\": \"*\",\n    \"Resource\": \"*\"\n}",
                        'ManagedPolicys': [
                            'Policy1',
                            'Policy2'
                        ],
                        'Roles': [
                            'Role1',
                            'Role2'
                        ],
                        'Groups': [
                            'Group1',
                            'Group2'
                        ]
                    }
                ]
            }
        }

        expected = {
            'SimplePolicy': {
                'Type': 'AWS::IAM::Policy',
                'Properties': {
                    'PolicyName': 'SimplePolicy',
                    'PolicyDocument': {
                        'Version': '2012-10-17',
                        'Statement': [
                            {
                                "Effect": "Allow",
                                "Action": "*",
                                "Resource": "*"
                            }
                        ]
                    }
                }
            },
            'ComplexPolicy': {
                'Type': 'AWS::IAM::Policy',
                'Properties': {
                    'PolicyName': 'ComplexPolicy',
                    'PolicyDocument': {
                        'Version': '2012-10-17',
                        'Statement': [
                            {
                                "Effect": "Allow",
                                "Action": "*",
                                "Resource": "*"
                            }
                        ]
                    },
                    'ManagedPolicyArns': [
                        'arn:aws:iam::aws:policy/Policy1',
                        'arn:aws:iam::aws:policy/Policy2'
                    ],
                    'Roles': [
                        {
                            'Fn::ImportValue': {
                                'Fn::Sub': 'Role1'
                            }
                        },
                        {
                            'Fn::ImportValue': {
                                'Fn::Sub': 'Role2'
                            }
                        }
                    ],
                    'Groups': [
                        {
                            'Fn::ImportValue': {
                                'Fn::Sub': 'Group1'
                            }
                        },
                        {
                            'Fn::ImportValue': {
                                'Fn::Sub': 'Group2'
                            }
                        }
                    ]
                }
            }
        }

        actual = templateCF(resources, 'resources')
        self.assertDictEqual(actual, expected)

    def test_templateCF_IAMRolesInstanceProfiles(self):
        resources = {
            'iam_roles': {
                'Roles': {
                    'SimpleRole': {
                        'RoleName': 'SimpleRole',
                        'ReverseTrust': [
                            'arn:aws:iam::123456789012:root'
                        ]
                    },
                    'ComplexRole': {
                        'RoleName': 'ComplexRole',
                        'ManagedPolicys': [
                            'Policy1',
                            'Policy2'
                        ],
                        'MFA_Required': True,
                        'ReverseTrust': [
                            'arn:aws:iam::123456789012:root',
                            'arn:aws:iam::987654321098:root'
                        ],
                        'DependsOn': 'SimpleRole'
                    }
                },
                'InstanceProfiles': {
                    'SimpleInstProf': {
                        'RoleName': 'SimpleInstProf',
                        'Type': 'ec2'
                    },
                    'ComplexInstProf': {
                        'RoleName': 'ComplexInstProf',
                        'Type': 'ec2',
                        'ManagedPolicys': [
                            'Policy3',
                            'Policy4'
                        ]
                    }
                }
            }
        }
        expected = {
            'SimpleRole': {
                'Type': 'AWS::IAM::Role',
                'Properties': {
                    'AssumeRolePolicyDocument': {
                        'Version': '2012-10-17',
                        'Statement': [{
                            'Effect': 'Allow',
                            'Principal': {
                                'AWS': [
                                    'arn:aws:iam::123456789012:root'
                                ]
                            },
                            'Action': [
                                'sts:AssumeRole'
                            ]
                        }]
                    },
                    'RoleName': 'SimpleRole'
                }
            },
            'ComplexRole': {
                'Type': 'AWS::IAM::Role',
                'Properties': {
                    'ManagedPolicyArns': [
                        'arn:aws:iam::aws:policy/Policy1',
                        'arn:aws:iam::aws:policy/Policy2'
                    ],
                    'AssumeRolePolicyDocument': {
                        'Version': '2012-10-17',
                        'Statement': [{
                            'Effect': 'Allow',
                            'Principal': {
                                'AWS': [
                                    'arn:aws:iam::123456789012:root',
                                    'arn:aws:iam::987654321098:root'
                                ]
                            },
                            'Condition': {
                                'Bool': {
                                    'aws:MultiFactorAuthPresent': 'true'
                                }
                            },
                            'Action': [
                                'sts:AssumeRole'
                            ]
                        }]
                    },
                    'RoleName': 'ComplexRole'
                },
                'DependsOn': 'SimpleRole'
            },
            'SimpleInstProf': {
                'Type': 'AWS::IAM::Role',
                'Properties': {
                    'AssumeRolePolicyDocument': {
                        'Version': '2012-10-17',
                        'Statement': [{
                            'Effect': 'Allow',
                            'Principal': {
                                'Service': 'ec2.amazonaws.com'
                            },
                            'Action': ['sts:AssumeRole']
                        }]
                    },
                    'Path': {
                        'Fn::Join': [
                            '', [
                                '/', {
                                    'Ref': 'AccountName'
                                },
                                '/IAM/InstanceRoles/'
                            ]
                        ]
                    },
                    'RoleName': 'SimpleInstProf'
                }
            },
            'SimpleInstProfInstanceProfile': {
                'Type': 'AWS::IAM::InstanceProfile',
                'Properties': {
                    'InstanceProfileName': 'SimpleInstProf',
                    'Roles': [{
                        'Ref': 'SimpleInstProf'
                    }]
                },
                'DependsOn': 'SimpleInstProf'
            },
            'ComplexInstProf': {
                'Type': 'AWS::IAM::Role',
                'Properties': {
                    'AssumeRolePolicyDocument': {
                        'Version': '2012-10-17',
                        'Statement': [{
                            'Effect': 'Allow',
                            'Principal': {
                                'Service': 'ec2.amazonaws.com'
                            },
                            'Action': ['sts:AssumeRole']
                        }]
                    },
                    'ManagedPolicyArns': [
                        'arn:aws:iam::aws:policy/Policy3',
                        'arn:aws:iam::aws:policy/Policy4'
                    ],
                    'Path': {
                        'Fn::Join': [
                            '', [
                                '/', {
                                    'Ref': 'AccountName'
                                },
                                '/IAM/InstanceRoles/'
                            ]
                        ]
                    },
                    'RoleName': 'ComplexInstProf'
                }
            },
            'ComplexInstProfInstanceProfile': {
                'Type': 'AWS::IAM::InstanceProfile',
                'Properties': {
                    'InstanceProfileName': 'ComplexInstProf',
                    'Roles': [{
                        'Ref': 'ComplexInstProf'
                    }]
                },
                'DependsOn': 'ComplexInstProf'
            }
        }

        actual = templateCF(resources, 'resources')
        self.assertDictEqual(actual, expected)

    def test_templateCF_IAMUsersGroups(self):
        resources = {
            'iam_users': {
                'Users': {
                    'IAM-F.Last': {
                        'Groups': [
                            'NormalGroup'
                        ]
                    },
                    'IAM-F.Last2': {
                        'Groups': [
                            'NormalGroup',
                            'MissingGroup'
                        ]
                    },
                    'IAM-F.Last3': {
                        'Groups': [
                        ]
                    }
                },
                'Groups': {
                    'NormalGroup': {
                    },
                    'UnassignedGroup': {
                    }
                }
            }
        }
        expected = {
            'IAMFLast': {
                'Type': 'AWS::IAM::User',
                'Properties': {
                    'Groups': [
                        {
                            'Ref': 'NormalGroup'
                        }
                    ],
                    'Path': {
                        'Fn::Join': [
                            '', [
                                '/', {
                                    'Ref': 'AccountName'
                                },
                                '/IAM/Users/'
                            ]
                        ]
                    },
                    'UserName': 'IAM-F.Last'
                }
            },
            'IAMFLast2': {
                'Type': 'AWS::IAM::User',
                'Properties': {
                    'Groups': [
                        {
                            'Ref': 'NormalGroup'
                        },
                        {
                            'Ref': 'MissingGroup'
                        }
                    ],
                    'Path': {
                        'Fn::Join': [
                            '', [
                                '/', {
                                    'Ref': 'AccountName'
                                },
                                '/IAM/Users/'
                            ]
                        ]
                    },
                    'UserName': 'IAM-F.Last2'
                }
            },
            'IAMFLast3': {
                'Type': 'AWS::IAM::User',
                'Properties': {
                    'Groups': [
                    ],
                    'Path': {
                        'Fn::Join': [
                            '', [
                                '/', {
                                    'Ref': 'AccountName'
                                },
                                '/IAM/Users/'
                            ]
                        ]
                    },
                    'UserName': 'IAM-F.Last3'
                }
            },
            'NormalGroup': {
                'Type': 'AWS::IAM::Group',
                'Properties': {
                    'GroupName': 'NormalGroup',
                    'Path': {
                        'Fn::Join': [
                            '', [
                                '/', {
                                    'Ref': 'AccountName'
                                },
                                '/IAM/Groups/'
                            ]
                        ]
                    }
                }
            },
            'UnassignedGroup': {
                'Type': 'AWS::IAM::Group',
                'Properties': {
                    'GroupName': 'UnassignedGroup',
                    'Path': {
                        'Fn::Join': [
                            '', [
                                '/', {
                                    'Ref': 'AccountName'
                                },
                                '/IAM/Groups/'
                            ]
                        ]
                    }
                }
            }
        }

        actual = templateCF(resources, 'resources')
        self.assertDictEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
