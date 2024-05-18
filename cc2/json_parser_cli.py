import os
import argparse
import sys
from json_parser import JsonParser

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
        print("Invalid way to invoke")
        print("usage: json_parser [-h] -f FILENAME")
        print("Example : cat test.json | python json_parser_cli.py\n\t  python json_parser_cli.py -f test.json")
        sys.exit(1)
    else:
        content = sys.stdin.read()
        json = JsonParser(content)
        json_dict = json.parse()
        print(json_dict)
        sys.exit(0)

else :
    relative_path = os.path.dirname(__file__)
    filepath = os.path.join(relative_path, filename)
    if os.path.exists(filepath) :
        with open(filepath, 'r', encoding='utf8') as file:
            data = file.read()
        json = JsonParser(data)
        json_dict = json.parse()
        print(json_dict)
        sys.exit(0)