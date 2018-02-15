import sys
import logging
from lambdaapi import LambdaAPI
from botocore.exceptions import ClientError

from logger import get_pystacks_log
log = get_pystacks_log()


class lambdatasks:

    def __init__(self):
        pass

    def invokeLambda(self, function, payload, session):
        client = session.client('lambda')
        b = bytearray()
        b.extend(payload)
        try:
            client.invoke(
                FunctionName=function,
                Payload=b
            )
        except ClientError as err:
            logging.warn(err)
            sys.exit(1)


def upsert_alias(session, function_name, alias_name, alias_desc, function_version=None):
    lapi = LambdaAPI(session)

    # Publish a version from $LATEST. Assumes deployment made to lambda without version
    if not function_version:
        function_version = lapi.publish_version(function_name)['Version']

    alias_exists = False
    for a in lapi.list_aliases(function_name)['Aliases']:
        if a['Name'] == alias_name:
            alias_exists = True
            break

    if alias_exists:
        log.info("alias exists. Updating ...")
        response = lapi.update_alias(**locals())
    else:
        log.info("alias does not exist. Creating ...")
        response = lapi.create_alias(**locals())

    log.info("Alias '{Name}' for: '{Description}' is setup: Function version {FunctionVersion} used for Alias ARN: {AliasArn}".format(**response))
    return response
