class S3:

    def __init__(self, session):
        self.client = session.client('s3')
        self.resource = session.resource('s3')

    def list_buckets(self):
        return self.client.list_buckets()

    def checkForFile(self, bucket, key):
        response = self.client.list_objects(
            Bucket=bucket,
            Delimiter=key,
        )
        return response

    def uploadFile(self, filename, bucket, key):
        self.client.upload_file(
            Filename=filename,
            Bucket=bucket,
            Key=key
        )

    def create_bucket(self, bucket, region):
        ret = self.client.create_bucket(
            ACL='private',
            Bucket=bucket,
            CreateBucketConfiguration={
                'LocationConstraint': region
            }
        )
