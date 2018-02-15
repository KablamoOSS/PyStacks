import unittest

from mock import MagicMock

from PyStacks.PyStacks.ec2tasks import ec2tasks


class TestEC2TasksSetup(unittest.TestCase):
    def setUp(self):
        self.mocksession = MagicMock()
        self.mockec2Client = MagicMock()

        self.mocksession.client.return_value = self.mockec2Client

        self.ec2tasks = ec2tasks()


class TestEC2Tasks(TestEC2TasksSetup):
    def test_filter(self):
        assertfilters = [{"Name": "vpc-id", "Values": ["vpc-73de4917"]}]
        testfilter = self.ec2tasks.buildFilters("vpc-id", ["vpc-73de4917"])
        self.assertEquals(testfilter, assertfilters)

    def test_filters(self):
        assertfilters = [{"Name": "vpc-id", "Values": ["vpc-73de4917", "vpc-73de4918"]}]
        testfilter = self.ec2tasks.buildFilters("vpc-id", ["vpc-73de4917", "vpc-73de4918"])
        self.assertEquals(testfilter, assertfilters)

    def test_routelist(self):
        routelist = {
            "Routes": [
                {
                    "DestinationCidrBlock": "172.31.0.0/16",
                    "GatewayId": "local",
                    "Origin": "CreateRouteTable",
                    "State": "active"
                },
                {
                    "DestinationCidrBlock": "0.0.0.0/0",
                    "GatewayId": "igw-6d253308",
                    "Origin": "CreateRoute",
                    "State": "active"
                }
            ]
        }
        assertroutelist = ["172.31.0.0/16", "0.0.0.0/0"]
        testroutelist = self.ec2tasks.buildRoutelist(routelist)
        self.assertEquals(testroutelist, assertroutelist)

    def test_routelist_empty(self):
        routelist = {
            "Routes": [
            ]
        }
        assertroutelist = []
        testroutelist = self.ec2tasks.buildRoutelist(routelist)
        self.assertEquals(testroutelist, assertroutelist)

    def test_vpcpeeroptions_true(self):
        noop = True
        assertoptions = {'AllowDnsResolutionFromRemoteVpc': True}
        testoptions = self.ec2tasks.buildVPCPeerOptions(noop)
        self.assertEquals(testoptions, assertoptions)

    def test_vpcpeeroptions_false(self):
        noop = False
        assertoptions = {'AllowDnsResolutionFromRemoteVpc': False}
        testoptions = self.ec2tasks.buildVPCPeerOptions(noop)
        self.assertEquals(testoptions, assertoptions)

    def test_vpcpeeroptions_default(self):
        assertoptions = {'AllowDnsResolutionFromRemoteVpc': True}
        testoptions = self.ec2tasks.buildVPCPeerOptions()
        self.assertEquals(testoptions, assertoptions)
