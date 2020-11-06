# converter for nxosc to IEM SceneRotator Euler values

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient

def print_handler(address, *args):
    print(f"{address}: {args}")

ip_out = "127.0.0.1"
port_out = 6500

client = SimpleUDPClient(ip_out, port_out)  # Create client

def default_handler(address, *argv): 
    client.send_message("/SceneRotator/ypr", [-argv[1], -argv[0], argv[2]])  

dispatcher = Dispatcher() 
dispatcher.map("/nxosc/xyz", default_handler)

ip_in = "127.0.0.1"
port_in = 8000

server = BlockingOSCUDPServer((ip_in, port_in), dispatcher)
server.serve_forever()  # Blocks forever
