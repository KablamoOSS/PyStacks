import kms


class kmstasks:

    def __init__(self):
        pass

    def decrypt_secrets(self, session, **secrets):
        config = {}
        for k, v in secrets.iteritems():
            vde = self.decrypt(session, v)
            config[k] = vde
        return config

    def decrypt(self, session, string):
        crypto = kms.kms(session)
        decrypted = crypto.decrypt(string)
        return decrypted

    def encrypt(self, string, session, key_alias):
        crypto = kms.kms(session)
        encrypted = crypto.encrypt(string, key_alias)
        print encrypted
        return encrypted
