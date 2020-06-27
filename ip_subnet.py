#!/usr/bin/env python3
# Tue May 26 22:16:31 WAT 2020
# babaibeji

# Written with love using VIM

import sys
import parser_child
from octet_mapping import OCTET_MAPPING as octet_mapping


# =================
# Network Data Type
# =================
class Data:
  def __init__(self, ip, subnet_mask):
    self.ip = ip
    self.subnet_mask = subnet_mask


# =================
# Methods for oper-
# ating on a subnet
# are defined here
# =================
class Subnet:
  def get_network_id(self, ip, subnet_mask):
    ip_address = Data(ip, subnet_mask)
    # Ensure that both ip and subnet_mask are both in the legal nomenclature
    try:
      subnet_mask = list(map(int, ip_address.subnet_mask.split('.')))
      ip = list(map(int, ip_address.ip.split('.')))
    except ValueError:
      print(f'Value error. Ensure that you entered the flag\'s corresponding format')
      sys.exit()

    network_id = '.'.join(list(map(str, [i&j for i,j in zip(ip, subnet_mask)])))
    metadata = {'network_id':network_id, 'subnet_mask':subnet_mask}
    return f"Base Network ID =>  {metadata['network_id']}"

  def subnet_ip_addresses(self, decimal_subnet):
    subnet_mask = list(map(int, decimal_subnet.split('.')))
    cidr_list = [bin(octet).strip('0b') for octet in subnet_mask]
    cidr = sum(list(map(len, cidr_list)))
    range_of_addresses = 2**(32 - cidr) -2
    return f'Number of available hosts and IP Addresses => {range_of_addresses}'

  def ip_class(self, ip_address):
    ipp = ip_address.split('.')
    ip = int(ipp[0])
    
    try:
      assert ip <= 223 and ip >= 1
    except AssertionError:
      print(f'Wrong IP class. The first octet of the Network ID should be between 0 - 223')
      
      sys.exit()

    if 1 <= ip <= 126:
      return f'A class A IP Address'
    elif 128 <= ip <=191:
      return f'A Class B IP Address'
    elif 192 <= ip <= 223:
      return f'A Class C IP Address'
    elif ip == 127:
      return f'A localhost'

# NB: Network prefix is the same as CIDR (Classless Inter-Domain Range)
# Converts to decimal notation from network prefix notation or CIDR
def prefix_to_decimal_converter(ip_in_prefix_notation):
  ip_addr_list = ip_in_prefix_notation.split('/')
  network_id = ip_addr_list[0]
  network_prefix = int(ip_addr_list.pop())

  try:
    assert network_prefix <= 32 and network_prefix >= 0
  except AssertionError:
    print(f'CIDR value can only be between 0 - 32')
    sys.exit()

  subnet_mask = '1'*network_prefix + (32-network_prefix)*'0'
  first_octet = subnet_mask[:8]
  second_octet = subnet_mask[8:16]
  third_octet = subnet_mask[16:24]
  fourth_octet = subnet_mask[24:]
  subnet_list = [octet_mapping[int(first_octet)], octet_mapping[int(second_octet)],\
  octet_mapping[int(third_octet)], octet_mapping[int(fourth_octet)]]
  subnet = '.'.join(subnet_list)
  return network_id, subnet


class EdgeCaseError(Exception):
  pass


def argparse_unpacker():
  keyword_map = {}
  parse = parser_child.parser
  parsed = parse.parse_args()

  network_prefix = parsed.network_prefix
  ip_and_subnetmask = parsed.ip_and_subnetmask
  subnetworks_info = parsed.subnetworks_info
  
  if network_prefix is not None:
    network_id_and_subnet = network_prefix
    keyword_map['network_prefix'] = network_id_and_subnet

  if ip_and_subnetmask is not None:
    network_id_and_subnet = tuple(ip_and_subnetmask)
    keyword_map['ip_and_subnetmask'] = network_id_and_subnet

  if subnetworks_info is not None:
    subnet_info = tuple(subnetworks_info)
    keyword_map['subnetworks_info'] = subnet_info

  return keyword_map


if __name__ == '__main__':

  subnet_node = Subnet()
  
  # Unpacks keyword_map into args_map
  args_map = argparse_unpacker()

  # Gracefully handles the exception of passing one flag
  try:
    net, submask = prefix_to_decimal_converter(args_map['network_prefix'])
  except KeyError:
    net, submask = args_map['ip_and_subnetmask']

  ip_address_class = subnet_node.ip_class(net)
  print(ip_address_class)

  network_id = subnet_node.get_network_id(net, submask)
  print(network_id)

  available_ip = subnet_node.subnet_ip_addresses(submask)
  print(available_ip)

