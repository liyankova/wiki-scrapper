# wikiscrapper/utils.py
import os
from urllib.parse import urlparse

def get_and_prepare_filepath(current_url, output_dir, file_format):
    """
    Creates a nested file path based on the URL structure,
    ensures directories exist, and applies the correct file extension.
    """
    parsed = urlparse(current_url)
    path = parsed.path.strip('/')
    
    if path.endswith(('.html', '.htm', '.aspx', '.php')):
        path = path.rsplit('.', 1)[0]
    
    extension = f".{file_format}"
    
    if not path:
        return os.path.join(output_dir, 'index' + extension)

    relative_filepath = os.path.join(*path.split('/')) + extension
    final_filepath = os.path.join(output_dir, relative_filepath)
    
    directory = os.path.dirname(final_filepath)
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
        
    return final_filepath

def is_valid_url(url, base_domain):
    """Checks if a URL belongs to the base domain."""
    parsed_url = urlparse(url)
    return parsed_url.netloc == base_domain
