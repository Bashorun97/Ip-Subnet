import sys

command_list = sys.argv
legal_octets = [0,128, 192, 224, 248, 252, 254, 255, 240]

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
    print(f"Your networkID =>  {metadata['network_id']}")

  def subnet_ip_addresses(self, decimal_subnet):
    # convert decimal subnet to CID notation
    subnet_mask = list(map(int, decimal_subnet.split('.')))
    cidr_list = [bin(octet).strip('0b') for octet in subnet_mask]
    cidr = sum(list(map(len, cidr_list)))
    range_of_addresses = 2**(32 - cidr) -2
    print(f'Number of IP Addresses => {range_of_addresses}')

def command_handler(flag):
  loop = True
  while loop:
    try:
      if flag == '--ip-addr':
        ip_addr = str(input('Enter ip: '))
        subnet = str(input('Enter subnet: '))
        return ip_addr, subnet
      elif flag == '--cidr-addr':
        ip_addr = str(input('Enter IP in CIDR notation:' ))
        ip_addr_list = ip_addr.split('/')
        cidr = ip_addr_list.pop()
        # logic for --cidr-addr
        pass
        return ip_addr, subnet
      else:
        print(f'Invalid flag')
        sys.exit()
      loop = False
    except IndexError:
      print('Exit')
      break

#def caller(
 #return command_list
if __name__ == '__main__':
  try:
    flag_type = command_list[1]
  except IndexError:
    print('Use a flag')
    sys.exit()
  command_soup = command_handler(flag_type)
  ip, subnet_mask = command_soup[0], command_soup[1]
  subnet = NetworkId()
  subnet.get_network_id(ip,subnet_mask)
  subnet.subnet_ip_addresses(subnet_mask)
 
