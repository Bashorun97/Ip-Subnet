#!/usr/bin/env python3
# Tue May 26 22:16:31 WAT 2020
# babaibeji

import sys
from octet_mapping import *

command_list = sys.argv

class Data:
  def __init__(self, ip, subnet_mask):
    self.ip = ip
    self.subnet_mask = subnet_mask

class NetworkId:
  def get_network_id(self, ip, subnet_mask):
    ip_address = Data(ip, subnet_mask)
    ip = list(map(int, ip_address.ip.split('.')))
    subnet_mask = list(map(int, ip_address.subnet_mask.split('.')))
    network_id = '.'.join(list(map(str, [i&j for i,j in zip(ip, subnet_mask)])))
    metadata = {'network_id':network_id, 'subnet_mask':subnet_mask}
    print(f"NetworkID =>  {metadata['network_id']}")

  def subnet_ip_addresses(self, decimal_subnet):
    subnet_mask = list(map(int, decimal_subnet.split('.')))
    cidr_list = [bin(octet).strip('0b') for octet in subnet_mask]
    cidr = sum(list(map(len, cidr_list)))
    range_of_addresses = 2**(32 - cidr) -2
    print(f'Number of available IP Addresses => {range_of_addresses}')

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
      print(f'Incorrect IP class')
      sys.exit()

def command_handler(flag):
  loop = True
  while loop:
    try:
      if flag == '--ip-addr':
        ip_addr = str(input('Enter ip: '))
        subnet = str(input('Enter subnet: '))
        return ip_addr, subnet
      elif flag == '--cidr-addr':
        ip_addr = str(input('Enter IP in CIDR notation: ' ))
        #Converts CIDR to decimal
        ip_addr_list = ip_addr.split('/')
        network_prefix = ip_addr_list[0]
        cidr = ip_addr_list.pop()
        subnet_mask = '1'*int(cidr) + (32-int(cidr))*'0'
        first_octet = subnet_mask[:8]
        second_octet = subnet_mask[8:16]
        third_octet = subnet_mask[16:24]
        fourth_octet = subnet_mask[24:]
        subnet_list = [octet_mapping[int(first_octet)], octet_mapping[int(second_octet)], octet_mapping[int(third_octet)], octet_mapping[int(fourth_octet)]]
        subnet = '.'.join(subnet_list)
        return network_prefix, subnet
      else:
        print(f'Invalid flag')
        sys.exit()
      loop = False
    except IndexError:
      print('Exit')
      break

if __name__ == '__main__':
  try:
    flag_type = command_list[1]
  except IndexError:
    print('Use a flag')
    sys.exit()
  command_soup = command_handler(flag_type)
  ip, subnet_mask = command_soup[0], command_soup[1]
  subnet = NetworkId()
  print(subnet.ip_class(ip))
  subnet.get_network_id(ip,subnet_mask)
  subnet.subnet_ip_addresses(subnet_mask)

