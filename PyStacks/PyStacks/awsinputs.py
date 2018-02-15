import re


def IsSubnet(var):
    if re.search("^subnet-[\w]{8}\Z", var):
        return True
    return False


def IsVPC(var):
    if re.search("^vpc-[\w]{8}\Z", var):
        return True
    return False


def IsVPCPeer(var):
    if re.search("^pcx-[\w]{8}\Z", var):
        return True
    return False


def IsRouteTable(var):
    if re.search("^rtb-[\w]{8}\Z", var):
        return True
    return False


def IsInternetGateway(var):
    if re.search("^igw-[\w]{8}\Z", var):
        return True
    return False


def IsDHCPSet(var):
    if re.search("^dopt-[\w]{8}\Z", var):
        return True
    return False


def IsNetworkACL(var):
    if re.search("^acl-[\w]{8}\Z", var):
        return True
    return False


def IsSecurityGroup(var):
    if re.search("^sg-[\w]{8}\Z", var):
        return True
    return False


def IsVirtualPrivateGateway(var):
    if re.search("^vgw-[\w]{8}\Z", var):
        return True
    return False


def IsEC2(var):
    if re.search("^i-[\w]{17}\Z", var):
        return True
    return False


def IsVol(var):
    if re.search("^vol-[\w]{17}\Z", var):
        return True
    return False


def IsSnapshot(var):
    if re.search("^snap-[\w]{17}\Z", var):
        return True
    return False


def IsENI(var):
    if re.search("^eni-[\w]{8}\Z", var):
        return True
    return False


def IsEIP(var):
    if re.search("^eipalloc-[\w]{8}\Z", var):
        return True
    return False


def IsEFS(var):
    if re.search("^fs-[\w]{8}\Z", var):
        return True
    return False


def IsRootOrg(var):
    if re.search("^r-[\w]{4,32}\Z", var):
        return True
    return False


def IsSCP(var):
    if re.search("^p-[\w]{4,32}\Z", var):
        return True
    return False


def IsOU(var):
    if re.search("^ou-[\w]{4,32}-[\w]{8,32}\Z", var):
        return True
    return False


def IsAccount(var):
    if re.search("^ou-[0-9]{12}\Z", var):
        return True
    return False


def IsIPAddress(var):
    if re.search("^[0-9]{1,3}?\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\Z", var) and validIP(var):
        return True
    return False


def IsCIDR(var):
    if re.search("^[0-9]{1,3}?\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/[0-9]{1,2}?\Z", var) and validCIDR(var):
        return True
    return False


def validIP(var):
    status = validOctetsRange(var.split("."))
    return status


def validCIDR(var):
    ip, cidr = var.split("/")
    cidrstatus = validCIDRRange(cidr)
    ipstatus = validOctetsRange(ip.split("."))
    if cidrstatus and ipstatus:
        return True
    return False


def validOctetsRange(octets):
    status = True
    for octet in octets:
        if int(octet) not in range(0, 256):
            status = False
    return status


def validCIDRRange(cidr):
    status = True
    if int(cidr) not in range(0, 33):
        status = False
    return status
