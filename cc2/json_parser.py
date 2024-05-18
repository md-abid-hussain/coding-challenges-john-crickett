import sys
from typing import List
from enum import Enum

class InvalidTokenException(Exception):
    pass

class InvalidJSONException(Exception):
    pass

class TokenType(Enum):
    START_OBJECT = 0
    END_OBJECT = 1
    KEY = 2
    VALUE = 3
    COLON = 4
    COMMA = 5
    ARRAY_OPEN = 6
    ARRAY_CLOSE = 7

    DELIMITER = 12

class Token:
    def __init__(
        self, token_type: TokenType, value, line: int | None, position: int | None
    ):
        self.type = token_type
        self.value = value
        self.line = line
        self.position = position

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return str(self.value)

    @classmethod
    def delimiter(cls):
        return Token(TokenType.DELIMITER, ".", None, None)

    @classmethod
    def isnumeric(cls,numeric_string: str) -> bool:
        try:
            int(numeric_string)
            return True
        except ValueError:
            pass
        try:
            float(numeric_string)
            return True
        except ValueError:
            return False
        
    @classmethod
    def find_last_index(cls,string: str, offset: int, char: str, alt_char: str):
        count = 0
        index = 0
        while index < len(string):
            if string[index] == alt_char:
                count += 1

            if string[index] == char:
                if count > 0:
                    count -= 1
                else:
                    return offset + index + 1

            index += 1

        return -1

class JsonParser:
    def __init__(self, json_string):
        self.json_string = json_string

    def _tokenizer(self):
        self.tokens = tokenize(self.json_string)
        return self.tokens

    def parse(self):
        try:
            return parse(self._tokenizer())
        except InvalidTokenException as ite:
            print(ite)
        except InvalidJSONException as ije:
            print(ije)

        sys.exit(2)
    


def tokenize_array(array_string: str, line, position) -> List[Token]:
    tokens: List[Token] = []
    index = 0

    while index < len(array_string):
        character = array_string[index]

        if character.isspace():
            pass
        elif character == ",":
            tokens.append(Token(TokenType.COMMA, ",", line, position))
        elif character == '"':
            string_index = array_string.find('"', index + 1)
            if string_index == -1:
                raise InvalidTokenException(
                    f"Invalid token: Expected string but got {character} at line {line} position {position}"
                )
            tokens.append(
                Token(
                    TokenType.VALUE,
                    array_string[index : string_index + 1],
                    line,
                    position,
                )
            )
            position += string_index - index
            index = string_index

        elif character == "t":
            if array_string[index : index + 4] == "true":
                tokens.append(Token(TokenType.VALUE, True, line, position))
                index = index + 4
                position += 4
            else:
                raise InvalidTokenException(
                    f"Invalid token: Expected true got {array_string[index:index+4]} at line {line} position {position}"
                )

        elif character == "f":
            if array_string[index : index + 5] == "false":
                tokens.append(Token(TokenType.VALUE, False, line, position))
                position += 4
                index = index + 5
            else:
                raise InvalidTokenException(
                    f"Invalid token: Expected false got {array_string[index:index+5]} at line {line} position {position}"
                )

        elif character == "n":
            if array_string[index : index + 4] == "null":
                tokens.append(Token(TokenType.VALUE, None, line, position))
                position += 4
                index = index + 4
            else:
                raise InvalidTokenException(
                    f"Invalid token: Expected null got {array_string[index:index+4]} at line {line} position {position}"
                )

        elif character.isdecimal():
            num_string_end = array_string.find(",", index)

            if num_string_end == -1:
                num_string_end = array_string.find("}", index)

            if num_string_end == -1:
                raise InvalidTokenException(
                    f"Invalid token: Expected number {array_string[index:]} at line {line} position {position} to be followed by , or {"}"}"
                )

            num_string = array_string[index:num_string_end].strip()

            if num_string.isnumeric():
                tokens.append(Token(TokenType.VALUE, int(num_string), line, position))
            elif Token.isnumeric(num_string):
                tokens.append(Token(TokenType.VALUE, float(num_string), line, position))
            else:
                raise InvalidTokenException(
                    f"Invalid token: Expected number got {num_string} at line {line} position {position}"
                )

            index = num_string_end - 1
        elif character == "{":
            end_str_index = Token.find_last_index(array_string[index + 1 :], index, "}", "{")
            if end_str_index == -1:
                raise InvalidTokenException(
                    f"Invalid token: at {array_string[index]} at line {line} position {position}"
                )
            inner_json_token = tokenize(
                array_string[index : end_str_index + 1], line, position
            )
            tokens += inner_json_token
            index = end_str_index
        else:
            raise InvalidTokenException(
                f"Invalid token: {array_string[index]} at line {line} position {position}"
            )

        index += 1
        position += 1

    return tokens


