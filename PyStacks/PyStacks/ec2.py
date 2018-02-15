class ec2:

    def __init__(self, session):
        self.ec2Client = session.client('ec2')

    def getSubnets(self, filters=None, subnetids=None, noop=False):
        if subnetids is None:
            subnetids = []
        if filters is None:
            filters = []
        print subnetids
        subnets = self.ec2Client.describe_subnets(
            Filters=filters,
            DryRun=noop,
            SubnetIds=subnetids
        )

        return subnets

    def getRouteTables(self, filters=None, routetableids=None, noop=False):
        if routetableids is None:
            routetableids = []
        if filters is None:
            filters = []
        routetables = self.ec2Client.describe_route_tables(
            Filters=filters,
            DryRun=noop,
            RouteTableIds=routetableids
        )

        return routetables

    def getVPCs(self, filters=None, vpcids=None, noop=False):
        if vpcids is None:
            vpcids = []
        if filters is None:
            filters = []
        vpcs = self.ec2Client.describe_vpcs(
            Filters=filters,
            DryRun=noop,
            VpcIds=vpcids
        )
        return vpcs

    def getVPCpeering(self, filters=None, vpcpeerid=None, noop=False):
        if vpcpeerid is None:
            vpcpeerid = []
        if filters is None:
            filters = []
        peers = self.ec2Client.describe_vpc_peering_connections(
            Filters=filters,
            DryRun=noop,
            VpcPeeringConnectionIds=vpcpeerid
        )
        return peers

    def getGustomerGateways(self, filters=None, cgwids=None, noop=False):
        if cgwids is None:
            cgwids = []
        if filters is None:
            filters = []
        cgws = self.ec2Client.describe_customer_gateways(
            Filters=filters,
            CustomerGatewayIds=cgwids,
            DryRun=noop
        )

        return cgws

    def getVPNConnections(self, filters=None, vpnids=None, noop=False):
        if vpnids is None:
            vpnids = []
        if filters is None:
            filters = []
        vpns = self.ec2Client.describe_vpn_connections(
            Filters=filters,
            VpnConnectionIds=vpnids,
            DryRun=noop
        )

        return vpns

    def getVPNGateways(self, filters=None, vpngwids=None, noop=False):
        if vpngwids is None:
            vpngwids = []
        if filters is None:
            filters = []
        vpngws = self.ec2Client.describe_vpn_gateways(
            Filters=filters,
            VpnGatewayIds=vpngwids,
            DryRun=noop
        )

        return vpngws

    def getTags(self, filters=None, noop=False):
        tags = []
        if filters is None:
            filters = []
        response = self.ec2Client.describe_tags(
            Filters=filters,
            DryRun=noop
        )
        tags.extend(response["Tags"])
        while "NextToken" in response:
            response = self.ec2Client.describe_tags(
                Filters=filters,
                DryRun=noop,
                NextToken=response["NextToken"]
            )
            tags.extend(response["Tags"])

        return tags

    def createVPCpeering(self, peeraccount, peervpcid, vpcid, noop=False):
        self.ec2Client.create_vpc_peering_connection(
            DryRun=noop,
            PeerOwnerId=peeraccount,
            PeerVpcId=peervpcid,
            VpcId=vpcid
        )

    def allowVPCpeeringDNS(self, peerid, options, noop=False):
        self.ec2Client.modify_vpc_peering_connection_options(
            DryRun=noop,
            AccepterPeeringConnectionOptions=options,
            RequesterPeeringConnectionOptions=options,
            VpcPeeringConnectionId=peerid
        )

    def deleteVPCpeering(self, peerid, vpcid, noop=False):
        self.ec2Client.delete_vpc_peering_connection(
            DryRun=noop,
            VpcPeeringConnectionId=peerid
        )

    def createRouteVPCPeer(self, cidr, routetableid, peerid, noop=False):
        self.ec2Client.create_route(
            DestinationCidrBlock=cidr,
            DryRun=noop,
            RouteTableId=routetableid,
            VpcPeeringConnectionId=peerid
        )

    def deleteRouteVPCPeer(self, cidr, routetableid, noop=False):
        self.ec2Client.create_route(
            DestinationCidrBlock=cidr,
            DryRun=noop,
            RouteTableId=routetableid
        )

    def get_instances_names_from_id(self, instance_ids):

        response = self.ec2Client.describe_instances(
            InstanceIds=instance_ids
        )

        instances = []
        instance_names = []
        for reservation in response["Reservations"]:
            instances.append(reservation["Instances"][0])
        for instance in instances:
            for tags in instance["Tags"]:
                if tags["Key"] == "Name":
                    instance_names.append(tags["Value"])
        return instance_names

    def create_customer_gateway(self, bgpasn, publicip, vpntype="ipsec.1", noop=False):
        response = self.ec2Client.create_customer_gateway(
            BgpAsn=bgpasn,
            PublicIp=publicip,
            Type=vpntype,
            DryRun=noop
        )

        return response["CustomerGateway"]

    def create_vpn_gateway(self, gatewayaz=None, vpntype="ipsec.1", noop=False):
        if gatewayaz:
            response = self.ec2Client.create_vpn_gateway(
                AvailabilityZone=gatewayaz,
                Type=vpntype,
                DryRun=noop
            )
        else:
            response = self.ec2Client.create_vpn_gateway(
                AvailabilityZone=gatewayaz,
                Type=vpntype,
                DryRun=noop
            )
        return response["VpnGateway"]

    def create_vpn_connection(self, cgwid, vpngwid, vpntype="ipsec.1", noop=False, options={'StaticRoutesOnly': False}):
        self.ec2Client.create_vpn_connection(
            CustomerGatewayId=cgwid,
            Type=vpntype,
            VpnGatewayId=vpngwid,
            DryRun=noop,
            Options=options
        )

    def create_vpn_connection_route(self, cidr, vpnid):
        self.ec2Client.create_vpn_connection_route(
            DestinationCidrBlock=cidr,
            VpnConnectionId=vpnid
        )

    def delete_vpn_connection(self, vpnid, noop=False):
        self.ec2Client.delete_vpn_connection(
            VpnConnectionId=vpnid,
            DryRun=noop
        )

    def delete_vpn_connection_route(self, cidr, vpnid):
        self.ec2Client.delete_vpn_connection_route(
            DestinationCidrBlock=cidr,
            VpnConnectionId=vpnid
        )

    def delete_vpn_gateway(self, vpngwid, noop=False):
        self.ec2Client.delete_vpn_gateway(
            VpnGatewayId=vpngwid,
            DryRun=noop
        )

    def create_tags(self, resources, tags, noop=False):
        self.ec2Client.create_tags(
            DryRun=noop,
            Resources=resources,
            Tags=tags
        )

    def delete_tags(self, resources, tags=None, noop=False):
        if tags is None:
            tags = []
        self.ec2Client.delete_tags(
            DryRun=noop,
            Resources=resources,
            Tags=tags
        )


class ec2vpcpeer:

    def __init__(self, session, identifier):
        self.vpcpeerResource = session.resource('ec2')
        self.vpcpeer = self.vpcpeerResource.VpcPeeringConnection(identifier)

    def accept(self, noop=False):
        self.vpcpeer.accept(
            DryRun=noop
        )

    def getAccepterInfo(self):
        return self.vpcpeer.accepter_vpc_info

    def getRequesterInfo(self):
        return self.vpcpeer.requester_vpc_info

    def getStatus(self):
        return self.vpcpeer.status
