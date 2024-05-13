from typing import List
from enum import Enum

class TokenType(Enum):
    START_OBJECT = 'start object'
    END_OBJECT = 'end object'
    KEY = 'key'
    VALUE = 'value'
    COLON = 'colon'
    COMMA = ','
    ARRAY_OPEN = '['
    ARRAY_CLOSE = ']'
    
class Token:
    def __init__(self, token_type:TokenType, value, line:int, position:int):
        self.type = token_type
        self.value = value
        self.line = line
        self.position = position

    # def __str__(self) -> str:
    #     return f'{self.value} at line {self.line} position {self.position}'
    
    # def __repr__(self) -> str:
    #     return f'{self.value} at line {self.line} position {self.position}'
    
    def __str__(self) -> str:
        return str(self.type.value)

    def __repr__(self) -> str:
        return str(self.type.value)

    def create_key_or_value(key_or_value:str, is_key:bool, line, position):
        return Token(TokenType.KEY, key_or_value, line, position) if is_key else Token(TokenType.VALUE, key_or_value, line, position)
    
    def isnumeric(numeric_string) -> bool:
        try:
            float(numeric_string)
            return True
        except ValueError:
            return False

def find_last_index(string:str, char:str, alt_char:str):
    print(string)
    count = 0
    index = 0
    while index < len(string):
        if string[index] == alt_char:
            count += 1

        if string[index] == char:
            if count > 0:
                count -= 1
            else:
                return index
        index += 1

    return -1


def tokenize_array(array_string:str, line, position) -> List[Token]:
    tokens:List[Token] = []
    index = 0

    while index < len(array_string):
        character = array_string[index]

        if character.isspace():
            pass
        elif character == ',':
            tokens.append(Token(TokenType.COMMA,',' ,line, position))
        elif character == '"':
            string_index = array_string.find('"',index+1)
            if string_index == -1:
                raise SyntaxError(f'Invalid token {array_string[index]} at line {line} position {position}')
            tokens.append(Token(TokenType.VALUE, array_string[index:string_index+1], line, position))
            position += string_index - index
            index = string_index
        
        elif character == 't':
            if array_string[index: index+4] == 'true':
                tokens.append(Token(TokenType.VALUE, True, line, position))
                index = index + 4
                position += 4
            else:
                raise SyntaxError(f'Invalid token {array_string[index:index+4]} at line {line} position {position}')
        
        elif character == 'f':
            if array_string[index: index+5] == 'false':
                tokens.append(Token(TokenType.VALUE, False, line, position))
                position += 4
                index = index + 5
            else:
                raise SyntaxError(f'Invalid token {array_string[index:index+5]} at line {line} position {position}')

        elif character == 'n':
            if array_string[index: index+4] == 'null':
                tokens.append(Token(TokenType.VALUE, None, line, position))
                position += 4
                index = index + 4
            else:
                raise SyntaxError(f'Invalid token {array_string[index:index+5]} at line {line} position {position}')

        elif character.isdecimal():
            num_string_end = array_string.find(',', index)

            if num_string_end == -1:
                num_string_end = array_string.find('}', index)

            if num_string_end == -1:
                raise SyntaxError(f'Invalid token {array_string[index:]} at line {line} position {position}')
            # while array_string[num_string_index].isdecimal() and array_string[num_string_index] != ',':
            #     num_string_index += 1

            num_string = array_string[index : num_string_end]

            if num_string.isnumeric():
                tokens.append(Token(TokenType.VALUE, int(num_string), line, position))
            elif Token.isnumeric(num_string):
                tokens.append(Token(TokenType.VALUE, float(num_string), line, position))
            else:
                raise SyntaxError(f'Invalid token {num_string} at line {line} position {position}')
            
            index = num_string_end - 1

        # elif character == '{':
        #     tokens.append(Token(TokenType.START_OBJECT, '{', line, position))
        # elif character == '}':
        #     tokens.append(Token(TokenType.END_OBJECT, '}', line, position))
        elif character == '{':
            end_str_index = array_string.find('}', index)
            # end_str_index = find_last_index(array_string[index+1:], '}', '{')
            if end_str_index == -1:
                raise SyntaxError(f'Invalid token at {array_string[index]} at line {line} position {position}')
            inner_json_token = tokenize(array_string[index:end_str_index+1], line, position)
            inner_json_token.append(Token(TokenType.END_OBJECT, '}', line , position))
            tokens += inner_json_token
            index = end_str_index
        # elif character == '}':
        #     tokens.append(Token(TokenType.END_OBJECT, '}', line, position))
        else :
            raise SyntaxError(f'Invalid token {array_string[index]} at line {line} position {position}')
        
        index += 1
        position += 1

    return tokens

