# import os
import unittest
import pprint
# import json

from PyStacks.PyStacks.zonefile import loadZoneFile, parseZone, dedup, buildfromzone, loadJSONZoneFile


class TestZonefile(unittest.TestCase):

    def test_loadzonefile_ignores_comments_replaces_spaces_replaces_IN(self):
        config = loadZoneFile(file_name='test', region='global')

        self.assertEqual(10, len(config))

        for x in config:
            self.assertTrue('  ' not in x)
            self.assertTrue(' IN ' not in x)

    def test_loadJSONZoneFile(self):
        loadJSONZoneFile('test')
        # Not sure if this function can be tested. It appears
        # to read a json file, and then stringify it

    def test_loadJSONZoneFile_blank_file(self):
        with self.assertRaises(Exception):
            loadJSONZoneFile('test_blank')

    # zonefile.parseZone
    def test_parseZone(self):
        zonefile = loadZoneFile(file_name='test', region='global')
        zone = parseZone(zonedata=zonefile, zonename='testzone')

        # A records
        self.assertEqual(zone[0][0], 'example.com.')
        self.assertEqual(zone[0][1], '300')
        self.assertEqual(zone[0][2], 'A')
        self.assertEqual(zone[0][3], '8.8.8.8')

        self.assertEqual(zone[1][0], 'skypeweb.example.com.')
        self.assertEqual(zone[1][1], '300')
        self.assertEqual(zone[1][2], 'A')
        self.assertEqual(zone[1][3], '8.8.8.8')

        # NS records
        self.assertEqual(zone[2][0], 'example.com.')
        self.assertEqual(zone[2][1], '300')
        self.assertEqual(zone[2][2], 'NS')
        self.assertEqual(zone[2][3], 'ns.rackspace.com.')

        self.assertEqual(zone[3][0], 'example.com.')
        self.assertEqual(zone[3][1], '300')
        self.assertEqual(zone[3][2], 'NS')
        self.assertEqual(zone[3][3], 'ns2.rackspace.com.')

        # MX Records
        self.assertEqual(zone[4][0], 'example.com.')
        self.assertEqual(zone[4][1], '300')
        self.assertEqual(zone[4][2], 'MX')
        self.assertEqual(zone[4][3], '10')
        self.assertEqual(zone[4][4], 'cluster5.us.messagelabs.com.')

        self.assertEqual(zone[5][0], 'example.com.')
        self.assertEqual(zone[5][1], '300')
        self.assertEqual(zone[5][2], 'MX')
        self.assertEqual(zone[5][3], '20')
        self.assertEqual(zone[5][4], 'cluster5a.us.messagelabs.com.')

        # TXT Records
        self.assertEqual(zone[6][0], 'example.com.')
        self.assertEqual(zone[6][1], '300')
        self.assertEqual(zone[6][2], 'TXT')
        self.assertEqual(zone[6][3], '"MS=msexample"')

        self.assertEqual(zone[7][0], 'example.com.')
        self.assertEqual(zone[7][1], '300')
        self.assertEqual(zone[7][2], 'TXT')
        self.assertEqual(zone[7][3], '"EXAMPLE"')

        # SRV Records
        self.assertEqual(zone[8][0], 'example.com.')
        self.assertEqual(zone[8][1], '300')
        self.assertEqual(zone[8][2], 'SRV')
        self.assertEqual(zone[8][3], '0 5 5060 sipserver.example.com.')
        self.assertEqual(zone[8][4], '5')
        self.assertEqual(zone[8][5], '5060')
        self.assertEqual(zone[8][6], 'sipserver.example.com.')

    def test_dedup(self):

        zone = [
            ['example.com.', '300', 'A', '8.8.8.8', ''],
            ['example.com.', '300', 'A', '8.8.4.4', ''],
            ['example.com.', '300', 'A', '10.0.0.0', ''],
            ['skypeweb.example.com.', '300', 'A', '8.8.8.8', ''],
            ['example.com.', '300', 'NS', 'ns.rackspace.com.', ''],
            ['example.com.', '300', 'NS', 'ns2.rackspace.com.', ''],
            ['example.com.', '300', 'MX', '10', 'cluster5.us.messagelabs.com.', ''],
            ['example.com.', '300', 'MX', '20', 'cluster5a.us.messagelabs.com.', ''],
            ['example.com.', '300', 'TXT', '"TextRecord1"'],
            ['example.com.', '300', 'TXT', '"TextRecord2"'],
            ['example.com.', '300', 'SRV', '0 5 5060 sipserver.example.com.', '5',
                '5060', 'sipserver.example.com.', '']
        ]

        deduped = dedup(zone)

        # collate the types in the deduped zone
        seen_types = set()
        for record in deduped:
            record_type = record[0] + record[2]
            if record_type not in seen_types:
                seen_types.add(record_type)
            else:
                pprint.pprint(seen_types)
                self.fail('Duplicate record type found:')

        # Hard coded checks to confirm the output of the dedup function

        # A records
        self.assertEqual(deduped[0][0], 'example.com.')
        self.assertEqual(deduped[0][1], '300')
        self.assertEqual(deduped[0][2], 'A')
        self.assertEqual(deduped[0][3][0], '8.8.8.8')
        self.assertEqual(deduped[0][3][1], '8.8.4.4')
        self.assertEqual(deduped[0][3][2], '10.0.0.0')

        self.assertEqual(deduped[1][0], 'skypeweb.example.com.')
        self.assertEqual(deduped[1][1], '300')
        self.assertEqual(deduped[1][2], 'A')
        self.assertEqual(deduped[1][3][0], '8.8.8.8')

        # NS records
        self.assertEqual(deduped[2][0], 'example.com.')
        self.assertEqual(deduped[2][1], '300')
        self.assertEqual(deduped[2][2], 'NS')
        self.assertEqual(deduped[2][3][0], 'ns.rackspace.com.')
        self.assertEqual(deduped[2][3][1], 'ns2.rackspace.com.')

        # MX records
        self.assertEqual(deduped[3][0], 'example.com.')
        self.assertEqual(deduped[3][1], '300')
        self.assertEqual(deduped[3][2], 'MX')
        self.assertEqual(deduped[3][3][0], '10 cluster5.us.messagelabs.com.')
        self.assertEqual(deduped[3][3][1], '20 cluster5a.us.messagelabs.com.')
        self.assertEqual(deduped[3][4], 'cluster5.us.messagelabs.com.')

        # TXT records
        self.assertEqual(deduped[4][0], 'example.com.')
        self.assertEqual(deduped[4][1], '300')
        self.assertEqual(deduped[4][2], 'TXT')
        self.assertEqual(deduped[4][3][0], '"TextRecord1"')
        self.assertEqual(deduped[4][3][1], '"TextRecord2"')

        # SRV records
        self.assertEqual(deduped[5][0], 'example.com.')
        self.assertEqual(deduped[5][1], '300')
        self.assertEqual(deduped[5][2], 'SRV')
        self.assertEqual(deduped[5][3][0], '0 5 5060 sipserver.example.com.')
        self.assertEqual(deduped[5][4], '5')
        self.assertEqual(deduped[5][5], '5060')
        self.assertEqual(deduped[5][6], 'sipserver.example.com.')

    # zonefile.buildfromzone
    def test_buildfromzone(self):
        config = loadZoneFile(file_name='test', region='global')
        zone = parseZone(zonedata=config, zonename='stack')
        records = dedup(zone)
        jsonrecords = buildfromzone(records)

        # A records
        self.assertEqual(jsonrecords[0]['Name'], 'example.com.')
        self.assertEqual(jsonrecords[0]['ResourceRecords'][0]['Value'],
                         '8.8.8.8')
        self.assertEqual(jsonrecords[0]['TTL'], 300)
        self.assertEqual(jsonrecords[0]['Type'], 'A')

        self.assertEqual(jsonrecords[1]['Name'], 'skypeweb.example.com.')
        self.assertEqual(jsonrecords[1]['ResourceRecords'][0]['Value'],
                         '8.8.8.8')
        self.assertEqual(jsonrecords[1]['TTL'], 300)
        self.assertEqual(jsonrecords[1]['Type'], 'A')

        # NS records
        self.assertEqual(jsonrecords[2]['Name'], 'example.com.')
        self.assertEqual(jsonrecords[2]['ResourceRecords'][0]['Value'],
                         'ns.rackspace.com.')
        self.assertEqual(jsonrecords[2]['ResourceRecords'][1]['Value'],
                         'ns2.rackspace.com.')
        self.assertEqual(jsonrecords[2]['TTL'], 300)
        self.assertEqual(jsonrecords[2]['Type'], 'NS')

        # MX Records
        self.assertEqual(jsonrecords[3]['Name'], 'example.com.')
        self.assertEqual(jsonrecords[3]['ResourceRecords'][0]['Value'],
                         '10 cluster5.us.messagelabs.com.')
        self.assertEqual(jsonrecords[3]['ResourceRecords'][1]['Value'],
                         '20 cluster5a.us.messagelabs.com.')
        self.assertEqual(jsonrecords[3]['TTL'], 300)
        self.assertEqual(jsonrecords[3]['Type'], 'MX')

        # TXT Records
        self.assertEqual(jsonrecords[4]['Name'], 'example.com.')
        self.assertEqual(jsonrecords[4]['ResourceRecords'][0]['Value'],
                         '"MS=msexample"')
        self.assertEqual(jsonrecords[4]['ResourceRecords'][1]['Value'],
                         '"EXAMPLE"')
        self.assertEqual(jsonrecords[4]['TTL'], 300)
        self.assertEqual(jsonrecords[4]['Type'], 'TXT')

        # SRV Records
        self.assertEqual(jsonrecords[5]['Name'], 'example.com.')
        self.assertEqual(jsonrecords[5]['ResourceRecords'][0]['Value'],
                         '0 5 5060 sipserver.example.com.')
        self.assertEqual(jsonrecords[5]['TTL'], 300)
        self.assertEqual(jsonrecords[5]['Type'], 'SRV')


if __name__ == '__main__':
    unittest.main()
