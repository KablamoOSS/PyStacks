
class rekognitiontasks:

    def __init__(self):
        pass

    def buildImageObject(self, image, bucket, name, version=None):
        image_object = {}
        image_object["Bytes"] = image
        image_object["S3Object"] = self.builds3_object(bucket=bucket, name=name, version=version)

        return image_object

    def builds3_object(self, bucket, name, version=None):
        s3_object = {}
        s3_object["Bucket"] = bucket
        s3_object["Name"] = name
        if version:
            s3_object["Version"] = version

        return s3_object
