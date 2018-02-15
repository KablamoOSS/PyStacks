import unittest
import time
import json

from mock import MagicMock

from PyStacks.PyStacks.route53 import route53


class TestRoute53Setup(unittest.TestCase):
    def setUp(self):
        self.mocksession = MagicMock()
        self.mockcfClient = MagicMock()
        self.mockdnsClient = MagicMock()

        self.mocksession.client.return_value = self.mockdnsClient

        self.dns = route53(self.mocksession)


class TestRoute53(TestRoute53Setup):
    def test_listRecords_empty_return(self):
        self.mockdnsClient.list_resource_record_sets.return_value = {
            'IsTruncated': False,
            'ResourceRecordSets': []
        }

        actual = self.dns.listRecords(zoneid='something')
        self.mockdnsClient.list_resource_record_sets.assert_called_with(
            HostedZoneId='something')
        self.assertEqual([], actual)

    def test_getDelegationSets(self):
        self.dns.dnsClient.list_reusable_delegation_sets = MagicMock()
        self.dns.dnsClient.list_reusable_delegation_sets.return_value = {
            'DelegationSets': 'MyLittleDelegationSet'
        }

        sets = self.dns.getDelegationSets()
        self.assertEquals(sets, 'MyLittleDelegationSet')

    def test_getNameServers(self):
        self.dns.dnsClient.get_hosted_zone = MagicMock()
        self.dns.dnsClient.get_hosted_zone.return_value = {
            'HostedZone': {
                'Id': '/HostedZone/TestZone',
                'Name': 'MyLittleZone',
                'CallerReference': 'DummyCaller',
                'Config': {
                    'Comment': 'Test',
                    'PrivateZone': False
                },
                'ResourceRecordSetCount': 123
            },
            'DelegationSet': {
                'Id': 'string',
                'CallerReference': 'string',
                'NameServers': [
                    'MyLittleNameServer'
                ]
            }
        }

        sets = self.dns.getNameServers('MyLittleDelegationSetId')
        self.assertEquals(['MyLittleNameServer'], sets)

    def test_listRecords_multiple_return(self):
        self.mockdnsClient.list_resource_record_sets.return_value = {
            'IsTruncated': False,
            'ResourceRecordSets': ['terry', 'was', 'here']
        }

        actual = self.dns.listRecords(zoneid='something')

        self.mockdnsClient.list_resource_record_sets.assert_called_with(
            HostedZoneId='something')
        self.assertEqual(['terry', 'was', 'here'], actual)

    def test_getZoneID_returns_false_if_no_match(self):
        self.mockdnsClient.list_hosted_zones.return_value = {
            'HostedZones': [],
            'IsTruncated': False
        }

        actual = self.dns.getZoneID(zonename='something')

        self.mockdnsClient.list_hosted_zones.assert_called_with()
        self.assertFalse(actual)

    def test_getZoneID_returns_only_first_match(self):
        self.mockdnsClient.list_hosted_zones.return_value = {
            'HostedZones': [
                {
                    'Id': '/hostedzone/origin',
                    'Name': 'something',
                },
                {
                    'Id': '/hostedzone/nothere',
                    'Name': 'something',
                },
            ],
            'IsTruncated':
            False
        }

        actual = self.dns.getZoneID(zonename='something')

        self.mockdnsClient.list_hosted_zones.assert_called_with()
        self.assertEqual([{
            'Id': '/hostedzone/origin',
            'Name': 'something'
        }], actual)

    def test_getZoneID_returns_first_match(self):
        self.mockdnsClient.list_hosted_zones.return_value = {
            'HostedZones': [
                {
                    'Id': '/hostedzone/origin',
                    'Name': 'thisshouldnotmatch',
                },
                {
                    'Id': '/hostedzone/bingowashisnameo',
                    'Name': 'something',
                },
            ],
            'IsTruncated':
            False
        }

        actual = self.dns.getZoneID(zonename='something')

        self.mockdnsClient.list_hosted_zones.assert_called_with()
        self.assertEqual([{
            'Id': '/hostedzone/bingowashisnameo',
            'Name': 'something'
        }], actual)

    def test_getZoneID_returns_all(self):
        self.mockdnsClient.list_hosted_zones.return_value = {
            'HostedZones': [
                {
                    'Id': '/hostedzone/origin',
                    'Name': 'thisshouldnotmatch',
                },
                {
                    'Id': '/hostedzone/bingowashisnameo',
                    'Name': 'something',
                },
            ],
            'IsTruncated':
            False
        }

        actual = self.dns.getZoneID(zonename='doesnotexist')

        self.mockdnsClient.list_hosted_zones.assert_called_with()
        self.assertEqual(None, actual)

    def test_createZone(self):
        self.dns.dnsClient = MagicMock()
        self.dns.dnsClient.create_hosted_zone = MagicMock()
        caller = 'MyLittleZoneName' + " created " + \
            time.strftime("%H:%M:%S") + "-" + time.strftime("%d/%m/%Y")
        self.dns.createZone('MyLittleZoneName', caller, 'MyLittleSetId')

        self.dns.dnsClient.create_hosted_zone.assert_called_with(
            Name='MyLittleZoneName', CallerReference=caller, HostedZoneConfig={'Comment': caller}, DelegationSetId='MyLittleSetId'
        )
        self.assertEqual(self.dns.dnsClient.create_hosted_zone.call_count, 1)

    def test_createRecord(self):
        self.dns.dnsClient = MagicMock()
        self.dns.dnsClient.change_resource_record_sets = MagicMock()

        self.dns.createRecord(
            changebatch='MyLittleChangeBatch',
            hostzoneid='MyLittleHostZoneId',
        )
        self.dns.dnsClient.change_resource_record_sets.assert_called_with(
            HostedZoneId='MyLittleHostZoneId',
            ChangeBatch='MyLittleChangeBatch',
        )

    def test_createRecord_with_logging(self):
        self.dns.dnsClient = MagicMock()
        self.dns.dnsClient.change_resource_record_sets = MagicMock()

        self.dns.createRecord(
            changebatch='MyLittleChangeBatch',
            hostzoneid='MyLittleHostZoneId',
            logging=True
        )
        self.dns.dnsClient.change_resource_record_sets.assert_called_with(
            HostedZoneId='MyLittleHostZoneId',
            ChangeBatch='MyLittleChangeBatch'
        )

    def test_createChangeBatch(self):
        batchset = json.dumps([
            {'MyLittleBatchSetId': 'MyLittleBatchSet'}
        ])

        changeset = self.dns.createChangeBatch(
            batchset=batchset,
            action='MyLittleAction',
            comment='MyLittleComment'
        )

        changeset_expected = {
            'Comment': 'MyLittleComment',
            'Changes': [
                {
                    'Action': 'MyLittleAction',
                    'ResourceRecordSet': {
                        'MyLittleBatchSetId': 'MyLittleBatchSet'
                    }
                }
            ]
        }
        self.assertEquals(changeset, changeset_expected)


if __name__ == '__main__':
    unittest.main()
