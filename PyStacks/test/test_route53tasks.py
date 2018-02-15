import unittest

from mock import MagicMock

from PyStacks.PyStacks.route53tasks import route53tasks


class TestRoute53TasksSetup(unittest.TestCase):
    def setUp(self):
        self.mocksession = MagicMock()
        self.mockcfClient = MagicMock()
        self.mockdnsClient = MagicMock()

        self.mocksession.client.return_value = self.mockdnsClient

        self.dnstasks = route53tasks()


class TestRoute53Tasks(TestRoute53TasksSetup):
    def test_createBatchSets_resolve(self):
        new = [
            {
                "Name": "new.test.records",
                "ResourceRecords": [
                    {
                        "Value": "new.records"
                    }
                ],
                "TTL": 300,
                "Type": "CNAME"
            },
            {
                "Name": "same.test.records",
                "ResourceRecords": [
                    {
                        "Value": "ns1.test.records."
                    },
                    {
                        "Value": "ns2.test.records."
                    },
                    {
                        "Value": "ns3.test.records."
                    },
                    {
                        "Value": "ns4.test.records."
                    }
                ],
                "TTL": 300,
                "Type": "NS"
            }
        ]
        current = [
            {
                "Name": "delete.test.records",
                "ResourceRecords": [
                    {
                        "Value": "old.records"
                    }
                ],
                "TTL": 300,
                "Type": "CNAME"
            },
            {
                "Name": "same.test.records",
                "ResourceRecords": [
                    {
                        "Value": "ns1.test.records."
                    },
                    {
                        "Value": "ns2.test.records."
                    },
                    {
                        "Value": "ns3.test.records."
                    },
                    {
                        "Value": "ns4.test.records."
                    }
                ],
                "TTL": 300,
                "Type": "NS"
            }
        ]
        assertupsertbatch = [
            {
                "Name": "new.test.records",
                "ResourceRecords": [
                    {
                        "Value": "new.records"
                    }
                ],
                "TTL": 300,
                "Type": "CNAME"
            }
        ]
        assertdeletebatch = [
            {
                "Name": "delete.test.records",
                "ResourceRecords": [
                    {
                        "Value": "old.records"
                    }
                ],
                "TTL": 300,
                "Type": "CNAME"
            }
        ]
        assertstablebatch = [
            {
                "Name": "same.test.records",
                "ResourceRecords": [
                    {
                        "Value": "ns1.test.records."
                    },
                    {
                        "Value": "ns2.test.records."
                    },
                    {
                        "Value": "ns3.test.records."
                    },
                    {
                        "Value": "ns4.test.records."
                    }
                ],
                "TTL": 300,
                "Type": "NS"
            }
        ]
        upsertbatch, deletebatch, stablebatch = self.dnstasks.createBatchSets(new, current)
        self.assertEquals(upsertbatch, assertupsertbatch)
        self.assertEquals(deletebatch, assertdeletebatch)
        self.assertEquals(stablebatch, assertstablebatch)
