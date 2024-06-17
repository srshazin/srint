from typing import Dict, Any, Union, List, Tuple
import socket
from srint.utils.logging import perror, log_success, log_warning, get_green_str
import traceback
from srint.utils.parser import parse_http_response
import asyncio, time, threading
from asyncio import StreamReader, StreamWriter
from srint.utils.helpers import print_headers
from srint.routing.route_utils import map_routes
from srint.core.response import make_response
from srint.core.models import Config
from srint.core.context import ContextManager
from  srint.core.states import *
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

async def client_handler(reader: StreamReader, writer: StreamWriter):
    try:
        payload = await reader.read(4096)
        client_host, client_port =  writer.get_extra_info("peername")
        print(f"Connection received from {client_host}:{client_port}")
        headers: Dict[str, Union[str, Dict[str, str]] ] = parse_http_response(payload.decode())
        print("Accessed path: " + headers["path"] )
        resp_callback = map_routes(request_path=headers.get("path"))
        response = make_response(resp_callback())
        writer.write(response)
    except KeyboardInterrupt:
        # close the connecting on keyboard interrupt
        print("Keyboard interrupt received. Closing connection...")
        writer.close()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        writer.close()


# create a async socket server
async def create_server(host: str, port: int):
    server = await asyncio.start_server(client_handler, host, port)
    async with server:
        print("Asynchronous server started...")
        await server.serve_forever() 



async def start_server():
    global loop, server
    app_conf = ContextManager.get_config()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    server = loop.run_until_complete(await create_server(app_conf.host, app_conf.port))
    print("Server started")
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        traceback.print_exc()
        exit(1)
    
def stop_server():
    global loop, server
    if server:
        server.close()
        loop.run_until_complete(server.wait_closed())
        print("Server stopped")
    if loop:
        loop.stop()
        loop.close()
        print("Event loop closed")


class RestartHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"Detected changes in {event.src_path}")
    
async def watch():
    print("WATCHING")
    event_handler = RestartHandler()
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=True)
    observer.start()

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    
async def run_parallel():
    await asyncio.gather(start_server(), watch())

def server(port=6942, config: Config = None)-> None:
    ipv4_addr = socket.gethostbyname(socket.gethostname())
    host: str = "0.0.0.0"
    # display the debug logs
    print("Development server started")
    print(f"Listening to port {port}")
    print(get_green_str(f"Running on http://{ipv4_addr}:{port}/ "))
    log_warning("Warning: this is not a deployment server. This is for debugging purpose only", showIcon=True)

    asyncio.run(run_parallel())
    # test
    
    
