"""Unit tests for StringReader class"""

from io import StringIO
from char_reader import StringReader


def test_sanity():
    assert 1 == 1

def test_empty_string():
    """."""
    string_io = StringIO('')
    r = StringReader(string_io)

    assert r.string_io.getvalue() == ''
    assert r.get_next_char() == ''


def test_1_letter():
    """."""
    string_io = StringIO('a')
    r = StringReader(string_io)
    assert r.string_io.getvalue() == 'a'
    assert r.get_next_char() == ''
    assert r.string_io.getvalue() == 'a'
    assert r.get_next_char() == ''

def test_bigger_string():
    """."""
    string_io = StringIO('abcdef')
    r = StringReader(string_io)

    assert r.char == 'a'
    assert r.get_next_char() == 'b'
    assert r.get_next_char() == 'c'
    assert r.get_next_char() == 'd'
    assert r.get_next_char() == 'e'
    assert r.get_next_char() == 'f'
    assert r.get_next_char() == ''
    
def test_string_io():
    """."""
    string_io = StringIO('\'a\'')
    r = StringReader(string_io)

    assert r.char == '\''
    assert r.get_next_char() == 'a'
    assert r.get_next_char() == '\''
    for _ in range(10):
        assert r.get_next_char() == ''

def test_string_io_with_newline_in():
    """."""
    string_io = StringIO('\'a\n\'')
    r = StringReader(string_io)

    assert r.char == '\''
    assert r.get_next_char() == 'a'
    assert r.get_next_char() == '\n'
    assert r.get_next_char() == '\''
    for _ in range(10):
        assert r.get_next_char() == ''

def test_string_io_with_newline_out():
    """."""
    string_io = StringIO('\'a\'\n')
    r = StringReader(string_io)

    assert r.char == '\''
    assert r.get_next_char() == 'a'
    assert r.get_next_char() == '\''
    assert r.get_next_char() == '\n'
    for _ in range(10):
        assert r.get_next_char() == ''


def test_string_io_with_newline_in_and_out():
    """."""
    string_io = StringIO('\'a\n\'\n')
    r = StringReader(string_io)

    assert r.char == '\''
    assert r.get_next_char() == 'a'
    assert r.get_next_char() == '\n'
    assert r.get_next_char() == '\''
    assert r.get_next_char() == '\n'
    for _ in range(10):
        assert r.get_next_char() == ''

def test_get_position_basic():
    """."""
    s = StringIO("")
    r = StringReader(s)

    assert r.get_position() == (1, 1)

def test_get_position_one_normal_char():
    """."""
    s = StringIO("a")
    r = StringReader(s)

    assert r.get_position() == (1, 1)
    r.next_char()
    assert r.get_position() == (1, 2)

def test_get_position_one_newline_char():
    """."""
    s = StringIO("\n")
    r = StringReader(s)

    assert r.get_position() == (1, 1)
    r.next_char()
    assert r.get_position() == (2, 1)

def test_get_position_2_newline_char():
    """."""
    s = StringIO("\n\n")
    r = StringReader(s)

    assert r.get_position() == (1, 1)
    r.next_char()
    assert r.get_position() == (2, 1)
    r.next_char()
    assert r.get_position() == (3, 1)

def test_get_position_newline_inside_apostrophes():
    """."""
    s = StringIO("'\n\n'")
    r = StringReader(s)

    assert r.get_position() == (1, 1)
    r.next_char()
    assert r.get_position() == (1, 2)
    r.next_char()
    assert r.get_position() == (2, 1)
    r.next_char()
    assert r.get_position() == (3, 1)
    r.next_char()
    assert r.get_position() == (3, 2)