def tokenize(json_string:str, line = 0, position = 0) -> List[Token]:
    tokens:List[Token] = []
    index = 0

    is_key = True

    while index < len(json_string):
        character = json_string[index]

        if character == ':':
            tokens.append(Token(TokenType.COLON, ':',line, position))
        elif character == ',':
            tokens.append(Token(TokenType.COMMA, ',', line, position))
        elif not is_key:
            if character == '"':
                end_string_index = json_string.find('"',index+1)
                if end_string_index == -1:
                    raise SyntaxError(f'Invalid token {json_string[index:]} at line {line} position {position}')
                tokens.append(Token(TokenType.VALUE,json_string[index: end_string_index+1], line, position))
                position += end_string_index - index
                index = end_string_index
            elif character == 't':
                if json_string[index: index+4] == 'true':
                    tokens.append(Token(TokenType.VALUE, True, line, position))
                    index = index + 3
                    position += 3
                else:
                    raise SyntaxError(f'Invalid token {json_string[index:index+4]} at line {line} position {position}')
                
            elif character == 'f':
                if json_string[index: index+5] == 'false':
                    tokens.append(Token(TokenType.VALUE, False, line, position))
                    position += 4
                    index = index + 4
                else:
                    raise SyntaxError(f'Invalid token {json_string[index:index+5]} at line {line} position {position}')

            elif character == 'n':
                if json_string[index: index+4] == 'null':
                    tokens.append(Token(TokenType.VALUE, None, line, position))
                    position += 3
                    index = index + 3
                else:
                    raise SyntaxError(f'Invalid token {json_string[index:index+5]} at line {line} position {position}')

            elif character.isdecimal():
                num_string_end = json_string.find(',', index)

                if num_string_end == -1:
                    num_string_end = json_string.find('}', index)

                if num_string_end == -1:
                    raise SyntaxError(f'Invalid token {json_string[index:]} at line {line} position {position}')

                num_string = json_string[index : num_string_end]

                if num_string.isnumeric():
                    tokens.append(Token(TokenType.VALUE, int(num_string), line, position))
                elif Token.isnumeric(num_string):
                    tokens.append(Token(TokenType.VALUE, float(num_string), line, position))
                else:
                    raise SyntaxError(f'Invalid token {num_string} at line {line} position {position}')
                
                index = num_string_end - 1

            # elif character == '{':
            #     tokens.append(Token(TokenType.START_OBJECT, '{', line, position))
            # elif character == '}':
            #     tokens.append(Token(TokenType.END_OBJECT, '}', line, position))
            elif character == '{':
                end_str_index = json_string.find('}', index)
                # end_str_index = find_last_index(json_string[index+1:], '}', '{')
                if end_str_index == -1:
                    raise SyntaxError(f'Invalid token at {json_string[index]} at line {line} position {position}')
                inner_json_token = tokenize(json_string[index:end_str_index+1], line, position)
                # inner_json_token.append(Token(TokenType.END_OBJECT, '}', line, position))
                tokens += inner_json_token
                index = end_str_index
            elif character == '[':
                end_bracket_index = json_string.find(']', index)
                if end_bracket_index == -1:
                    raise SyntaxError('Invalid JSON string ]')
                array_string = json_string[index+1 : end_bracket_index]
                array_tokens = tokenize_array(array_string, line, position)
                tokens.append(Token(TokenType.ARRAY_OPEN, '[', line, position))
                tokens += array_tokens
                tokens.append(Token(TokenType.ARRAY_CLOSE, ']', line, position))
                position += end_bracket_index - index
                index = end_bracket_index
                
            elif character.isspace():
                pass
            else :
                raise SyntaxError(f'Invalid token {json_string[index]} at line {line} position {position}')
            
            if character.isspace():
                pass
            else :
                is_key = not is_key
        elif character == '{':
            tokens.append(Token(TokenType.START_OBJECT, '{', line, position))
        elif character == '}':
            tokens.append(Token(TokenType.END_OBJECT, '}', line, position))
        elif character == '"':
            end_string_index = json_string.find('"',index+1)
            if end_string_index == -1:
                raise SyntaxError(f'Invalid token {json_string[index:]} at line {line} position {position}')
            tokens.append(Token(TokenType.KEY,json_string[index: end_string_index+1], line, position))
            is_key = not is_key
            position += end_string_index - index
            index = end_string_index
        elif character.isspace():
            pass
        else :
            raise SyntaxError(f'Invalid token {character} at line {line} position {position}')
        
        position += 1

        if character == '\n':
            line += 1
            position = 0

        index += 1

    return tokens
    
def parse(tokens:List[Token]):
    validate_syntax(tokens)

    parsed_json = dict()

    return parsed_json

