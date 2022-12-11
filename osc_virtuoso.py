#  converter from nxosc OSC message with Euler angle values 
#  to IEM SceneRotator or envelop for Live

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient

def print_handler(address, *args):
    print(f"{address}: {args}")

plu = 'none'
plugin = 0

ip_in = '127.0.0.1'
port_in = 8000
ip_out = input('Outgoing OSC IP (leave blank for is 127.0.0.1):')
if ip_out == "":
	ip_out = '127.0.0.1'
port_out = input('Outgoing OSC port: ')
if port_out:
	port_out = int(port_out)
else:
   port_out = 6500

plugin = int(input("Which plugin will receive OSC? \n 1) IEM SceneRotator \n 2) Envelop \n 3) DearVR Monitor \n 4) Virtuoso \nType number:"))

client = SimpleUDPClient(ip_out, port_out)  # Create client

if plugin == 1:
   plu = 'IEM SceneRotator'
   print(f"Sending to {ip_out}:{port_out} to {plu}, use CTRL+C to stop")
   def default_handler(address, *argv): 
      client.send_message("/SceneRotator/ypr", [-argv[1], -argv[0], argv[2]])
if plugin == 2:
   plu = 'Envelop'
   print(f"Sending to {ip_out}:{port_out} to {plu}, use CTRL+C to stop")
   def default_handler(address, *argv): 
      client.send_message("/E4 HOA Transform/yaw", (-((argv[1]+180)/360))+1)
      client.send_message("/E4 HOA Transform/pitch", (-((argv[0]+180)/360))+1)
      client.send_message("/E4 HOA Transform/roll", (argv[2]+180)/360)
if plugin == 3:
   plu = 'DearVR Monitor'
   print(f"Sending to {ip_out}:{port_out} to {plu}, use CTRL+C to stop")
   def default_handler(address, *argv): 
      client.send_message("/DearVR Monitor/yaw", (-((argv[1]+180)/360))+1)
elif plugin == 4:
	plu = 'Virtuoso'
	print(f"Sending to {ip_out}:{port_out} to {plu}, use CTRL+C to stop")
	def default_handler(address, *argv): 
		client.send_message("/Virtuoso/quat", [argv[3], argv[2], argv[0], argv[1]])

dispatcher = Dispatcher() 
if plugin <= 3:
	dispatcher.map("/nxosc/xyz", default_handler)
elif plugin == 4:
	dispatcher.map("/nxosc/quaternion", default_handler)

server = BlockingOSCUDPServer((ip_in, port_in), dispatcher)
server.serve_forever()  # Blocks forever