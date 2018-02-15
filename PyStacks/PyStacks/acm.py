class acm:

    def __init__(self, session):
            self.acmClient = session.client('acm')

    def requestCertificate(self, domain, atlnames, token, domainoptions):
            self.acmClient.request_certificate(
                DomainName=domain,
                SubjectAlternativeNames=atlnames,
                IdempotencyToken=token,
                DomainValidationOptions=domainoptions
            )
