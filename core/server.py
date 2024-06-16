from typing import Dict, Any, Union, List, Tuple
import socket
from srint.utils.logging import perror, log_success, log_warning, get_green_str
import traceback
from srint.utils.parser import parse_http_response

from srint.utils.helpers import print_headers
from srint.routing.route_utils import map_routes
from srint.core.response import make_response
from srint.core.models import Config

def server(port=6942, config: Config = None)-> None:
    run_server = True
    ipv4_addr = socket.gethostbyname(socket.gethostname())
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr: Tuple[str, int] = (("0.0.0.0", port))
    sock.bind(addr)
    sock.listen()
    
    print("Development server started")
    print(f"Listening to port {port}")
    print(get_green_str(f"Running on http://{ipv4_addr}:{port}/ "))
    log_warning("Warning: this is not a deployment server. This is for debugging purpose only")
    try:
        while run_server:
            try:
                client, client_addr = sock.accept()
                print(f"Connection from {client_addr[0]}:{client_addr[1]}")
                response_ = client.recv(1024)
                headers: Dict[str, Union[str, Dict[str, str]] ] = parse_http_response(response_.decode())
                # print("--------------------------------------------")
                # print_headers(headers)
                # print("--------------------------------------------")
                print("Accessed path: " + headers["path"] )
                resp = map_routes(request_path=headers.get("path"), routes=config.routes)
                client.send(make_response(resp()))
            except KeyboardInterrupt:
                run_server = False
                break

        run_server = False
        sock.close()
        print("Keyboard interrupt. CLosing server")
    except:
        traceback.print_exc()
        run_server = False
        sock.close()
    finally:
        sock.close()