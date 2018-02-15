import unittest

from PyStacks.PyStacks.template import templateCF


class TestTemplate(unittest.TestCase):

    def test_templateCF_Route53Zone(self):
        resources = {
            'route53_zone': {
                'testr53zone': {
                    'name': 'example.com',
                    'comment': 'testzonecomment',
                    'hostedzone': {
                        'Name': 'testname',
                        'Tag2': 'testtagstuff'
                    },
                    'vpcs': {
                        'vpc-12345678': 'ap-southeast-2',
                        'vpc-87654321': 'us-west-2'
                    }
                }
            }
        }
        expected = {
            'testr53zone': {
                'Type': 'AWS::Route53::HostedZone',
                'Properties': {
                    'HostedZoneConfig': {
                        'Comment': 'testzonecomment'
                    },
                    'HostedZoneTags': [
                        {
                            'Key': 'Name',
                            'Value': 'testname'
                        },
                        {
                            'Key': 'Tag2',
                            'Value': 'testtagstuff'
                        }
                    ],
                    'VPCs': [
                        {
                            'VPCId': 'vpc-87654321',
                            'VPCRegion': 'us-west-2'
                        },
                        {
                            'VPCId': 'vpc-12345678',
                            'VPCRegion': 'ap-southeast-2'
                        }
                    ],
                    'Name': 'example.com'
                }
            }
        }

        actual = templateCF(resources, 'resources')
        self.assertDictEqual(actual, expected)

    def test_templateCF_Route53Record(self):
        resources = {
            'route53_record': {
                'testr53record': {
                    'comment': 'testcomment',
                    'zoneid': 'testzoneid',
                    'recordsets': [
                        [
                            'atest',
                            'A',
                            '1.2.3.4',
                            '900',
                            '0',
                            'base'
                        ],
                        [
                            'cnametest',
                            'CNAME',
                            'example.com',
                            '900',
                            '0',
                            'base'
                        ]
                    ]
                }
            }
        }
        expected = {
            'testr53record': {
                'Type': 'AWS::Route53::RecordSetGroup',
                'Properties': {
                    'Comment': 'testcomment',
                    'HostedZoneId': {
                        'Fn::ImportValue': {
                            'Fn::Sub': [
                                '${DNSStack}-Route53-testzoneid-Zone',
                                {
                                    'DNSStack': {
                                        'Ref': 'DNSStack'
                                    }
                                }
                            ]
                        }
                    },
                    'RecordSets': [
                        {
                            'Name': 'atest',
                            'Type': 'A',
                            'ResourceRecords': ['1.2.3.4'],
                            'TTL': '900',
                            'Weight': '0',
                            'SetIdentifier': 'base'
                        },
                        {
                            'Name': 'cnametest',
                            'Type': 'CNAME',
                            'ResourceRecords': ['example.com'],
                            'TTL': '900',
                            'Weight': '0',
                            'SetIdentifier': 'base'
                        }
                    ]
                }
            }
        }

        actual = templateCF(resources, 'resources')
        self.assertDictEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
