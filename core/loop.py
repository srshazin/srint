# from srint.utils.parser import parse_http_response
# from typing import Dict, Any, Union, List
# from srint.utils.helpers import print_headers
# from srint.core.helpers import map_routes
# from srint.core.response import make_response
# from srint.core.models import Config

# def loop(sock, config: Config ):
#     try:
#         client, client_addr = sock.accept()
#         print(f"Connection from {client_addr[0]}:{client_addr[1]}")
#         response_ = client.recv(1024)
#         headers: Dict[str, Union[str, Dict[str, str]] ] = parse_http_response(response_.decode())
#         print("--------------------------------------------")
#         print_headers(headers)
#         print("--------------------------------------------")
#         resp = map_routes(request_path=headers.get("path"), routes=config.routes)
#         client.send(make_response(resp()).encode())
#     except KeyboardInterrupt:
#         global run_server
#         run_server = False