def tokenize(json_string: str, line=0, position=0) -> List[Token]:
    tokens: List[Token] = []
    index = 0

    is_key = True

    while index < len(json_string):
        character = json_string[index]

        if character == ":":
            tokens.append(Token(TokenType.COLON, ":", line, position))
        elif character == ",":
            tokens.append(Token(TokenType.COMMA, ",", line, position))
        elif not is_key:
            if character == '"':
                end_string_index = json_string.find('"', index + 1)
                if end_string_index == -1:
                    raise InvalidTokenException(
                        f"Invalid token: Expected string but got {character} at line {line} position {position}"
                    )
                tokens.append(
                    Token(
                        TokenType.VALUE,
                        json_string[index : end_string_index + 1],
                        line,
                        position,
                    )
                )
                position += end_string_index - index
                index = end_string_index
            elif character == "t":
                if json_string[index : index + 4] == "true":
                    tokens.append(Token(TokenType.VALUE, True, line, position))
                    index = index + 3
                    position += 3
                else:
                    raise InvalidTokenException(
                        f"Invalid token: Expected true got {json_string[index:index+4]} at line {line} position {position}"
                    )

            elif character == "f":
                if json_string[index : index + 5] == "false":
                    tokens.append(Token(TokenType.VALUE, False, line, position))
                    position += 4
                    index = index + 4
                else:
                    raise InvalidTokenException(
                        f"Invalid token: Expected false got {json_string[index:index+5]} at line {line} position {position}"
                    )

            elif character == "n":
                if json_string[index : index + 4] == "null":
                    tokens.append(Token(TokenType.VALUE, None, line, position))
                    position += 3
                    index = index + 3
                else:
                    raise InvalidTokenException(
                        f"Invalid token: Expected null got {json_string[index:index+4]} at line {line} position {position}"
                    )

            elif character.isdecimal():
                num_string_end = json_string.find(",", index)

                if num_string_end == -1:
                    num_string_end = json_string.find("}", index)

                if num_string_end == -1:
                    raise InvalidTokenException(
                        f"Invalid token: Expected number {json_string[index:]} at line {line} position {position} to be followed by , or {"}"}"
                    )

                num_string = json_string[index:num_string_end].strip()
                if num_string.isnumeric():
                    tokens.append(
                        Token(TokenType.VALUE, int(num_string), line, position)
                    )
                elif Token.isnumeric(num_string):
                    tokens.append(
                        Token(TokenType.VALUE, float(num_string), line, position)
                    )
                else:
                    raise InvalidTokenException(
                        f"Invalid token: Expected number got {num_string} at line {line} position {position}"
                    )

                index = num_string_end - 1
            elif character == "{":
                end_str_index = Token.find_last_index(
                    json_string[index + 1 :], index, "}", "{"
                )
                if end_str_index == -1:
                    raise InvalidTokenException(
                        f"Invalid token: at {json_string[index]} at line {line} position {position}"
                    )
                inner_json_token = tokenize(
                    json_string[index : end_str_index + 1], line, position
                )
                tokens += inner_json_token
                index = end_str_index
            elif character == "[":
                end_bracket_index = Token.find_last_index(
                    json_string[index + 1 :], index, "]", "["
                )
                if end_bracket_index == -1:
                    raise InvalidTokenException(
                        f"Invalid token: Expected ] for {character} at line {line} position {position} "
                    )
                array_string = json_string[index + 1 : end_bracket_index]
                array_tokens = tokenize_array(array_string, line, position)
                tokens.append(Token(TokenType.ARRAY_OPEN, "[", line, position))
                tokens += array_tokens
                tokens.append(Token(TokenType.ARRAY_CLOSE, "]", line, position))
                position += end_bracket_index - index
                index = end_bracket_index

            elif character.isspace():
                pass
            else:
                raise InvalidTokenException(
                    f"Invalid token: {json_string[index]} at line {line} position {position}"
                )

            if character.isspace():
                pass
            else:
                is_key = not is_key
        elif character == "{":
            tokens.append(Token(TokenType.START_OBJECT, "{", line, position))
        elif character == "}":
            tokens.append(Token(TokenType.END_OBJECT, "}", line, position))
        elif character == '"':
            end_string_index = json_string.find('"', index + 1)
            if end_string_index == -1:
                raise InvalidTokenException(
                    f"Invalid token: Expected a string key got {json_string[index:]} at line {line} position {position}"
                )
            tokens.append(
                Token(
                    TokenType.KEY,
                    json_string[index : end_string_index + 1],
                    line,
                    position,
                )
            )
            is_key = not is_key
            position += end_string_index - index
            index = end_string_index
        elif character.isspace():
            pass
        else:
            raise InvalidTokenException(
                f"Invalid token: {character} at line {line} position {position}"
            )

        position += 1

        if character == "\n":
            line += 1
            position = 0

        index += 1

    return tokens

