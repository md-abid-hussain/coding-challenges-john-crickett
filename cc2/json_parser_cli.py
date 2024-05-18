import os
import argparse
import sys
from json_parser import InvalidJSONException, InvalidTokenException, JsonParser
import json

parser = argparse.ArgumentParser(
    prog="json parser",
    description="json parser implementation in python",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog='''
Example : cat test.json | python json_parser_cli.py
          python json_parser_cli.py -f test.json
'''
)

parser.add_argument("-f", "--filename", help="file name", nargs="?")

args = parser.parse_args()

filename = args.filename

if filename is None:
    if sys.stdin.isatty():
        sys.stdout.write("Invalid way to invoke")
        sys.stdout.write("usage: json_parser [-h] -f FILENAME")
        sys.stdout.write("Example : cat test.json | python json_parser_cli.py\n\t  python json_parser_cli.py -f test.json")
        sys.exit(1)
    else:
        content = sys.stdin.read()
        try:
            json_data = JsonParser(content)
            json_dict = json_data.parse()
            sys.stdout.write(json.dumps(json_dict))
            sys.exit(0)
        except InvalidTokenException as ite:
            sys.stderr.write(ite)
            sys.exit(3)
        except InvalidJSONException as ije:
            sys.stderr.write(ije)
            sys.exit(3)

else :
    relative_path = os.path.dirname(__file__)
    filepath = os.path.join(relative_path, filename)
    if os.path.exists(filepath) :
        with open(filepath, 'r', encoding='utf8') as file:
            data = file.read()
        try:
            json_data = JsonParser(data)
            json_dict = json_data.parse()
            sys.stdout.write(json.dumps(json_dict))
            sys.exit(0)
        except InvalidTokenException as ite:
            sys.stderr.write(ite)
            sys.exit(3)
        except InvalidJSONException as ije:
            sys.stderr.write(ije)
            sys.exit(3)
    else:
        sys.stderr.write('File not found')
        sys.exit(2)