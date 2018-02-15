from verification import ensure_http_success


class IoTAPI:
    def __init__(self, session):
        self.client = session.client('iot')

    @ensure_http_success
    def create_thing(self, name, thing_type=None, attributes={}):
        """This creates a thing only using an existing session.  None of the other API setting are supported at this
        time """

        params = {
            "thingName": name,
            "thingTypeName": thing_type,
            "attributePayload": {
                "attributes": attributes,
                "merge": False,
            },
        }

        return self.client.create_thing(**{k: v for k, v in params.items() if v})

    @ensure_http_success
    def create_keys_and_certificate(self, active=True):
        """Creates a certificate to authenticate a 'thing' to the IoT cloud.  This will be the last time the private keys returned in the
        response will be accessible

        Returns
            (cloud.pem.crt, cloud.pem.key)
        """

        return self.client.create_keys_and_certificate(setAsActive=active)

    @ensure_http_success
    def attach_thing_principal(self, thingName, certArn):
        """Takes an IoT 'Thing' ... yes thats that they call it ... and attaches a certificate to it. Use
        'create_keys_and_certificate' to produce the cert
        """

        return self.client.attach_thing_principal(
            thingName=thingName,
            principal=certArn,
        )

    @ensure_http_success
    def attach_policy(self, policyName, certArn):
        return self.client.attach_policy(
            policyName=policyName,
            target=certArn,
        )

    @ensure_http_success
    def describe_endpoint(self):
        return self.client.describe_endpoint()

    @ensure_http_success
    def list_things(self):
        return self.client.list_things()

    @ensure_http_success
    def list_thing_principals(self, thing_name):
        return self.client.list_thing_principals(thingName=thing_name)

    @ensure_http_success
    def delete_thing(self, thing_name):
        return self.client.delete_thing(thingName=thing_name)

    def delete_certificate(self, cert_id):
        return self.client.delete_certificate(certificateId=cert_id)

    @ensure_http_success
    def detach_thing_principal(self, thing_name, principal):
        return self.client.detach_thing_principal(
            thingName=thing_name,
            principal=principal,
        )

    @ensure_http_success
    def detach_policy(self, policy_name, principal):
        return self.client.detach_policy(
            policyName=policy_name,
            target=principal,
        )

    @ensure_http_success
    def update_certificate(self, cert_id, new_status):
        return self.client.update_certificate(
            certificateId=cert_id,
            newStatus=new_status,
        )

    @ensure_http_success
    def list_attached_policies(self, principal):
        return self.client.list_attached_policies(target=principal)

    @ensure_http_success
    def list_certificates(self):
        return self.client.list_certificates()
