from typing import Dict, Union
import traceback
def parse_http_response(http_request: str)-> Dict[str, Union[str, Dict[str, str]]]:
    try:
        # Split the request into lines
        lines = http_request.split("\r\n")

        # Extract the request line
        request_line = lines[0]
        method, path, version = request_line.split(" ")

        # Extract headers
        headers = {}
        for line in lines[1:]:
            if line == "":  # End of headers
                break
            key, value = line.split(":", 1)
            headers[key.strip()] = value.strip()

        return {
            "method": method,
            "path": path,
            "version": version,
            "headers": headers
        }
    except:
        traceback.print_exc()