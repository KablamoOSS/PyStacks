import os
import pprint
import re
import json
import sys

from botocore.exceptions import ClientError


def loadZoneFile(file_name, region):
    directory = os.path.dirname(__file__)

    path = '../configs/user/region/{region}/{file_name}.zone'.format(
        region=region, file_name=file_name)

    content = []
    try:
        with open(os.path.join(directory, path), 'r') as file_name:
            content = file_name.readlines()
    except IOError as err:
        print err
        sys.exit(1)

    content = [x for x in content if not x.startswith(';')]
    content = [x for x in content if not x.startswith('$')]
    content = [x for x in content if not x.strip() == '']
    content = [x.replace(' IN ', ' ') for x in content]
    content = [re.sub('\s+', ' ', x) for x in content]

    return content


def getZoneFilelist(region, stack=None):
    directory = os.path.dirname(__file__)

    if stack is None:
        path = '../configs/user/region/{region}/'.format(
            region=region)
        content = [file_name.replace('.zone', '') for file_name in os.listdir(os.path.join(directory, path)) if file_name.endswith('.zone')]
    else:
        content = [stack]
    return content


def getJSONZoneFilelist(stack=None):
    directory = os.path.dirname(__file__)

    if stack is None:
        path = '../configs/user/dns/'
        content = [file_name.replace('.zone', '') for file_name in os.listdir(os.path.join(directory, path)) if file_name.endswith('.zone')]
    else:
        content = stack
    return content


def getJSONSchema(file_name, folderpath):
    directory = os.path.dirname(__file__)

    path = '../configs/user/{folderpath}/{file_name}'.format(
        folderpath=folderpath, file_name=file_name)

    content = []
    with open(os.path.join(directory, path), 'r') as file_name:
        content = file_name.read()
    try:
        json.loads(content)
    except ClientError as err:
        print err
        sys.exit(1)

    return content


def loadJSONZoneFile(file_name):
    directory = os.path.dirname(__file__)

    path = '../configs/user/dns/{file_name}.zone'.format(
        file_name=file_name)

    content = []
    with open(os.path.join(directory, path), 'r') as file_name:
        content = file_name.read()
    try:
        json.loads(content)
    except ClientError as err:
        print err
        sys.exit(1)

    return content

# Requires the SOA to be on a single line with the TTL/Expiry et al delimited by space).
# This will pass a named-checkzone as well as comply with filtering out the SOA
# The parse also removes the NS records for the apex of the zone, as these
# will typically be the delegation set in Route53


def parseZone(zonedata, zonename, logoutput=None):
    zone = []
    fqdn = zonename + "."
    # print "#### Zone before filtering ####"
    # pprint.pprint(zonedata)
    # print "###############################"
    for x in zonedata:
        if "TXT" in x:
            txtrecord = x.split('"')
            record = txtrecord[0].split(' ')
            record[3] = "\"" + txtrecord[1] + "\""
        elif "SRV" in x:
            record = x.split(' ')
            record[3] = record[3] + " " + record[4] + " " + record[5] + " " + record[6]
        else:
            record = x.split(' ')
        if not record[2] == "SOA":  # I dont recognise your authority!
            # Removes the Apex NS records
            if not record[0] == fqdn and not record[0] == "@" or not record[2] == "NS":
                zone.append(record)
    if logoutput:
        print "Parsing Output"
        print zone
        print "--------------"
        sys.stdout.flush()
    return zone

# Take a list of records and combine them by type
# If you have 5 A records on seperate lines, this will merge them all onto one line


def dedup(seq, logoutput=None):
    seen = set()  # Sets be unquie yo
    deduped = []  # Returned list of discreet records
    points = {}  # Sets dont work well for index to pop the list
    for x in seq:
        setlen = len(seen)
        # So remember how records can have types, need to inspect for the type.
        record = '{ "' + x[0] + '", "' + x[2] + '" }'
        if record not in seen:
            seen.add(record)
            points[record] = setlen
            # So MX like to be difficult and make a record 5 fields rather than
            # 4. (God this looks ugly)
            if x[2] == "MX":
                x[3] = [x[3] + " " + x[4]]
            else:
                x[3] = [x[3]]
            # Inseting the whole object gets around length issues, I like
            # python.
            deduped.insert(setlen, x)
        else:
            update = deduped.pop(points[record])
            if x[2] == "MX":
                update[3].append(x[3] + " " + x[4])
            else:
                update[3].append(x[3])
            deduped.insert(points[record], update)
    record = []  # Reset button bro
    if logoutput:
        print "DEDUPED Output"
        pprint.pprint(deduped)
        print "--------------"
        sys.stdout.flush()
    return deduped


def buildfromzone(records):
    dictrecords = []

    for x in records:
        temprec = {}
        tempvalues = []
        temprec["Name"] = x[0]
        for value in x[3]:
            tempvalue = {}
            tempvalue["Value"] = value
            tempvalues.append(tempvalue)
        temprec["ResourceRecords"] = tempvalues
        temprec["TTL"] = int(x[1])
        temprec["Type"] = x[2]
        dictrecords.append(temprec)

    return dictrecords


def writezone(data, name, logging=None, directory=None):
    if logging:
        pprint.pprint(data)
    filedirectory = os.path.dirname(os.path.realpath(__file__))
    if directory:
        targetdirectory = os.path.join(
            filedirectory, directory)
    else:
        targetdirectory = os.path.join(
            filedirectory, '../configs/user/dns/')

    if not os.path.exists(targetdirectory):
        os.makedirs(targetdirectory)

    if directory:
        path = '{directory}/{file_name}zone'.format(file_name=name, directory=directory)
    else:
        path = '../configs/user/dns/{file_name}zone'.format(file_name=name)

    with open(os.path.join(filedirectory, path), "wb") as fh:
        fh.write(json.dumps(data))
