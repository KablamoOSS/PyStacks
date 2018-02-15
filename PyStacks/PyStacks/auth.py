import os
import boto3


class authenticate:

    def __init__(self, region):
        self.stsClient = boto3.client('sts')
        self.assumedRole = os.environ.get('ASSUMED_ROLE')
        self.mfaSerial = os.environ.get('MFA_SERIAL')
        self.awsMfaToken = os.environ.get('TOKEN')
        self.awsRegion = region
        self.sess = None

    def getSession(self):
        if self.sess is None:
            self.sess = self.newSession()
        return self.sess

    def newSession(self):

        if self.assumedRole is not None:
            if self.mfaSerial is None:
                creds = self.stsClient.assume_role(
                    RoleArn=self.assumedRole,
                    RoleSessionName='ecs-deploy-session',
                    DurationSeconds=3600
                )
            else:
                creds = self.stsClient.assume_role(
                    RoleArn=self.assumedRole,
                    RoleSessionName='ecs-deploy-session',
                    DurationSeconds=3600,
                    SerialNumber=self.mfaSerial,
                    TokenCode=self.awsMfaToken
                )

            session = boto3.session.Session(
                aws_access_key_id=creds['Credentials']['AccessKeyId'],
                aws_secret_access_key=creds['Credentials']['SecretAccessKey'],
                aws_session_token=creds['Credentials']['SessionToken'],
                region_name=self.awsRegion
            )
        else:
            session = boto3.session.Session(
                region_name=self.awsRegion
            )
        return session
