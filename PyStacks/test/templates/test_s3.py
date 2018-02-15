import unittest

from PyStacks.PyStacks.template import templateCF


class TestTemplate(unittest.TestCase):

    def test_templateCF_S3(self):
        resources = {
            's3': {
                'S3Bucket': {
                    'name': 'stuff.holder',
                    'accesscontrol': 'PublicRead',
                    'versioning': True,
                    'tags': {
                        'Name': 'Api'
                    },
                    'notices': {
                        'lamda': [{
                            'event': 's3:ObjectCreated:*',
                            'function': 'somelambdaarn'
                        }]
                    }
                }
            },
            's3_policies': {
                'S3BucketPolicies': {
                    'policy': '"what": "on earth"'
                }
            }
        }
        expected = {
            'S3BucketPolicies': {
                'Type': 'AWS::S3::BucketPolicy',
                'Properties': {
                    'what': 'on earth'
                }
            },
            'S3Bucket': {
                'Type': 'AWS::S3::Bucket',
                'Properties': {
                    'AccessControl': 'PublicRead',
                    'NotificationConfiguration': {
                        'LambdaConfigurations': [
                            {
                                'Event': 's3:ObjectCreated:*',
                                'Function': 'somelambdaarn'
                            }
                        ]
                    },
                    'VersioningConfiguration': {
                        'Status': 'Enabled'
                    },
                    'BucketName': 'stuff.holder',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': 'Api'
                        }
                    ]
                }
            }
        }
        self.maxDiff = 'None'
        actual = templateCF(resources, 'resources')
        self.assertDictEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
