#!/usr/bin/env python3
# Tue May 26 22:16:31 WAT 2020
# babaibeji

# Written with love using VIM

import sys
import math
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
    return metadata 

  def subnet_ip_addresses(self, decimal_subnet):
    subnet_mask = list(map(int, decimal_subnet.split('.')))
    cidr_list = [bin(octet).strip('0b') for octet in subnet_mask]
    cidr = sum(list(map(len, cidr_list)))
    range_of_addresses = 2**(32 - cidr) -2
    return range_of_addresses

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


def cidr_spliter(ip_in_prefix_notation):
  ip_addr_list = ip_in_prefix_notation.split('/')
  # Packs network ID and cidr into a tuple
  splited_data = ip_addr_list[0], int(ip_addr_list.pop())
  return splited_data


# NB: Network prefix is the same as CIDR (Classless Inter-Domain Range)
# Converts to decimal notation from network prefix notation or CIDR
def prefix_to_decimal_converter(ip_in_prefix_notation):
  network_id, cidr = cidr_spliter(ip_in_prefix_notation)
  
  try:
    assert cidr <= 32 and cidr >= 0
  except AssertionError:
    print(f'CIDR value can only be between 0 - 32')
    sys.exit()

  subnet_mask = '1'*cidr+ (32-cidr)*'0'
  first_octet = subnet_mask[:8]
  second_octet = subnet_mask[8:16]
  third_octet = subnet_mask[16:24]
  fourth_octet = subnet_mask[24:]
  subnet_list = [octet_mapping[int(first_octet)], octet_mapping[int(second_octet)],\
  octet_mapping[int(third_octet)], octet_mapping[int(fourth_octet)]]
  subnet = '.'.join(subnet_list)
  return network_id, subnet


class CreateSubnetwork(Subnet):
  def __init__(self):
    #sub_quantity = args_map['subnetworks_info']
    pass

  def generate_metadata(self, **kwargs):
    network_id, cidr = cidr_spliter(kwargs['parent_addr'])
    
    if kwargs.__contains__('sub_quantity'):
      added_bits = math.log2(kwargs['sub_quantity'])
      sub = str(math.floor(sum([cidr, added_bits])))
      extended_network_address = [network_id, sub]

    else:
      # Host quantity
      quantity = 32 - math.log2(kwargs['host_quantity'])
      extended_network_address = [network_id, str(math.floor(quantity))]

    # new_cidr depending on the outcome of preceding control structure
    new_cidr = '/'.join(extended_network_address)
    child_addr, parent_addr = map(prefix_to_decimal_converter, (new_cidr, kwargs['parent_addr']))
    parent_net = self.get_network_id(parent_addr[0], parent_addr[1])
    child_net = self.get_network_id(child_addr[0], child_addr[1])
    
    # extended_subnet_bits = [bin(octet).strip('0b') for octet in extended_network_address]

    network_metadata = {'parent_addr':parent_net, 'child_addr':child_net}
    return network_metadata

  def generate_addresses(self, args):
    addresses = self.subnet_ip_addresses(args)
    return addresses


def argparse_unpacker(parse_object=None):
  keyword_map = {}
  parse = parse_object
  parsed = parse.parse_args()

  network_prefix = parsed.network_prefix
  ip_and_subnetmask = parsed.ip_and_subnetmask
  create_subnets = parsed.create_subnets
  create_hosts = parsed.create_hosts
  
  if network_prefix is not None:
    network_id_and_subnet = network_prefix
    keyword_map['network_prefix'] = network_id_and_subnet

  if ip_and_subnetmask is not None:
    network_id_and_subnet = tuple(ip_and_subnetmask)
    keyword_map['ip_and_subnetmask'] = network_id_and_subnet

  if create_subnets is not None:
    subnet_info = tuple(create_subnets)
    keyword_map['create_subnets'] = subnet_info

  if create_hosts is not None:
    host_info = tuple(create_hosts)
    keyword_map['create_hosts'] = host_info


  return keyword_map


def str_serializer(arg):
  arr = map(str, arg)
  arr = '.'.join(arr)
  return arr


if __name__ == '__main__':

  subnet_node = Subnet()
  create = CreateSubnetwork()

  parse_object = parser_child.parser
  
  # Unpacks keyword_map into args_map
  args_map = argparse_unpacker(parse_object)

  # Gracefully handles the exception of passing one flag
  try:
    network_prefix = args_map['network_prefix']
    net, submask = prefix_to_decimal_converter(network_prefix)
  except KeyError:
    net, submask = args_map['ip_and_subnetmask']
  
  ip_address_class = subnet_node.ip_class(net)
  network_info = subnet_node.get_network_id(net, submask)
  available_ip = subnet_node.subnet_ip_addresses(submask)

  if len(args_map) == 2:
    #====================
    #Creating Subnetworks
    #====================
    if args_map.__contains__('create_subnets'):

      sub_quantity = args_map['create_subnets'][0]

      # Generates networks metadata. Contains base address, new address and subnet bits
      metadata = create.generate_metadata(sub_quantity=sub_quantity, parent_addr=network_prefix)
      parent = metadata['parent_addr']
      child = metadata['child_addr']
      #subnet = metadata['subnet_bits']
      
      parent_mask = str_serializer(parent['subnet_mask'])
      child_mask = str_serializer(child['subnet_mask'])
      parent_hosts = create.generate_addresses(parent_mask)
      child_hosts = create.generate_addresses(child_mask)

      print(f"Base Network ID of {parent['network_id']} => {parent_hosts} Hosts.")
      print(f"Network ID => {parent['network_id']}")
      print(f'{sub_quantity} newly created subnetworks defined with {child_hosts} Hosts ')

    # Then args_map contains create_hosts
    else:
      host_quantity = args_map['create_hosts'][0]
      metadata = create.generate_metadata(host_quantity=host_quantity, parent_addr=network_prefix)
      parent = metadata['parent_addr']
      child = metadata['child_addr']
      
      parent_mask = str_serializer(parent['subnet_mask'])
      child_mask = str_serializer(child['subnet_mask'])

      parent_ip = create.generate_addresses(parent_mask)
      child_ip = create.generate_addresses(child_mask)
      print(f"Base Network ID of {parent['network_id']} => {parent_ip} Hosts")
      print(f'{child_ip} newly created hosts defined within xx Subnetworks')

  else:
    print(ip_address_class)
    print(f"Base Network ID => {network_info['network_id']}")
    print(f'Number of available hosts or IP Addresses => {available_ip}')

