from os import path
from sys import stdin, stdout
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
    prog="Wc",
    description="WC"
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
    if stdin.isatty():
        stdout.write("filename is required")
    else:
        content = stdin.readlines()

        output = ""
        

        if args.lines:
            output += f" {count_lines(content)}"

        if args.words:
            output += f" {count_words(content)}"

        if args.count:
            output += f" {count_bytes(content)}"
        
        if args.chars:
            output += f" {count_chars(content)}"

        stdout.write(output)

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

        stdout.write(output)
    else:
        stdout.write(f"File {filename} not found")