def validate_syntax(tokens:List[Token]):
    stack:List[Token] = []

    if not tokens:
        raise SyntaxError('Invalid JSON string')

    if tokens[0].type != TokenType.START_OBJECT:
        raise SyntaxError(f'Invalid character {tokens[0].value} at line {tokens[0].line} position {tokens[0].position}')
    
    last_token = tokens[0]
    
    stack.append(tokens[0])
    index = 1
    # print(0, stack)
    # print("last token", last_token)
    while index < len(tokens):
        if tokens[index].type == TokenType.START_OBJECT:
            if len(stack) >= 2 and stack[-1].type == TokenType.COLON and stack[-2].type == TokenType.KEY:
                stack.append(tokens[index])
                stack.append(".")
            else :
                raise SyntaxError(f'Invalid character {tokens[index].value} at line {tokens[index].line} position {tokens[index].position}')
        if tokens[index].type == TokenType.END_OBJECT:
            if last_token.type == TokenType.COMMA:
                raise SyntaxError(f'Invalid character {tokens[index].value} at line {tokens[index].line} position {tokens[index].position}')

            elif stack and stack[-1] == '.':
                stack.pop()
                stack.pop()
                stack.pop()
                stack.pop()
            elif stack and stack[-1].type == TokenType.START_OBJECT:
                stack.pop()
            else:
                raise SyntaxError(f'Invalid character {tokens[index].value} at line {tokens[index].line} position {tokens[index].position}')
        elif tokens[index].type == TokenType.KEY:
            if stack[-1] == '.' or stack[-1].type == TokenType.START_OBJECT:
                pass
            elif stack[-1].type == TokenType.COMMA:
                stack.pop()
            else:
                raise SyntaxError(f'Invalid character {tokens[index].value} at line {tokens[index].line} position {tokens[index].position}')
            stack.append(tokens[index])
        elif tokens[index].type == TokenType.COLON:
            if stack[-1].type == TokenType.KEY:
                stack.append(tokens[index])
            else:
                raise SyntaxError(f'Invalid character {tokens[index].value} at line {tokens[index].line} position {tokens[index].position}')
        elif tokens[index].type == TokenType.VALUE:
            if len(stack) >= 2 and stack[-1].type == TokenType.COLON and stack[-2].type == TokenType.KEY:
                stack.pop()
                stack.pop()
            else:
                raise SyntaxError(f'Invalid character {tokens[index].value} at line {tokens[index].line} position {tokens[index].position}')
        elif tokens[index].type == TokenType.COMMA:
            if last_token.type != TokenType.VALUE and last_token.type != TokenType.END_OBJECT:
                raise SyntaxError(f'Invalid character {tokens[index].value} at line {tokens[index].line} position {tokens[index].position}')
            stack.append(tokens[index])
        elif tokens[index].type == TokenType.ARRAY_OPEN:
            if stack[-1].type == TokenType.COLON and stack[-2 ].type == TokenType.KEY:
                stack.append(tokens[index])
                stack.append('.')
                last_token = tokens[index]
                index = index+1
                
                while tokens[index].type != TokenType.ARRAY_CLOSE:
                    if tokens[index].type not in [TokenType.VALUE, TokenType.COMMA, TokenType.START_OBJECT, TokenType.END_OBJECT]:
                        raise SyntaxError(f'Invalid character {tokens[index]}')
                    if tokens[index].type == TokenType.START_OBJECT:
                        # end_object_index = tokens.index(next(token for token in tokens if token.type == TokenType.END_OBJECT))
                        # print("EEEEEEEEEEEEEEEEEEnd", end_object_index, index)
                        temp_index = index
                        while tokens[temp_index].type!=TokenType.END_OBJECT:
                            temp_index += 1
                        end_object_index = temp_index
                        validate_syntax(tokens[index: end_object_index+1])
                        index = end_object_index
                    last_token = tokens[index]
                    index = index+1
                
                if tokens[index].type == TokenType.ARRAY_CLOSE and last_token.type in [TokenType.VALUE, TokenType.END_OBJECT, TokenType.ARRAY_OPEN]:
                    stack.pop()
                    stack.pop()
                    stack.pop()
                    stack.pop()
                else:
                    raise SyntaxError(last_token)

            else:
                raise SyntaxError()
        
        # print(index, stack)
        last_token = tokens[index]
        # print("last token", last_token)
        index = index + 1
        

    if len(stack):
        raise SyntaxError(f'Invalid JSON string {stack}')
    # return True


j_string = """
{
  "key": "value",
  "key-n": 101,
  "key-o": {
    "oh":"This seems great"
  },
  "key-l": ["yep", "its", true, "but","is", "this", "?",{"idk":"maybe"}]
}
"""
print(j_string)
tokens = tokenize(j_string)

print(tokens)
parsed_json = parse(tokens)

"""
{
    "glossary": {
        "title": "example glossary",
		"GlossDiv": {
            "title": "S",
			"GlossList": {
                "GlossEntry": {
                    "ID": "SGML",
					"SortAs": "SGML",
					"GlossTerm": "Standard Generalized Markup Language",
					"Acronym": "SGML",
					"Abbrev": "ISO 8879:1986",
					"GlossDef": {
                        "para": "A meta-markup language, used to create markup languages such as DocBook."
                    },
					"GlossSee": "markup"
                }
            }
        }
    }
}
"""