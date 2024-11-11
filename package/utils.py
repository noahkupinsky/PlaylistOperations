import re
from typing import TypeAlias

Token: TypeAlias = tuple[str, int]

def extract_outermost_brackets_content(s):
    stack = []
    results = []
    start = None

    for i, char in enumerate(s):
        if char == "[":
            if not stack:  # Start of an outermost bracketed section
                start = i + 1  # Start after the opening bracket
            stack.append(i)
        
        elif char == "]":
            if not stack:
                raise ValueError("Unmatched closing bracket at position {}".format(i))
            stack.pop()
            
            if not stack:  # End of an outermost bracketed section
                results.append(s[start:i])  # Capture the substring inside the outermost brackets

    # If stack is not empty after processing, there are unmatched opening brackets
    if stack:
        raise ValueError("Unmatched opening bracket at position {}".format(stack[-1]))

    return results

def lex_operation_tokens(string: str) -> list[Token]:
    # match regex for anything inside square brackets
    square_brackets_content = extract_outermost_brackets_content(string)
    
    if len(square_brackets_content) == 0 or len(square_brackets_content) > 1:
        return []
    
    tokens_block = square_brackets_content[0]
    print(tokens_block)

    # match capital letter and number sequences
    tokens_match = re.match(r"^([A-Z][0-9]+(\s*,?\s*))*$", tokens_block)
    if not tokens_match:
        raise ValueError("Invalid metadata format - invalid token format")
    token_strings = re.findall(r"[A-Z][0-9]+", tokens_block)

    # convert tokens to tuples
    tokens = [(token[0], int(token[1:])) for token in token_strings]
    return tokens