"""Unit tests for StringReader class"""

from char_reader import StringReader


def test_sanity():
    assert 1 == 1

def test_empty_string():
    """."""
    string_literal = ''
    r = StringReader(string_literal)

    assert r.idx == 0
    assert r.string_literal == ''

    assert r.get_next_char() is None


def test_1_letter():
    """."""
    string_literal = 'a'
    r = StringReader(string_literal)

    assert r.idx == 0
    assert r.string_literal == 'a'
    assert r.get_next_char() == 'a'
    assert r.idx == 1
    assert r.string_literal == 'a'
    assert r.get_next_char() is None

def test_bigger_string():
    """."""
    string_literal = 'abcdef'
    r = StringReader(string_literal)

    assert r.get_next_char() == 'a'
    assert r.get_next_char() == 'b'
    assert r.get_next_char() == 'c'
    assert r.get_next_char() == 'd'
    assert r.get_next_char() == 'e'
    assert r.get_next_char() == 'f'
    assert r.get_next_char() is None
    
def test_string_literal():
    """."""
    string_literal = '\'a\''
    r = StringReader(string_literal)

    assert r.get_next_char() == '\''
    assert r.get_next_char() == 'a'
    assert r.get_next_char() == '\''
    for _ in range(10):
        assert r.get_next_char() is None

def test_string_literal_with_newline_in():
    """."""
    string_literal = '\'a\n\''
    r = StringReader(string_literal)

    assert r.get_next_char() == '\''
    assert r.get_next_char() == 'a'
    assert r.get_next_char() == '\n'
    assert r.get_next_char() == '\''
    for _ in range(10):
        assert r.get_next_char() is None

def test_string_literal_with_newline_out():
    """."""
    string_literal = '\'a\'\n'
    r = StringReader(string_literal)

    assert r.get_next_char() == '\''
    assert r.get_next_char() == 'a'
    assert r.get_next_char() == '\''
    assert r.get_next_char() == '\n'
    for _ in range(10):
        assert r.get_next_char() is None


def test_string_literal_with_newline_in_and_out():
    """."""
    string_literal = '\'a\n\'\n'
    r = StringReader(string_literal)

    assert r.get_next_char() == '\''
    assert r.get_next_char() == 'a'
    assert r.get_next_char() == '\n'
    assert r.get_next_char() == '\''
    assert r.get_next_char() == '\n'
    for _ in range(10):
        assert r.get_next_char() is None

def test_get_position_basic():
    """."""
    s = ""
    r = StringReader(s)

    assert r.get_position() == (1, 0)

def test_get_position_one_normal_char():
    """."""
    s = "a"
    r = StringReader(s)

    assert r.get_position() == (1, 0)
    r.next_char()
    assert r.get_position() == (1, 1)

def test_get_position_one_newline_char():
    """."""
    s = "\n"
    r = StringReader(s)

    assert r.get_position() == (1, 0)
    r.next_char()
    assert r.get_position() == (2, 0)

def test_get_position_2_newline_char():
    """."""
    s = "\n\n"
    r = StringReader(s)

    assert r.get_position() == (1, 0)
    r.next_char()
    assert r.get_position() == (2, 0)
    r.next_char()
    assert r.get_position() == (3, 0)

def test_get_position_newline_inside_apostrophes():
    """."""
    s = "'\n\n'"
    r = StringReader(s)

    assert r.get_position() == (1, 0)
    r.next_char()
    assert r.get_position() == (1, 1)
    r.next_char()
    assert r.get_position() == (2, 0)
    r.next_char()
    assert r.get_position() == (3, 0)
    r.next_char()
    assert r.get_position() == (3, 1)