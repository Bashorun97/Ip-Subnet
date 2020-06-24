#!/usr/bin/env python3
# Tue May 26 22:16:31 WAT 2020
# babaibeji

# Written with love using VIM

import sys
import parser
from octet_mapping import OCTET_MAPPING as octet_mapping


class Data:
  def __init__(self, ip, subnet_mask):
    self.ip = ip
    self.subnet_mask = subnet_mask

class Subnet:
  def get_network_id(self, ip, subnet_mask):
    ip_address = Data(ip, subnet_mask)
    ip = list(map(int, ip_address.ip.split('.')))
    subnet_mask = list(map(int, ip_address.subnet_mask.split('.')))
    network_id = '.'.join(list(map(str, [i&j for i,j in zip(ip, subnet_mask)])))
    metadata = {'network_id':network_id, 'subnet_mask':subnet_mask}
    return f"NetworkID =>  {metadata['network_id']}"

  def subnet_ip_addresses(self, decimal_subnet):
    subnet_mask = list(map(int, decimal_subnet.split('.')))
    cidr_list = [bin(octet).strip('0b') for octet in subnet_mask]
    cidr = sum(list(map(len, cidr_list)))
    range_of_addresses = 2**(32 - cidr) -2
    return f'Number of available IP Addresses => {range_of_addresses}'

  def ip_class(self, ip_address):
    ipp = ip_address.split('.')
    ip = int(ipp[0])
    if 1 <= ip <= 126:
      return f'A class A IP Address'
    elif 128 <= ip <=191:
      return f'A Class B IP Address'
    elif 192 <= ip <= 223:
      return f'A Class C IP Address'
    elif ip == 127:
      return f'A localhost'
    else:
      return f'Incorrect IP class'
      sys.exit()

def cidr_to_decimal_converter(ip_in_cidr_notation):
  ip_addr_list = ip_in_cidr_notation.split('/')
  network_prefix = ip_addr_list[0]
  cidr = ip_addr_list.pop()
  subnet_mask = '1'*int(cidr) + (32-int(cidr))*'0'
  first_octet = subnet_mask[:8]
  second_octet = subnet_mask[8:16]
  third_octet = subnet_mask[16:24]
  fourth_octet = subnet_mask[24:]
  subnet_list = [octet_mapping[int(first_octet)], octet_mapping[int(second_octet)],\
  octet_mapping[int(third_octet)], octet_mapping[int(fourth_octet)]]
  subnet = '.'.join(subnet_list)
  return network_prefix, subnet

def argparse_unpacker():
  parsed = parser.arg_parser()

  # Unpacks extended network prefix into network prefix and subnet mask
  extended_network_prefix = parsed.extended_network_prefix

 # Unpacks a list of network IP and subnetmask in decimal notation (e.g. 255.255.255.0)
  ip_and_subnetwork = parsed.ip_and_subnetmask

  if extended_network_prefix is not None:
    netwr_prefix_subnet = cidr_to_decimal_converter(extended_network_prefix)
    return netwr_prefix_subnet
  elif ip_and_subnetwork is not None:
    netwr_prefix_subnet = tuple(ip_and_subnetwork)
    return netwr_prefix_subnet

if __name__ == '__main__':
  argparse_unpacker()
  subnet_node = Subnet()
  ip, subnet = argparse_unpacker()
  network_id = subnet_node.get_network_id(ip, subnet)
  print(network_id)
  ip_address_class = subnet_node.ip_class(ip)
  print(ip_address_class)

  # Display number of ip addresses
  available_ip = subnet_node.subnet_ip_addresses(subnet)
  print(available_ip)