def parse(tokens: List[Token]):
    validate_syntax(tokens)
    _, json_dict = tokens_to_dict(tokens)
    return json_dict

def validate_syntax(tokens: List[Token]):
    stack: List[Token] = []

    if not tokens:
        raise InvalidJSONException("Invalid JSON string: expected {")

    if tokens[0].type != TokenType.START_OBJECT:
        raise InvalidJSONException(
            f"Invalid token: Expected {"{"} got {tokens[0].value} at line {tokens[0].line} position {tokens[0].position}"
        )

    last_token = tokens[0]

    stack.append(tokens[0])
    index = 1
    while index < len(tokens):
        if tokens[index].type == TokenType.START_OBJECT:
            if (
                len(stack) >= 2
                and stack[-1].type == TokenType.COLON
                and stack[-2].type == TokenType.KEY
            ):
                stack.append(tokens[index])
                stack.append(Token.delimiter())
            else:
                raise InvalidJSONException(
                    f"Invalid token: Expected : got {tokens[index].value} at line {tokens[index].line} position {tokens[index].position}"
                )
        if tokens[index].type == TokenType.END_OBJECT:
            if last_token.type == TokenType.COMMA:
                raise InvalidJSONException(
                    f"Invalid token: Expected key got {tokens[index].value} at line {tokens[index].line} position {tokens[index].position}"
                )

            elif stack and stack[-1].type == TokenType.DELIMITER:
                stack.pop()
                stack.pop()
                stack.pop()
                stack.pop()
            elif stack and stack[-1].type == TokenType.START_OBJECT:
                stack.pop()
            else:
                raise InvalidJSONException(
                    f"Invalid token: {tokens[index].value} at line {tokens[index].line} position {tokens[index].position}"
                )
        elif tokens[index].type == TokenType.KEY:
            if stack[-1].type == TokenType.DELIMITER or stack[-1].type == TokenType.START_OBJECT:
                pass
            elif stack[-1].type == TokenType.COMMA:
                stack.pop()
            else:
                raise InvalidJSONException(
                    f"Invalid token: Expected , got {tokens[index].value} at line {tokens[index].line} position {tokens[index].position}"
                )
            stack.append(tokens[index])
        elif tokens[index].type == TokenType.COLON:
            if stack[-1].type == TokenType.KEY:
                stack.append(tokens[index])
            else:
                raise InvalidJSONException(
                    f"Invalid token: Expected key got {tokens[index].value} at line {tokens[index].line} position {tokens[index].position}"
                )
        elif tokens[index].type == TokenType.VALUE:
            if (
                len(stack) >= 2
                and stack[-1].type == TokenType.COLON
                and stack[-2].type == TokenType.KEY
            ):
                stack.pop()
                stack.pop()
            else:
                raise InvalidJSONException(
                    f"Invalid token: Expected : got {tokens[index].value} at line {tokens[index].line} position {tokens[index].position}"
                )
        elif tokens[index].type == TokenType.COMMA:
            if (
                last_token.type != TokenType.VALUE
                and last_token.type != TokenType.END_OBJECT
            ):
                raise InvalidJSONException(
                    f"Invalid token: {tokens[index].value} at line {tokens[index].line} position {tokens[index].position}"
                )
            stack.append(tokens[index])
        elif tokens[index].type == TokenType.ARRAY_OPEN:
            if stack[-1].type == TokenType.COLON and stack[-2].type == TokenType.KEY:
                stack.append(tokens[index])
                stack.append(Token.delimiter())
                last_token = tokens[index]
                index = index + 1

                while tokens[index].type != TokenType.ARRAY_CLOSE:
                    if tokens[index].type not in [
                        TokenType.VALUE,
                        TokenType.COMMA,
                        TokenType.START_OBJECT,
                        TokenType.END_OBJECT,
                    ]:
                        raise InvalidJSONException(f"Invalid token: Expected value, comma(,), {"{, }"} got {tokens[index].value} at line {tokens[index].line} position {tokens[index].position}")
                    if tokens[index].type == TokenType.START_OBJECT:
                        temp_index = index
                        while tokens[temp_index].type != TokenType.END_OBJECT:
                            temp_index += 1
                        end_object_index = temp_index
                        validate_syntax(tokens[index : end_object_index + 1])
                        index = end_object_index
                    last_token = tokens[index]
                    index = index + 1

                if tokens[index].type == TokenType.ARRAY_CLOSE and last_token.type in [
                    TokenType.VALUE,
                    TokenType.END_OBJECT,
                    TokenType.ARRAY_OPEN,
                ]:
                    stack.pop()
                    stack.pop()
                    stack.pop()
                    stack.pop()
                else:
                    raise InvalidJSONException(f"Invalid token: {tokens[index].value} at line {tokens[index].line} position {tokens[index].position}")

            else:
                raise InvalidJSONException(f"Invalid token: {tokens[index].value} at line {tokens[index].line} position {tokens[index].position}")

        last_token = tokens[index]
        index = index + 1

    if len(stack):
        raise InvalidJSONException(f"Invalid JSON: Unbalanced tokens {stack}")
    
def create_array(tokens:List[Token]):
    array = []
    index=1
    while tokens[index].value != ']':
        token_val = tokens[index].value
        if token_val == ',':
            index += 1
            continue
        elif token_val == '{':
            last_index, inner_json = tokens_to_dict(tokens[index:])
            index = index+last_index
            array.append(inner_json)
        else:
            array.append(token_val)
        index = index+1
    return index, array

def tokens_to_dict(tokens:List[Token]):
    result = {}
    key = None
    index = 0
    while index < len(tokens):
        token_val = tokens[index].value
        if (key is None and token_val == '{') or token_val == ',' or token_val == ':':
            index += 1
            continue
        elif token_val == '}':
            break
        elif key is None:
            key = token_val
        else:
            if token_val == '{':
                last_index, result[key] = tokens_to_dict(tokens[index:])
                index = index+last_index
            elif token_val == '[':
                last_index, array = create_array(tokens[index:])
                result[key] = array
                index = index+last_index
            else:
                result[key] = token_val
            key = None
        index += 1
    return index, result

__all__ = ["JsonParser"]