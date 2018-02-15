def ensure_http_success(func):
    """May be used as a method decorator. Raises a RuntimeError if the input function does not return a
    successful HTTPStatusCode.  KeyError input function is not a Boto3 API call.

    Args:
        func (func):  This should be a boto3 API call.

    Returns:
        func
    """
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        if not 200 <= response['ResponseMetadata']['HTTPStatusCode'] < 300:
            raise RuntimeError("API call failed! :", response['ResponseMetadata'])
        return response
    return wrapper
