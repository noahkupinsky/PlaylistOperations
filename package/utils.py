import re
from typing import TypeAlias

Token: TypeAlias = tuple[str, int]

def lex_operation_tokens(string: str) -> list[Token]:
    # match regex for anything inside square brackets
    square_brackets_content = re.findall(r"\[(.*)\]", string)
    if len(square_brackets_content) == 0:
        return []
    elif len(square_brackets_content) > 1:
        raise ValueError("Invalid metadata format - too many square brackets")
    
    tokens_block = square_brackets_content[0]

    # match capital letter and number sequences
    tokens_match = re.match(r"^([A-Z][0-9]+(\s*,?\s*))*$", tokens_block)
    if not tokens_match:
        raise ValueError("Invalid metadata format - invalid token format")
    token_strings = re.findall(r"[A-Z][0-9]+", tokens_block)

    # convert tokens to tuples
    tokens = [(token[0], int(token[1:])) for token in token_strings]
    return tokens