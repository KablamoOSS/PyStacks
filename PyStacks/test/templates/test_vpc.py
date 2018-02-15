import unittest

from PyStacks.PyStacks.template import templateCF


class TestTemplate(unittest.TestCase):

    def test_templateCF_VPC(self):
        resources = {
            'vpc': {
                'Details': {
                    'VPC_Name': 'vpcname',
                    'VPC_CIDR': '10.0.0.0/8'
                },
                'Tags': {
                    'tagkey1': 'tagval1',
                    'tagkey2': 'tagval2'
                },
                'Subnets': {
                    'subnet1': {
                        'CIDR': '10.0.1.0/24',
                        'AZ': 0,
                        'RouteTable': 'routetable1',
                        'NetAcl': 'netacl1'
                    },
                    'subnet2': {
                        'CIDR': '10.0.2.0/24',
                        'AZ': 1,
                        'RouteTable': 'routetable2',
                        'NetAcl': 'netacl2'
                    }
                },
                'DHCP': {
                    'dhcp_name': 'example.com',
                    'dhcp_dns_servers': '8.8.8.8',
                    'dhcp_ntb_type': 2,
                    'dhcp_ntp_servers': '216.239.35.0'
                },
                'Routetables': {
                    'routetable1': {
                        'route1': {
                            'route_name': 'route1',
                            'route_cidr': '10.0.1.0/24',
                            'route_gw': 'igw-1234567'
                        },
                        'route2': {
                            'route_name': 'route2',
                            'route_cidr': '10.0.2.0/24',
                            'route_gw': 'igw-1234567'
                        }
                    },
                    'routetable2': {
                    }
                },
                'NetworkAcls': {
                    'netacl1': {
                        'aclrule1': '0,6,allow,false,10.0.1.0/24,22,22',
                        'aclrule2': '1,6,deny,false,10.0.1.0/24,0,65535'
                    },
                    'netacl2': {
                    }
                }
            }
        }
        expected = {
            'vpcname': {
                'Type': 'AWS::EC2::VPC',
                'Properties': {
                    'CidrBlock': '10.0.0.0/8',
                    'Tags': [
                        {
                            'Key': 'tagkey1',
                            'Value': 'tagval1'
                        },
                        {
                            'Key': 'tagkey2',
                            'Value': 'tagval2'
                        }
                    ],
                    'EnableDnsSupport': "true",
                    'EnableDnsHostnames': "true"
                }
            },
            'subnet1': {
                'Type': 'AWS::EC2::Subnet',
                'Properties': {
                    'VpcId': {
                        'Ref': 'vpcname'
                    },
                    'CidrBlock': '10.0.1.0/24',
                    'AvailabilityZone': {
                        'Fn::Select': [
                            '0',
                            {
                                'Fn::GetAZs': ''
                            }
                        ]
                    },
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': 'subnet1'
                        }
                    ]
                }
            },
            'subnet2': {
                'Type': 'AWS::EC2::Subnet',
                'Properties': {
                    'VpcId': {
                        'Ref': 'vpcname'
                    },
                    'CidrBlock': '10.0.2.0/24',
                    'AvailabilityZone': {
                        'Fn::Select': [
                            '1',
                            {
                                'Fn::GetAZs': ''
                            }
                        ]
                    },
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': 'subnet2'
                        }
                    ]
                }
            },
            'DHCPSet': {
                'Type': 'AWS::EC2::DHCPOptions',
                'Properties': {
                    'DomainName': 'example.com',
                    'DomainNameServers': [
                        '8.8.8.8'
                    ],
                    'NetbiosNodeType': '2',
                    'NtpServers': [
                        '216.239.35.0'
                    ],
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': 'example.com'
                        }
                    ]
                }
            },
            'DHCPAssociate': {
                'Type': 'AWS::EC2::VPCDHCPOptionsAssociation',
                'Properties': {
                    'DhcpOptionsId': {
                        'Ref': 'DHCPSet'
                    },
                    'VpcId': {
                        'Ref': 'vpcname'
                    }
                }
            },
            'InternetGateway': {
                'Type': 'AWS::EC2::InternetGateway',
                'Properties': {
                }
            },
            'AttachGatewayIgw': {
                'Type': 'AWS::EC2::VPCGatewayAttachment',
                'DependsOn': [
                    'InternetGateway',
                    'vpcname'
                ],
                'Properties': {
                    'VpcId': {
                        'Ref': 'vpcname'
                    },
                    'InternetGatewayId': {
                        'Ref': 'InternetGateway'
                    }
                }
            },
            'routetable1': {
                'Type': 'AWS::EC2::RouteTable',
                'Properties': {
                    'VpcId': {
                        'Ref': 'vpcname'
                    },
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': 'routetable1'
                        }
                    ]
                }
            },
            'route1': {
                'Type': 'AWS::EC2::Route',
                'DependsOn': 'AttachGatewayVgw',
                'Properties': {
                    'RouteTableId': {
                        'Ref': 'routetable1'
                    },
                    'DestinationCidrBlock': '10.0.1.0/24',
                    'GatewayId': {
                        'Ref': 'igw-1234567'
                    }
                }
            },
            'route2': {
                'Type': 'AWS::EC2::Route',
                'DependsOn': 'AttachGatewayVgw',
                'Properties': {
                    'RouteTableId': {
                        'Ref': 'routetable1'
                    },
                    'DestinationCidrBlock': '10.0.2.0/24',
                    'GatewayId': {
                        'Ref': 'igw-1234567'
                    }
                }
            },
            'routetable1RoutePropagation': {
                'Type': 'AWS::EC2::VPNGatewayRoutePropagation',
                'DependsOn': 'AttachGatewayVgw',
                'Properties': {
                    'RouteTableIds': [
                        {
                            'Ref': 'routetable1'
                        }
                    ],
                    'VpnGatewayId': {
                        'Ref': 'VGW'
                    }
                }
            },
            'routetable2': {
                'Type': 'AWS::EC2::RouteTable',
                'Properties': {
                    'VpcId': {
                        'Ref': 'vpcname'
                    },
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': 'routetable2'
                        }
                    ]
                }
            },
            'routetable2RoutePropagation': {
                'Type': 'AWS::EC2::VPNGatewayRoutePropagation',
                'DependsOn': 'AttachGatewayVgw',
                'Properties': {
                    'RouteTableIds': [
                        {
                            'Ref': 'routetable2'
                        }
                    ],
                    'VpnGatewayId': {
                        'Ref': 'VGW'
                    }
                }
            },
            'subnet1SubnetRouteTableAssociation': {
                'Type': 'AWS::EC2::SubnetRouteTableAssociation',
                'Properties': {
                    'SubnetId': {
                        'Ref': 'subnet1'
                    },
                    'RouteTableId': {
                        'Ref': 'routetable1'
                    }
                }
            },
            'subnet1SubnetNetworkAclAssociation': {
                'Type': 'AWS::EC2::SubnetNetworkAclAssociation',
                'Properties': {
                    'SubnetId': {
                        'Ref': 'subnet1'
                    },
                    'NetworkAclId': {
                        'Ref': 'netacl1'
                    }
                }
            },
            'subnet2SubnetRouteTableAssociation': {
                'Type': 'AWS::EC2::SubnetRouteTableAssociation',
                'Properties': {
                    'SubnetId': {
                        'Ref': 'subnet2'
                    },
                    'RouteTableId': {
                        'Ref': 'routetable2'
                    }
                }
            },
            'subnet2SubnetNetworkAclAssociation': {
                'Type': 'AWS::EC2::SubnetNetworkAclAssociation',
                'Properties': {
                    'SubnetId': {
                        'Ref': 'subnet2'
                    },
                    'NetworkAclId': {
                        'Ref': 'netacl2'
                    }
                }
            },
            'netacl1': {
                'Type': 'AWS::EC2::NetworkAcl',
                'Properties': {
                    'VpcId': {
                        'Ref': 'vpcname'
                    },
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': 'netacl1'
                        }
                    ]
                }
            },
            'aclrule1': {
                'Type': 'AWS::EC2::NetworkAclEntry',
                'Properties': {
                    'NetworkAclId': {
                        'Ref': 'netacl1'
                    },
                    'RuleNumber': '0',
                    'Protocol': '6',
                    'RuleAction': 'allow',
                    'Egress': 'false',
                    'CidrBlock': '10.0.1.0/24',
                    'PortRange': {
                        'From': '22',
                        'To': '22'
                    }
                }
            },
            'aclrule2': {
                'Type': 'AWS::EC2::NetworkAclEntry',
                'Properties': {
                    'NetworkAclId': {
                        'Ref': 'netacl1'
                    },
                    'RuleNumber': '1',
                    'Protocol': '6',
                    'RuleAction': 'deny',
                    'Egress': 'false',
                    'CidrBlock': '10.0.1.0/24',
                    'PortRange': {
                        'From': '0',
                        'To': '65535'
                    }
                }
            },
            'netacl2': {
                'Type': 'AWS::EC2::NetworkAcl',
                'Properties': {
                    'VpcId': {
                        'Ref': 'vpcname'
                    },
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': 'netacl2'
                        }
                    ]
                }
            },
            'AttachGatewayVgw': {
                'Type': 'AWS::EC2::VPCGatewayAttachment',
                'DependsOn': [
                    'InternetGateway',
                    'vpcname'
                ],
                'Properties': {
                    'VpcId': {
                        'Ref': 'vpcname'
                    },
                    'VpnGatewayId': {
                        'Ref': 'VGW'
                    }
                }
            }
        }

        actual = templateCF(resources, 'resources')
        self.assertDictEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
