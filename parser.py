import argparse

def arg_parser():
  parser = argparse.ArgumentParser()

  group = parser.add_mutually_exclusive_group()
  group.add_argument('-i', nargs=2, action='store', dest='ip_and_subnetmask', 
      help='Accepts an ip adress with subnet mask in subnet notation. e.g. ip_subnet -i 192.168.0.22 255.255.255.0')
  group.add_argument('-c', action='store', dest='extended_network_prefix',
      help='Accepts subnet mask in extended prefix notation. e.g. ip_subnet -c 192.168.0.22/24')
  group.add_argument('--version', action='version', version='ip-subnet v1.0')
  command_list = parser.parse_args()
  return command_list
arg_parser()
