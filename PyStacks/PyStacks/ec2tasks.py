import logging
import sys
import ec2
import json
from botocore.exceptions import ClientError


class ec2tasks:

    def __init__(self):
        pass

    def createVPCPeering(self, session, config, noop=False, logoutput=None):
        ec2client = ec2.ec2(session)
        for peer, values in config["resources"]["vpcpeer"].iteritems():
            print peer
            if logoutput:
                print "Peer Account:" + values["peeraccount"]
                print "Peer VPC ID:" + values["peervpcid"]
                print "VPC ID:" + values["vpcid"]
                print "----------------------------"
            try:
                ec2client.createVPCpeering(peeraccount=values["peeraccount"], peervpcid=values["peervpcid"], vpcid=values["vpcid"], noop=noop)
            except ClientError as err:
                logging.warn(err)
                sys.exit(1)

    def getVPCPeering(self, session, filtername=None, filtervalues=None, vpcpeerid=[], noop=False, logoutput=None):
        ec2client = ec2.ec2(session)
        filters = None
        if filtername and filtervalues:
            filters = self.buildFilters(name=filtername, filters=filtervalues)
        try:
            peers = ec2client.getVPCpeering(filters=filters, vpcpeerid=vpcpeerid, noop=noop)
        except ClientError as err:
            logging.warn(err)
            sys.exit(1)

        print json.dumps(peers, default=str, sort_keys=True, indent=4, separators=(',', ': '))

    def acceptVPCPeering(self, session, vpcpeerid=None, noop=False, logoutput=None):
        ec2client = ec2.ec2(session)
        peers = ec2client.getVPCpeering(vpcpeerid=vpcpeerid, noop=noop)
        for peer in peers["VpcPeeringConnections"]:
            vpcpeerclient = ec2.ec2vpcpeer(session=session, identifier=peer["VpcPeeringConnectionId"])
            status = vpcpeerclient.getStatus()
            if logoutput:
                print "VPC Peer: " + peer["VpcPeeringConnectionId"] + " has a status of: " + status["Code"]
            if status["Code"] == "pending-acceptance":
                try:
                    vpcpeerclient.allowVPCpeeringDNS(peerid=peer["VpcPeeringConnectionId"], options=self.buildVPCPeerOptions(), noop=noop)
                except ClientError as err:
                    logging.warn(err)
                try:
                    vpcpeerclient.accept(noop=noop)
                except ClientError as err:
                    logging.warn(err)
                status = vpcpeerclient.getStatus()
            if status["Code"] == "active":
                self.addPeertoRoutetable(ec2client=ec2client, peer=peer, vpcpeerclient=vpcpeerclient, role='Accepter', noop=noop, logoutput=logoutput)

    def verifyVPCPeering(self, session, vpcpeerid=None, noop=False, logoutput=None):
        ec2client = ec2.ec2(session)
        peers = ec2client.getVPCpeering(vpcpeerid=vpcpeerid, noop=noop)
        for peer in peers["VpcPeeringConnections"]:
            vpcpeerclient = ec2.ec2vpcpeer(session=session, identifier=peer["VpcPeeringConnectionId"])
            status = vpcpeerclient.getStatus()
            if status["Code"] == "pending-acceptance":
                print "VPC Peer: " + peer["VpcPeeringConnectionId"] + " has a status of: " + status["Code"] + " please accept the connection with its peer VPC"
            if status["Code"] == "active":
                self.addPeertoRoutetable(ec2client=ec2client, peer=peer, vpcpeerclient=vpcpeerclient, role='Requester', noop=noop, logoutput=logoutput)

    def addPeertoRoutetable(self, ec2client, peer, vpcpeerclient, role, noop=False, logoutput=None):
        status = vpcpeerclient.getStatus()
        if role == "Accepter":
            localinfo = vpcpeerclient.getAccepterInfo()
            peerinfo = vpcpeerclient.getRequesterInfo()
        else:
            localinfo = vpcpeerclient.getRequesterInfo()
            peerinfo = vpcpeerclient.getAccepterInfo()

        if status["Code"] == "active":
            routetables = ec2client.getRouteTables(filters=self.buildFilters(name="vpc-id", filters=[localinfo["VpcId"]]))
            for rt in routetables["RouteTables"]:
                if peerinfo["CidrBlock"] not in self.buildRoutelist(routes=rt):
                    try:
                        ec2client.createRouteVPCPeer(cidr=peerinfo["CidrBlock"], routetableid=rt["RouteTableId"], peerid=peer["VpcPeeringConnectionId"], noop=noop)
                        print "Route: " + peerinfo["CidrBlock"] + " added to Route Table: " + rt["RouteTableId"]
                    except ClientError as err:
                        logging.warn(err)
                else:
                    print "Route: " + peerinfo["CidrBlock"] + " already exists in Route Table: " + rt["RouteTableId"]

    def createVPNConnections(self, session, config, noop=False, logoutput=None):
        ec2client = ec2.ec2(session)
        cgws = self.getGustomerGateways(session=session)["CustomerGateways"]
        for peer, values in config["resources"]["vpcpeer"].iteritems():
            if values["ipaddress"] not in [x for x in cgws["IpAddress"] if cgws["State"] == "available"]:
                if noop:
                    print "VPN Connection: " + peer + " is not available"
                else:
                    try:
                        _vpngw = ec2client.create_vpn_gateway()
                    except ClientError as err:
                        logging.warn(err)
                    try:
                        _cgw = ec2client.create_customer_gateway(bgpasn=values["bgpasn"], publicip=values["publicip"])
                    except ClientError as err:
                        logging.warn(err)
                    try:
                        _vpnconnection = ec2client.create_vpn_connection(
                            cgwid=_cgw["CustomerGatewayId"],
                            vpngwid=_vpngw["VpnGatewayId"],
                            Options=self.buildVPNRoutingOptions(),
                            noop=noop
                        )
                    except ClientError as err:
                        logging.warn(err)

                    print _vpnconnection

    def getVPCs(self, session=None, vpcids=None, noop=False, logoutput=None):
        ec2client = ec2.ec2(session)
        vpcs = ec2client.getVPCs(vpcids=vpcids, noop=noop)
        if logoutput:
            print json.dumps(vpcs, default=str, sort_keys=True, indent=4, separators=(',', ': '))

        return vpcs

    def getRoutetables(self, session=None, routetableids=None, noop=False, logoutput=None):
        ec2client = ec2.ec2(session)
        routetables = ec2client.getRouteTables(routetableids=routetableids, noop=noop)
        if logoutput:
            print json.dumps(routetables, default=str, sort_keys=True, indent=4, separators=(',', ': '))

        return routetables

    def getSubnets(self, session=None, subnetids=None, noop=False, logoutput=None):
        ec2client = ec2.ec2(session)
        subnets = ec2client.getSubnets(subnetids=subnetids, noop=noop)
        if logoutput:
            print json.dumps(subnets, default=str, sort_keys=True, indent=4, separators=(',', ': '))

        return subnets

    def getVPNConnections(self, session=None, vpnids=None, noop=False, logoutput=None):
        ec2client = ec2.ec2(session)
        vpns = ec2client.getVPNConnections(vpnids=vpnids, noop=noop)
        if logoutput:
            print json.dumps(vpns, default=str, sort_keys=True, indent=4, separators=(',', ': '))

        return vpns

    def getVPNGateways(self, session=None, vpngwids=None, noop=False, logoutput=None):
        ec2client = ec2.ec2(session)
        vpngws = ec2client.getVPNGateways(vpngwids=vpngwids, noop=noop)
        if logoutput:
            print json.dumps(vpngws, default=str, sort_keys=True, indent=4, separators=(',', ': '))

        return vpngws

    def buildRoutelist(self, routes):
        routelist = []
        for route in routes["Routes"]:
            routelist.append(route["DestinationCidrBlock"])

        return routelist

    def buildFilters(self, name, filters):
        obj = {}
        filterlist = []
        obj["Name"] = name
        for x in filters:
            filterlist.append(x)
        obj["Values"] = filterlist

        return [obj]

    def buildVPCPeerOptions(self, allow=True):
        options = {
            'AllowDnsResolutionFromRemoteVpc': allow
        }

        return options

    def buildVPNRoutingOptions(self, staticroutes=False):
        options = {
            'StaticRoutesOnly': staticroutes
        }

        return options
