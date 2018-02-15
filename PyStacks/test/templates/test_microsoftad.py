import unittest

from PyStacks.PyStacks.template import templateCF


class TestTemplate(unittest.TestCase):

    def test_templateCF_MicrosoftAD(self):
        resources = {
            'microsoftad': {
                'testad': {
                    'createalias': True,
                    'enablesso': True,
                    'name': 'example.com',
                    'password': 'supers3cur3',
                    'shortname': 'ABC',
                    'subnets': [
                        'subnet1',
                        'subnet2'
                    ]
                }
            }
        }
        expected = {
            'testad': {
                'Type': 'AWS::DirectoryService::MicrosoftAD',
                'Properties': {
                    'CreateAlias': 'true',
                    'EnableSso': 'true',
                    'Name': 'example.com',
                    'Password': 'supers3cur3',
                    'ShortName': 'ABC',
                    'VpcSettings': {
                        'SubnetIds': [
                            {
                                'Fn::ImportValue': {
                                    'Fn::Sub': [
                                        '${VPCStack}-Subnet-subnet1',
                                        {
                                            'VPCStack': {
                                                'Ref': 'VPCStack'
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                'Fn::ImportValue': {
                                    'Fn::Sub': [
                                        '${VPCStack}-Subnet-subnet2',
                                        {
                                            'VPCStack': {
                                                'Ref': 'VPCStack'
                                            }
                                        }
                                    ]
                                }
                            }
                        ],
                        'VpcId': {
                            'Fn::ImportValue': {
                                'Fn::Sub': [
                                    '${VPCStack}-VPC-VPCid',
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
        }

        actual = templateCF(resources, 'resources')
        self.assertDictEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
