import unittest

from PyStacks.PyStacks.template import templateCF


class TestTemplate(unittest.TestCase):

    def test_templateCF_GenericLambda(self):
        resources = {
            'lambda': {
                'testLambda': {
                    'code': {
                        's3bucket': 'testS3Bucket',
                        'key': 's3-key',
                    },
                    'description': 'test description',
                    'environment': {
                        'envvar': 'value',
                    },
                    'functionName': 'lambdaName',
                    'handler': 'main.Handle',
                    'memorySize': 256,
                    'role': 'testRole',
                    'runTime': 'python2.7',
                    'timeout': 30,
                    'permission': 'testPerm',
                    'vpcConfig': {
                        'securityGroups': [
                            'SquidSecurity',
                        ],
                        'subnetIds': [
                            'Internal1',
                            'Internal2',
                            'Internal3',
                        ],
                    },
                },
            },
        }
        expected = {
            "testLambda": {
                "Type": "AWS::Lambda::Function",
                "Properties": {
                    "Handler": "main.Handle",
                    "Description": "test description",
                    "Code": {
                        "S3Bucket": "testS3Bucket",
                        "S3Key": "s3-key"
                    },
                    "FunctionName": "lambdaName",
                    "MemorySize": "256",
                    "Timeout": "30",
                    "Environment": {
                        "Variables": {
                            "envvar": "value"
                        }
                    },
                    "Role": "testRole",
                    "VpcConfig": {
                        "SecurityGroupIds": [
                            {"Fn::ImportValue": {"Fn::Sub": [
                                "${SecurityStack}-SecGroup-SquidSecurity", {"SecurityStack": {"Ref": "SecurityStack"}}]}}
                        ],
                        "SubnetIds": [
                            {"Fn::ImportValue": {"Fn::Sub": [
                                "${VPCStack}-Subnet-Internal1", {"VPCStack": {"Ref": "VPCStack"}}]}},
                            {"Fn::ImportValue": {"Fn::Sub": [
                                "${VPCStack}-Subnet-Internal2", {"VPCStack": {"Ref": "VPCStack"}}]}},
                            {"Fn::ImportValue": {"Fn::Sub": [
                                "${VPCStack}-Subnet-Internal3", {"VPCStack": {"Ref": "VPCStack"}}]}}
                        ]
                    }
                }
            }
        }

        actual = templateCF(resources, 'resources')
        self.assertDictEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
