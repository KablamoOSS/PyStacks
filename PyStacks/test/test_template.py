import unittest
import json
import os

from jinja2 import TemplateNotFound

from PyStacks.PyStacks.template import getResources
from PyStacks.PyStacks.template import template
from PyStacks.PyStacks.template import writecompiled
from PyStacks.PyStacks.template import templateCF
from PyStacks.PyStacks.template import voltron


class TestTemplate(unittest.TestCase):
    def test_getResources_maps_array(self):
        actual = getResources(resources=[1, 2, 3, 4, 5])
        self.assertEqual([1, 2, 3, 4, 5], actual)

    def test_template_exists(self):
        actual = template(template='./resources/ec2', ec2={})
        self.assertEqual(5, len(actual))

    def test_template_file_not_exist(self):
        with self.assertRaises(TemplateNotFound):
            template(template='./resources/SHOULDNOTEXIST', ec2={})

    def test_writecompiled_file_checkvalue(self):
        writecompiled(data='this is some data', name='test', region='aps2')

        filedirectory = os.path.dirname(os.path.realpath(__file__))

        data = None
        filepath = os.path.join(filedirectory,
                                '../configs/user/compiled/aps2/test.json')
        with open(filepath) as data_file:
            data = json.load(data_file)

        self.assertEqual('this is some data', data)

        os.remove(filepath)

    def test_writecompiled_file_array(self):
        writecompiled(data=[1, 2, 3], name='test_array', region='aps2')

        filedirectory = os.path.dirname(os.path.realpath(__file__))

        data = None
        filepath = os.path.join(
            filedirectory, '../configs/user/compiled/aps2/test_array.json')
        with open(filepath) as data_file:
            data = json.load(data_file)

        self.assertEqual([1, 2, 3], data)

        os.remove(filepath)

    def test_writecompiled_compile_folder_not_exist(self):
        filedirectory = os.path.dirname(os.path.realpath(__file__))

        directorypath = os.path.join(filedirectory,
                                     '../configs/user/compiled/NOTAREGION/')
        if os.path.exists(directorypath):
            os.rmdir(directorypath)

        writecompiled(
            data='this is some data', name='test', region='NOTAREGION')

        data = None
        filepath = os.path.join(
            filedirectory, '../configs/user/compiled/NOTAREGION/test.json')
        with open(filepath) as data_file:
            data = json.load(data_file)

        self.assertEqual('this is some data', data)

        os.remove(filepath)
        if os.path.exists(directorypath):
            os.rmdir(directorypath)

    def test_templateCF_empty_string_empty_dict(self):
        actual = templateCF(resources='', path='')
        self.assertEqual({}, actual)

    def test_templateCF_empty_resources_empty_dict(self):
        actual = templateCF(resources=[], path=None)
        self.assertEqual({}, actual)

    # def test_templateCF(self):
    #   resources = {
    #         's3': {
    #             'S3Bucket': {
    #                 'name': 'stuff.holder',
    #                 'accesscontrol': 'PublicRead',
    #                 'versioning': True,
    #                 'tags': {
    #                     'Name': 'Api'
    #                 }
    #             }
    #         },
    #         's3_policies': {
    #             'S3BucketPolicies': {
    #                 'policy': '"what": "on earth"'
    #             }
    #         }
    #     }
    #     expected = {
    #         'S3BucketPolicies': {
    #             'Type': 'AWS::S3::BucketPolicy',
    #             'Properties': {
    #                 'what': 'on earth'
    #             }
    #         },
    #         'S3Bucket': {
    #             'Type': 'AWS::S3::Bucket',
    #             'Properties': {
    #                 'AccessControl': 'PublicRead',
    #                 'VersioningConfiguration': {
    #                     'Status': 'Enabled'
    #                 },
    #                 'BucketName': 'stuff.holder',
    #                 'Tags': [
    #                     {
    #                         'Key': 'Name',
    #                         'Value': 'Api'
    #                     }
    #                 ]
    #             }
    #         }
    #     }

    #     actual = templateCF(resources, 'resources')
    #     self.assertDictEqual(actual, expected)

    def test_voltron(self):
        resources = {
            's3': {
                'S3Bucket': {
                    'name': 'stuff.holder',
                    'accesscontrol': 'PublicRead',
                    'versioning': True,
                    'tags': {
                        'Name': 'Api'
                    }
                }
            },
            's3_policies': {
                'S3BucketPolicies': {
                    'policy': '"what": "on earth"'
                }
            }
        }

        actual = voltron(
            stack='MyLittleStack',
            description='MyLittleDescription',
            parameters='MyLittleParameter',
            mappings='MyLittleMapping',
            resources=resources,
            outputs=resources
        )

        expected = {
            'Description': 'MyLittleDescription',
            'Parameters': 'MyLittleParameter',
            'AWSTemplateFormatVersion': '2010-09-09',
            'Outputs': {
                'S3Bucket': {
                    'Description': 'S3Bucket Object',
                    'Export': {'Name': {'Fn::Sub': '${AWS::StackName}-S3-S3Bucket'}},
                    'Value': {'Ref': 'S3Bucket'}
                },
                "S3BucketARN": {
                    "Description": "S3Bucket ARN",
                    "Export": {
                        "Name": {
                            "Fn::Sub": "${AWS::StackName}-S3-S3Bucket-ARN"
                        }
                    },
                    "Value": {
                        "Fn::GetAtt": [
                            "S3Bucket",
                            "Arn"
                        ]
                    }
                },
                'S3BucketDomainName': {
                    'Description': 'S3Bucket Domain Name',
                    'Export': {
                        'Name': {'Fn::Sub': '${AWS::StackName}-S3-S3Bucket-DomainName'}
                    },
                    'Value': {'Fn::GetAtt': ['S3Bucket', 'DomainName']}
                }
            },
            'Resources': {
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
            },
            'Mappings': 'MyLittleMapping'
        }

        print json.dumps(actual, sort_keys=True, indent=4, separators=(',', ': '))
        print expected
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
