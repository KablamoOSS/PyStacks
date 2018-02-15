import sys
import logging
import acm
from botocore.exceptions import ClientError


class acmtasks:

    def __init__(self):
        pass

    def requestCert(self, domain, altnames, githash, certarn, domainoptions, session):
        api = acm.acm(session)
        try:
            api.request_certificate(domain=domain, atlnames=altnames, token=githash, domainoptions=domainoptions)
        except ClientError as err:
            logging.warn(err)
            sys.exit(1)
