from os import path
import sys
import argparse

def count_bytes(data:str, is_filename:bool = False):
    if is_filename:
        return path.getsize(data)
    else:
        content = "\n".join(data)
        return len(content.encode("utf8")) + 1

def count_lines(data:str, is_filename:bool = False):
    if is_filename:
        with open(data, "r", encoding="utf8") as file:
            for count, line in enumerate(file):
                pass
        return count + 1
    return len(data)

def count_words(data:str, is_filename:bool = False):
    if is_filename:
        with open(data, "r", encoding="utf8") as file:
            words = 0
            for line in file:
                words = words + len(line.split())
        return words
    
    words = 0
    for line in data:
        words +=len(line.split())
    return words

def count_chars(data:str, is_filename:bool = False):
    if is_filename:
        with open(data, "r", encoding="utf-8-sig") as file:    
            chars = 0
            for line in file:
                chars += len(line)+1

        return chars + 1
            
    chars = 0
    for line in data:
        chars += len(line) + 1
        pass

    return chars
    
parser = argparse.ArgumentParser(
    prog="ccwc",
    description="wc implementation in python",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog='''
Example : cat test.txt | python ccwc.py -l
          python ccwc.py text.txt -l -w
'''
)

parser.add_argument("-l", "--lines", action="store_true", help="number of lines")
parser.add_argument("-c", "--count", action="store_true", help="number of bytes")
parser.add_argument("-w", "--words", action="store_true", help="number of words")
parser.add_argument("-m", "--chars", action="store_true", help="number of characters")
parser.add_argument("filename" , nargs="?")

args = parser.parse_args()

filename = args.filename

if not (args.count or args.lines or args.words or args.chars):
    args.count = True
    args.lines = True
    args.words = True

if filename is None:
    if sys.stdin.isatty():
        sys.stdout.write("Invalid way to invoke\n")
        sys.stdout.write("usage: python ccwc.py [-h] [-l] [-c] [-w] [-m] [filename]\n")
        sys.stdout.write("Example : cat test.txt | python ccwc.py -l\n\t  python ccwc.py text.txt -l -w")
        sys.exit(1)
    else:
        content = sys.stdin.readlines()

        output = ""
        

        if args.lines:
            output += f" {count_lines("".join(content))}"

        if args.words:
            output += f" {count_words("".join(content))}"

        if args.count:
            output += f" {count_bytes("".join(content))}"
        
        if args.chars:
            output += f" {count_chars("".join(content))}"

        sys.stdout.write(output)
        sys.exit(0)

else:

    if path.exists(filename):

        output = ""

        if args.lines:
            output += f" {count_lines(filename, True)}"

        if args.words:
            output += f" {count_words(filename, True)}"

        if args.count:
            output += f" {count_bytes(filename, True)}"
        
        if args.chars:
            output += f" {count_chars(filename, True)}"

        output += f" {filename}"

        sys.stdout.write(output)
        sys.exit(0)
    else:
        sys.stdout.write(f"file {filename} not found")
        sys.exit(1)