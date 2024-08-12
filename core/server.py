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

CONFIG = None

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



def start_server(config: Config):
    print("2")
    global server
    ContextManager.set_config(config)
    app_conf = ContextManager.get_config()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    server = loop.run_until_complete(asyncio.start_server(client_handler, app_conf.host, app_conf.port))
    try:
        loop.run_forever()
    except asyncio.CancelledError:
        pass
    finally:
        loop.run_until_complete(server.wait_closed())
        loop.close()
        print("Server stopped")
    
def stop_server():
    global server
    if server:
        server.close()
        # server should be restarted now


def restart_server():
    print("Restarting server...")
    stop_server()
    print("Server stopped from restart server()")
    start_server(CONFIG)
    print("Server started from restart_server()")

def restart_server_sync(loop):
    # loop = asyncio.get_event_loop()
    asyncio.run_coroutine_threadsafe(stop_server(), loop).result()
    print("Server stopped from restart server()")
    asyncio.run_coroutine_threadsafe(start_server(), loop).result()
    print("Server started from restart_server()")

class RestartHandler(FileSystemEventHandler):
    def __init__(self, restart_callback):
        super().__init__()
        # self.loop = loop
        self.restart_callback = restart_callback
#
    def on_modified(self, event):
        if event.src_path.endswith(".py"):#
            # print(f"Detected changes in {event.src_path}")
            # asyncio.run_coroutine_threadsafe(self.restart_callback(self.loop), self.loop)#
            self.restart_callback()
    
def watch():
    event_handler = RestartHandler(restart_callback=restart_server)
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=True)
    observer.start()#
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    
def run_parallel(config):
    ContextManager.set_config(config)
    app_conf = ContextManager.get_config()

    server_thread = threading.Thread(target=start_server, args=(config,))
    watch_thread = threading.Thread(target=watch)
#
    server_thread.start()
    watch_thread.start()

    server_thread.join()
    watch_thread.join()

def server(port=6942, config: Config = None)-> None:
    global CONFIG
    CONFIG = config
    ipv4_addr = socket.gethostbyname(socket.gethostname())
    host: str = "0.0.0.0"
    # display the debug logs
    print("Development server started")
    print(f"Listening to port {port}")
    print(get_green_str(f"Running on http://{ipv4_addr}:{port}/ "))
    log_warning("Warning: this is not a deployment server. This is for debugging purpose only", showIcon=True)

    run_parallel(CONFIG)
    
    
