import argparse
import parser_parent

parser = argparse.ArgumentParser(
    parents=[parser_parent.parser],
    )

creation_group = parser.add_mutually_exclusive_group()
parser.add_argument('--create-subnets',
    nargs=1,
    action='store',
    type=int, dest='create_subnets',
    help='Creates subnets within given address by specifying the number of \
        subnets followed by IP address in CIDR notation. i.e. ip_subnet --create-subnets 6 -c 192.168.73.1/24.'
        )

creation_group.add_argument('--create-hosts',
    nargs=1,
    action='store',
    type=int, dest='create_hosts',
    help='Creates subnetwors based off the given number of hosts'
    )
