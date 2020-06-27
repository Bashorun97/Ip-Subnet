import argparse
import parser_parent

parser = argparse.ArgumentParser(
    parents=[parser_parent.parser],
    )

parser.add_argument('--create-subnets',
    nargs=1,
    action='append',
    type=int, dest='subnetworks_info',
    help='Creates subnets  within given address by specifying the number of \
        subnets followed by hosts. i.e. ip_subnet --create-subnets 6 25. the flag\'s argument'
        )
