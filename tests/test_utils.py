import pytest
from package.utils import lex_operation_tokens

def test_get_operation_tokens():
    # no square brackets should return no tokens
    assert lex_operation_tokens("test") == []
    # multiple square brackets should return no tokens
    assert lex_operation_tokens("test [A0] [B1]") == []
    # empty square brackets should return no tokens
    assert lex_operation_tokens("test []") == []
    # valid square brackets with one token should return the token
    assert lex_operation_tokens("test [A0]") == [("A", 0)]
    # brackets with multiple tokens should return them
    assert lex_operation_tokens("test [A0B1]") == [("A", 0), ("B", 1)]
    # commas and whitespace should be ignored
    assert lex_operation_tokens("test [A0, B1]") == [("A", 0), ("B", 1)]
    assert lex_operation_tokens("test [A0,B1]") == [("A", 0), ("B", 1)]
    assert lex_operation_tokens("test [A0 ,B1]") == [("A", 0), ("B", 1)]
    assert lex_operation_tokens("test [A0 ,  B1]") == [("A", 0), ("B", 1)]
    # numbers should be able to be multiple digits
    assert lex_operation_tokens("test [A0B1C12]") == [("A", 0), ("B", 1), ("C", 12)]
    # invalid tokens should raise ValueError
    with pytest.raises(ValueError):
        lex_operation_tokens("test [A0B1C]")
    with pytest.raises(ValueError):
        lex_operation_tokens("test [A0B[1C1]")