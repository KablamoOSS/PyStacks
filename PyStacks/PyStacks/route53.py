import json
import pprint


class route53:

    def __init__(self, session):
        self.dnsClient = session.client('route53')

    def waiterRecordSet(self, session, Id):
        waiter = self.dnsClient.get_waiter('resource_record_sets_changed')
        waiter.wait(Id=Id)

    def listRecords(self, zoneid, logging=None):
        recordset = []
        response = self.dnsClient.list_resource_record_sets(
            HostedZoneId=zoneid)
        recordset.extend(response["ResourceRecordSets"])
        while response["IsTruncated"]:
            response = self.dnsClient.list_resource_record_sets(
                HostedZoneId=zoneid,
                StartRecordName=response["NextRecordName"],
                StartRecordType=response["NextRecordType"])
            recordset.extend(response["ResourceRecordSets"])
        return recordset

    def getZoneID(self, zonename=None, logging=None):
        zoneids = []
        response = self.dnsClient.list_hosted_zones()
        if logging == 'Full':
            pprint.pprint(response)
        zoneids.extend(response["HostedZones"])
        while response["IsTruncated"]:
            response = self.dnsClient.list_hosted_zones(
                Marker=response["Marker"])
            zoneids.extend(response["HostedZones"])
        if logging:
            pprint.pprint(response)
        if zonename:
            for x in zoneids:
                if x["Name"] == zonename:
                    return [x]
        else:
            return zoneids

    def getDelegationSets(self):
        response = self.dnsClient.list_reusable_delegation_sets()
        sets = response["DelegationSets"]
        print(json.dumps(sets))
        return sets

    def getNameServers(self, setid):
        response = self.dnsClient.get_hosted_zone(Id=setid)
        return response["DelegationSet"]["NameServers"]

    def createDelegationSet(self, caller):
        self.dnsClient.create_reusable_delegation_set(
            CallerReference='string'
        )

    def createZone(self, zonename, caller, setid):
        self.dnsClient.create_hosted_zone(
            Name=zonename, CallerReference=caller, HostedZoneConfig={'Comment': caller}, DelegationSetId=setid
        )

    def createRecord(self, changebatch, hostzoneid, logging=None):
        if logging:
            pprint.pprint(changebatch)
            pprint.pprint(hostzoneid)
        self.dnsClient.change_resource_record_sets(
            HostedZoneId=hostzoneid,
            ChangeBatch=changebatch
        )

    def createChangeBatch(self, batchset, action, comment, logging=None):
        changeset = {}
        if logging:
            pprint.pprint(batchset)
        recordset = json.loads(batchset)
        changeset["Comment"] = comment
        changeset["Changes"] = []
        for x in recordset:
            temprec = {}
            temprec["Action"] = action
            temprec["ResourceRecordSet"] = x
            changeset["Changes"].append(temprec)

        if logging:
            pprint.pprint(changeset)
        return changeset
