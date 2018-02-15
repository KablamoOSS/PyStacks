from verification import ensure_http_success


class LambdaAPI(object):

    def __init__(self, session):
        self.client = session.client('lambda')

    @ensure_http_success
    def list_versions_by_function(self, function_name, **_):
        return self.client.list_versions_by_function(
            FunctionName=function_name,
        )

    @ensure_http_success
    def list_aliases(self, function_name, **_):
        return self.client.list_aliases(FunctionName=function_name)

    @ensure_http_success
    def update_alias(self, function_name, alias_name, function_version, alias_desc=None, **_):
        params = {
            "FunctionName": function_name,
            "Name": alias_name,
            "FunctionVersion": function_version,
            "Description": alias_desc,
        }
        return self.client.update_alias(**{k: v for k, v in params.items() if v})

    @ensure_http_success
    def create_alias(self, function_name, alias_name, function_version, alias_desc=None, **_):
        params = {
            "FunctionName": function_name,
            "Name": alias_name,
            "FunctionVersion": function_version,
            "Description": alias_desc,
        }
        return self.client.create_alias(**{k: v for k, v in params.items() if v})

    @ensure_http_success
    def publish_version(self, function_name, latest_hash=None, version_desc=None, **_):
        params = {
            "FunctionName": function_name,
            "CodeSha256": latest_hash,  # update_function_code_response['CodeSha256'],  # Use to ensure matches $LATEST
            "Description": version_desc,
        }
        return self.client.publish_version(**{k: v for k, v in params.items() if v})
