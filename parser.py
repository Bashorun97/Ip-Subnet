import argparse

def arg_parser():
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', action='store', dest='ip_address', 
    help='Use the -i flag together with the -s flag i.e -i 192.168.0.22 -s 255.255.255.0')
  parser.add_argument('-s', action='store', dest='decimal_notation',
    help='Accepts subnet mask in decimal notation. i.e 255.255.255.0')
  parser.add_argument('-c', action='store', type=int, dest='extended_network_prefix',
    help='Accepts subnet mask in extended prefix notation. i.e 24, 25, 22')
  parser.add_argument('--version', action='version', version='ip-subnet v1.0')
  command_list = parser.parse_args()
  return command_list
#print(command_list.decimal_notation)
#print(command_list.extended_network_prefix)
#print(command_list)
