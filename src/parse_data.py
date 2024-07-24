import os
from urllib.parse import urlparse, unquote

def parse_api_data(data):
    result_dict = {}
    for item in data.get('data', {}).get('list', []):
        path = item.get('path', '')
        parsed_path = urlparse(path)
        filename = unquote(os.path.basename(parsed_path.path))
        name = os.path.splitext(filename)[0]
        result_dict[name] = path
    return result_dict
