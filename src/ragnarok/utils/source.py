import os
import re

class UnknownSourceTypeError(Exception):
    pass

def get_source_type(source):
    # Simple URL regex pattern
    url_pattern = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if re.match(url_pattern, source):
        return "URL"
    elif os.path.exists(source):
        return os.path.splitext(source)[1]
    else:
        raise UnknownSourceTypeError(f"The source '{source}' is neither a valid URL nor an existing file path.")