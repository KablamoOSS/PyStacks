import unittest
from PyStacks.PyStacks.template import templateCF


class TestTemplate(unittest.TestCase):

    def test_templateCF_ElasticSearch(self):

        self.maxDiff = None

        resources = {
            "elasticsearch": {
                "ElasticSearchTest": {
                    "version": 5.5,
                    "dedicatedmaster": True,
                    "instancecount": 4,
                    "instancetype": "m4.large.elasticsearch",
                    "mastertype": "m4.large.elasticsearch",
                    "mastercount": 2,
                    "zoneid": "testaws",
                    "zonesuffix": "test.aws",
                    "ebsoptions": {
                        "iops": 0,
                        "size": 60,
                        "type": "gp2"
                    },
                    "snapshotoptions": {
                        "AutomatedSnapshotStartHour": 0
                    },
                    "advancedoptions": {
                        "rest.action.multi.allow_explicit_index": "true"
                    },
                    "policy": {
                        "Action": "*",
                        "Effect": "Allow",
                        "Resource": "*"
                    }
                }
            }
        }
        expected = {
            "ElasticSearchTest": {
                "Properties": {
                    "AccessPolicies": {
                        "Statement": [
                            {
                                "Action": "*",
                                "Effect": "Allow",
                                "Resource": "*"
                            }
                        ],
                        "Version": "2012-10-17"
                    },
                    "AdvancedOptions": {
                        "rest.action.multi.allow_explicit_index": "true"
                    },
                    "DomainName": "ElasticSearchTest",
                    "EBSOptions": {
                        "EBSEnabled": "true",
                        "Iops": 0,
                        "VolumeSize": 60,
                        "VolumeType": "gp2"
                    },
                    "ElasticsearchClusterConfig": {
                        "DedicatedMasterCount": "2",
                        "DedicatedMasterEnabled": "true",
                        "DedicatedMasterType": "m4.large.elasticsearch",
                        "InstanceCount": "4",
                        "InstanceType": "m4.large.elasticsearch",
                        "ZoneAwarenessEnabled": "true"
                    },
                    "ElasticsearchVersion": "5.5",
                    "SnapshotOptions": {
                        "AutomatedSnapshotStartHour": "0"
                    }
                },
                "Type": "AWS::Elasticsearch::Domain"
            },
            "ElasticSearchTestDNS": {
                "Properties": {
                    "Comment": "ElasticSearchTest Records by default",
                    "HostedZoneId": {
                        "Fn::ImportValue": {
                            "Fn::Sub": [
                                "${DNSStack}-Route53-testaws-Zone", {
                                    "DNSStack": {
                                        "Ref": "DNSStack"
                                    }
                                }
                            ]
                        }
                    },
                    "RecordSets": [
                        {
                            "Name": "ElasticSearchTest.es.test.aws",
                            "ResourceRecords": [
                                {
                                    "Fn::GetAtt": [
                                        "ElasticSearchTest",
                                        "DomainEndpoint"
                                    ]
                                }
                            ],
                            "SetIdentifier": "ElasticSearchTest.es.test.aws",
                            "TTL": "60",
                            "Type": "CNAME",
                            "Weight": "10"
                        }
                    ]
                },
                "Type": "AWS::Route53::RecordSetGroup"
            }
        }

        actual = templateCF(resources, 'resources')
        self.assertDictEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
