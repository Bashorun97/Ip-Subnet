import argparse

def arg_parser():
  parser = argparse.ArgumentParser()

  address_group = parser.add_mutually_exclusive_group()

  address_group.add_argument('-i', nargs=2, action='store', dest='ip_and_subnetmask', 
      help='Accepts an ip address with subnet mask in subnet notation. e.g. ip_subnet -i 192.168.0.22 255.255.255.0')
  address_group.add_argument('-c', action='store', dest='network_prefix',
      help='Accepts an ip address with subnet mask in network prefix notation. e.g. ip_subnet -c 192.168.0.22/24')
  address_group.add_argument('--version', action='version', version='ip-subnet v1.0')


  parser.add_argument('--create-subnets', action='store', type=int, dest='subnet_num',
      help='Creates subnet hosts based on the flag\'s argument')
  command_list = parser.parse_args()
  return command_list

arg_parser()
