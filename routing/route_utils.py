from typing import Callable, Any, List, Dict, Union
import os
from mimetypes import guess_type
from srint.core.response import Response
from srint.core.context import ContextManager

def no_route_found():
    return "Nothing found sorry"

def calculate_content_length(body):
    """
    Calculate the content length based on the body.
    """
    if isinstance(body, str):
        body_bytes = body.encode('utf-8')  # Encode string to bytes for length calculation
    elif isinstance(body, bytes):
        body_bytes = body  # Already in bytes
    else:
        raise TypeError("Body must be either a string or bytes.")
    
    return len(body_bytes)  # Length in bytes


def map_routes(request_path: str)-> Callable[[Any], Any]:
    routes = ContextManager.get_config().routes
    for route in routes:
        if route["path"] == request_path:
            return route["handler"]
    
    # removing the preceding "/" from the path string
    static_path = request_path[1:] if request_path.startswith("/") else request_path
    
    def static_handler():
        """
        Handle a request for a static file and return an appropriate HTTP response as a string.
        """
        content_type, _ = guess_type(static_path)
        if content_type is None:
            content_type = "application/octet-stream"

        with open(static_path, 'rb') as file:
            body = file.read()
        
        content_length = len(body)
        response = Response()
        response.status_code = 200
        response.body = body
        response.contentType = content_type
        return response

    # check if the requested path is a static file
    if os.path.exists(static_path) and os.path.isfile(static_path):
        print("path found")
        # return static content
        return static_handler
    
    # finally return 404 response
    return no_route_found


