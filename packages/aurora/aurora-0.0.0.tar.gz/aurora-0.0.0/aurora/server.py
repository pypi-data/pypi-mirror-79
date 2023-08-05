import os
import sys
import argparse

def main(argv=sys.argv[1:]):

    # TODO: need to add which directory to poll
    # I think we might actually just want to point to a config.py or something
    parser = argparse.ArgumentParser(description='Aurora server')
    parser.add_argument('db', help='Database file')
    parser.add_argument('-p', '--port', help='The port to listen to')
    parser.add_argument('-H', '--host', help='The host to listen on')
    args = parser.parse_args(argv)

    port = args.port if args.port else 5000
    host = args.host if args.host else 'localhost'

    print(f'Running Aurora on http://{host}:{port}')

