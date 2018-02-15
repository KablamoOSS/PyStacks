import base64


class kms:
    def __init__(self, session):
        self.kmsClient = session.client('kms')

    def encrypt(self, secret, alias):
        ciphertext = self.kmsClient.encrypt(
            KeyId=alias,
            Plaintext=bytes(secret),
        )
        return base64.b64encode(ciphertext["CiphertextBlob"])

    def decrypt(self, secret):
        plaintext = self.kmsClient.decrypt(
            CiphertextBlob=bytes(base64.b64decode(secret))
        )
        return plaintext["Plaintext"]
