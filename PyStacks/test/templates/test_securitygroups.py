import unittest

from PyStacks.PyStacks.template import templateCF


class TestTemplate(unittest.TestCase):

    def test_templateCF_SecurityGroups(self):
        resources = {
            'securitygroups': {
                'StuffSecurity': {
                    'sg_description': 'The stuff security group',
                    'ingress': [
                        ['icmp', -1, -1, 'VPCCIDR'],
                        ['icmp', -1, -1, 'SydIpRange'],
                        ['tcp', 5432, 5432, 'StuffSecurity', 'SG_REF_VPC']
                    ],
                    'egress': [
                        ['icmp', -1, -1, 'CoreIpRange'],
                        ['tcp', 21, 21, 'GlobalIpRange'],
                        ['tcp', 22, 22, 'GlobalIpRange']
                    ]
                }
            }
        }
        expected = {
            "StuffSecurity": {
                "Type": "AWS::EC2::SecurityGroup",
                "Properties": {
                    "VpcId": {
                        "Fn::ImportValue": {
                            "Fn::Sub": [
                                "${VPCStack}-VPCid",
                                {"VPCStack": {
                                    "Ref": "VPCStack"
                                }}
                            ]
                        }
                    },
                    "Tags": [
                        {
                            "Key": "Name",
                            "Value": "StuffSecurity"
                        }
                    ],
                    "GroupDescription": "The stuff security group",
                    "SecurityGroupIngress": [
                        {
                            "IpProtocol": "icmp",
                            "FromPort": "-1",
                            "ToPort": "-1",
                            "CidrIp": {
                                "Ref": "VPCCIDR"
                            }
                        },
                        {
                            "IpProtocol": "icmp",
                            "FromPort": "-1",
                            "ToPort": "-1",
                            "CidrIp": {
                                "Ref": "SydIpRange"
                            }
                        },
                        {
                            "IpProtocol": "tcp",
                            "FromPort": "5432",
                            "ToPort": "5432",
                            "SourceSecurityGroupId": {
                                "Ref": "StuffSecurity"
                            }
                        }
                    ],
                    "SecurityGroupEgress": [
                        {
                            "IpProtocol": "icmp",
                            "FromPort": "-1",
                            "ToPort": "-1",
                            "CidrIp": {
                                "Ref": "CoreIpRange"
                            }
                        },
                        {
                            "IpProtocol": "tcp",
                            "FromPort": "21",
                            "ToPort": "21",
                            "CidrIp": {
                                "Ref": "GlobalIpRange"
                            }
                        },
                        {
                            "IpProtocol": "tcp",
                            "FromPort": "22",
                            "ToPort": "22",
                            "CidrIp": {
                                "Ref": "GlobalIpRange"
                            }
                        }
                    ]
                }
            }
        }

        actual = templateCF(resources, 'resources')
        self.assertDictEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
