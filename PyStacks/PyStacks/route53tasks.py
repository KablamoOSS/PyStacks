import sys
import logging
import route53
import dns.resolver
import socket
import output
import zonefile
import json
import pprint
import time
from botocore.exceptions import ClientError
from jsonschema.exceptions import ValidationError, SchemaError
from jsonschema import validate


class route53tasks:

    def __init__(self):
        pass

    def validateNameServers(self, zone, session, _logging=None):
        awsdns = route53.route53(session)
        publicResolver = dns.resolver.Resolver()
        route53Resolver = dns.resolver.Resolver()
        inconsistent = False
        publicResolver.nameservers = ['8.8.8.8']
        try:
            route53Resolver.nameservers = [socket.gethostbyname(awsdns.getNameServers(awsdns.getZoneID(zone + '.')[0]["Id"].split('/hostedzone/')[1])[0])]
        except ClientError as err:
            print "Error setting Resolver to Delegation Set"
            logging.warn(err)
            sys.exit(1)
        try:
            records = awsdns.listRecords(awsdns.getZoneID(zone + '.')[0]["Id"].split('/hostedzone/')[1])
        except ClientError as err:
            print "Error retriving records for Zone:" + zone
            logging.warn(err)
            sys.exit(1)
        for record in records:
            if _logging:
                print "Record Name: " + record["Name"]
                print "Record Type: " + record["Type"]
            try:
                public = publicResolver.query(record["Name"], record["Type"])
                aws = route53Resolver.query(record["Name"], record["Type"])
            except ClientError as err:
                print "Error resolving records for record:" + record
                logging.warn(err)
                sys.exit(1)
            publicrecs = [x for x in public]
            awsrecs = [x for x in aws]
            if publicrecs != awsrecs:
                if record["Name"] == zone and (record["Type"] == "SOA" or record["Type"] == "NS"):
                    inconsistent = True
                print output.boxwrap(record["Name"] + " " + record["Type"])
                print "Public:"
                print publicrecs
                print "AWS:"
                print awsrecs
        if inconsistent:
            print "Differences Exist for Zone: " + zone

    def validateJSONZoneFiles(self, path="ci", schema="route53.schema.json", zone=None, logoutput=None):
        JSONZoneFiles = zonefile.getJSONZoneFilelist()
        invalid = False
        for file in JSONZoneFiles:
            try:
                validate(json.loads(zonefile.loadJSONZoneFile(file=file)), json.loads(zonefile.getJSONSchema(folderpath=path, file=schema)))
            except ClientError as err:
                print "Error attempting validation process for: " + file
                if logoutput:
                    logging.warn(err)
                sys.exit(1)
            except ValidationError as ve:
                print "Error in: " + file
                if logoutput:
                    logging.warn(ve)
                invalid = True
            except SchemaError as serrs:
                print "Schema errors in:" + schema
                if logoutput:
                    logging.warn(serrs)
                invalid = True
        if invalid:
            print "Validation Errors"
            sys.exit(1)

    def createBatchSets(self, new, current):
        if isinstance(new, list) and isinstance(current, list):
            upsertbatch = [x for x in new if x not in current]
            deletebatch = [x for x in current if [x["Name"], x["Type"]] not in ([y["Name"], y["Type"]] for y in new)]
            stablebatch = [x for x in new if x in current]

            return upsertbatch, deletebatch, stablebatch
        else:
            print "Batch Sets are not Lists, please check input into createBatchSets"
            sys.exit(1)

    def upsertJSONzoneFile(self, zonename, session, comment, noop=True, logoutput=None, delete=False):
        dns = route53.route53(session)
        zoneid = dns.getZoneID(zonename + ".")
        jsonconfig = zonefile.loadJSONZoneFile(zonename)
        route53config = dns.listRecords(zoneid[0]["Id"].split('/hostedzone/')[1])

        upsertbatch, deletebatch, stablebatch = self.createBatchSets(new=json.loads(jsonconfig), current=route53config)
        print "New Records: (" + str(len(upsertbatch)) + ")"
        print json.dumps(upsertbatch, sort_keys=True, indent=4, separators=(',', ': '))
        print "--------------"
        if delete:
            print "Delete Records: (" + str(len(deletebatch)) + ")"
            print json.dumps(deletebatch, sort_keys=True, indent=4, separators=(',', ': '))
            print "--------------"
        print "Unchanged Records: (" + str(len(stablebatch)) + ")"
        if logoutput:
            print json.dumps(stablebatch, sort_keys=True, indent=4, separators=(',', ': '))
        print "--------------"
        if noop:
            pprint.pprint("NOOP in effect, no changes made.")
        else:
            if len(upsertbatch) > 0:
                batchset = dns.createChangeBatch(batchset=json.dumps(upsertbatch), action="UPSERT", comment="UPSERT for " + comment)
                try:
                    dns.createRecord(changebatch=batchset, hostzoneid=zoneid[0]["Id"].split('/hostedzone/')[1])
                except ClientError as err:
                    logging.warn(err)
                    sys.exit(1)
            if delete and len(deletebatch) > 0:
                batchset = dns.createChangeBatch(batchset=json.dumps(deletebatch), action="DELETE", comment="DELETE for " + comment)
                try:
                    dns.createRecord(changebatch=batchset, hostzoneid=zoneid[0]["Id"].split('/hostedzone/')[1])
                except ClientError as err:
                    logging.warn(err)
                    sys.exit(1)

    def cnameSwap(self, name, value1, value2, zonename, session, comment, ttl=300):
        dns = route53.route53(session)
        zoneid = dns.getZoneID(zonename + ".")
        print 'zoneid:'
        pprint.pprint(zoneid)
        # find the current cname value
        try:
            records = dns.resolver.query(name, 'CNAME')
        except:
            records = []
        targets = [str(x.target) for x in records]
        # swap the values
        newValue = value1
        if value1 in targets:
            newValue = value2
        print 'new cname: ' + newValue
        # Upsert the cname record
        record = {
            'Type': 'CNAME',
            'Name': name,
            'ResourceRecords': [{'Value': newValue}],
            'TTL': ttl
        }
        batchset = dns.createChangeBatch(batchset=json.dumps([record]), action="UPSERT", comment="UPSERT for " + comment)
        try:
            dns.createRecord(changebatch=batchset, hostzoneid=zoneid[0]["Id"].split('/hostedzone/')[1])
        except ClientError as err:
            logging.warn(err)
            sys.exit(1)

    def upsertBINDzoneFile(ctx, session, zonename=None, folder='dns', logoutput=None):
        dns = route53.route53(session)
        for file in zonefile.getZoneFilelist(folder, zonename):
            config = zonefile.loadZoneFile(file, folder)
            zoneid = dns.getZoneID(file + ".")

            if len(dns.listRecords(zoneid[0]["Id"].split('/hostedzone/')[1])) < 3:
                zone = zonefile.parseZone(zonedata=config, zonename=file, logoutput=logoutput)
                records = zonefile.dedup(seq=zone, logoutput=logoutput)
                jsonrecords = json.dumps(zonefile.buildfromzone(records))
                batchset = dns.createChangeBatch(batchset=jsonrecords, action="UPSERT", comment="automated upload of " + file + " zone file.")
                try:
                    dns.createRecord(changebatch=batchset, hostzoneid=zoneid[0]["Id"].split('/hostedzone/')[1])
                except ClientError as err:
                    logging.warn(err)
                    if 'InvalidChangeBatch' in str(err):
                        print json.dumps(batchset, sort_keys=True, indent=4, separators=(',', ': '))
                    sys.exit(1)
                print "Zone " + file + " imported successfully."
            else:
                print "Zone " + file + " isn't empty."
            sys.stdout.flush()

    def readBINDzoneFile(ctx, zonename, region='dns', logoutput=None):
        config = zonefile.loadZoneFile(zonename, region)
        zone = zonefile.parseZone(zonedata=config, zonename=zonename)
        records = zonefile.dedup(zone)
        jsonrecords = zonefile.buildfromzone(records)
        print json.dumps(jsonrecords, sort_keys=True, indent=4, separators=(',', ': '))

    def createDNSzoneFile(ctx, session, zonename=None, logoutput=None):
        dns = route53.route53(session)
        if zonename:
            zoneids = dns.getZoneID(zonename + ".")
        else:
            zoneids = dns.getZoneID()
        if logoutput:
            pprint.pprint(zoneids)
        for zoneid in zoneids:
            records = dns.listRecords(zoneid["Id"].split('/hostedzone/')[1])
            zonefile.writezone(records, zoneid["Name"])
            pprint.pprint("Writing out " + zoneid['Name'] + "zone file.")

    def createDNSzone(ctx, session, folder='dns', zonename=None, logoutput=None):
        dns = route53.route53(session)
        delegationset = dns.getDelegationSets()
        caller = None
        for zone in zonefile.getZoneFilelist(folder, zonename):
            caller = zone + " created " + time.strftime("%H:%M:%S") + "-" + time.strftime("%d/%m/%Y")
            try:
                dns.createZone(zonename=zone, caller=caller, setid=delegationset[0]["Id"])
            except ClientError as err:
                logging.warn(err)
                if 'ConflictingDomainExists' in str(err):
                    print 'Domain: ' + zone + ' conflict: Already Exists'
                else:
                    sys.exit(1)
            print caller

    def createDNSDelegationSet(ctx, session, region='ap-southeast-2', logoutput=None):
        dns = route53.route53(session)
        caller = "Delegation Set created " + time.strftime("%H:%M:%S") + "-" + time.strftime("%d/%m/%Y")
        try:
            response = dns.createDelegationSet(caller=caller)
        except ClientError as err:
            logging.warn(err)
            sys.exit(1)
        print response

    def getRRset(ctx, zonename, session):
        dns = route53.route53(session)
        zoneid = dns.getZoneID(zonename + ".")
        records = dns.listRecords(zoneid[0]["Id"].split('/hostedzone/')[1])
        print json.dumps(records, sort_keys=True, indent=4, separators=(',', ': '))
