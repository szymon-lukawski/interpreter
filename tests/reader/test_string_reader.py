"""Unit tests for TextIOReader class"""

from io import StringIO
import pytest

from lexer.char_reader import TextIOReader


def test_sanity():
    """."""
    assert 1 == 1


def test_empty_string():
    """Empty input always returns empty string"""
    text_io = StringIO("")
    r = TextIOReader(text_io)
    assert r.get_next_char() == ""
    assert r.get_next_char() == ""
    assert r.get_next_char() == ""
    assert r.get_next_char() == ""
    assert r.get_next_char() == ""


def test_pos_empty_string():
    """Position of empty input does not change even after invoking  next_char() multiple times and it is (1, 1)"""
    text_io = StringIO("")
    r = TextIOReader(text_io)
    assert r.get_position() == (1, 1)
    r.next_char()
    assert r.get_position() == (1, 1)
    r.next_char()
    assert r.get_position() == (1, 1)
    r.next_char()
    assert r.get_position() == (1, 1)


different_chars = list(
    "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-_=+/?,.<>|'\"\\\n\t`~§"
)


@pytest.mark.parametrize("char", different_chars)
def test_pos_of_first_letter(char: str):
    """Position of the first letter is always (1, 1). No matter whether it is a newline, tab, backslash or other char"""

    text_io = StringIO(char)
    r = TextIOReader(text_io)
    assert r.get_position() == (1, 1)
    assert r.get_curr_char() == char
    assert r.get_position() == (1, 1)
    assert r.get_next_char() == ""
    assert r.get_next_char() == ""


def test_few_letters():
    """abcdef"""
    text_io = StringIO("abcdef")
    r = TextIOReader(text_io)

    assert r.get_curr_char() == "a"
    assert r.get_next_char() == "b"
    assert r.get_next_char() == "c"
    assert r.get_next_char() == "d"
    assert r.get_next_char() == "e"
    assert r.get_next_char() == "f"
    assert r.get_next_char() == ""


def test_string_literal():
    """'a'"""
    text_io = StringIO("'a'")
    r = TextIOReader(text_io)

    assert r.get_curr_char() == "'"
    assert r.get_next_char() == "a"
    assert r.get_next_char() == "'"
    for _ in range(10):
        assert r.get_next_char() == ""


def test_position_one_newline_char():
    """\n - newline increments the row coordiante of the next char"""
    s = StringIO("\n")
    r = TextIOReader(s)

    assert r.get_position() == (1, 1)
    r.next_char()
    assert r.get_position() == (2, 1)


def test_position_2_newline_char():
    """\n\n - every newline increments the row coordiante of the next char"""
    s = StringIO("\n\n")
    r = TextIOReader(s)

    assert r.get_position() == (1, 1)
    r.next_char()
    assert r.get_position() == (2, 1)
    r.next_char()
    assert r.get_position() == (3, 1)


def test_position_is_not_affected_by_apostrophes():
    """'\n\n'"""
    s = StringIO("'\n\n'")
    r = TextIOReader(s)

    assert r.get_position() == (1, 1)
    r.next_char()
    assert r.get_position() == (1, 2)
    r.next_char()
    assert r.get_position() == (2, 1)
    r.next_char()
    assert r.get_position() == (3, 1)
    r.next_char()
    assert r.get_position() == (3, 2)




def test_newline_affects_the_new_character():
    """'a\n'\n"""
    text_io = StringIO("'a\n'\n")
    r = TextIOReader(text_io)

    assert r.get_curr_char() == "'"
    assert r.get_position() == (1, 1)
    assert r.get_next_char() == "a"
    assert r.get_position() == (1, 2)
    assert r.get_next_char() == "\n"
    assert r.get_position() == (1, 3)
    assert r.get_next_char() == "'"
    assert r.get_position() == (2, 1)
    assert r.get_next_char() == "\n"
    assert r.get_position() == (2, 2)
    for _ in range(10):
        assert r.get_next_char() == ""
        assert r.get_position() == (3, 1)


def test_get_position_return_a_copy():
    """Ala"""
    text_io = StringIO("Ala")
    r = TextIOReader(text_io)

    assert r.get_curr_char() == "A"
    row, col = r.get_position()
    assert (row, col) == (1, 1)
    row += 10
    col += 7
    assert (row, col) == (11, 8)
    assert r.get_position() == (1, 1)

def test_get_curr_char_does_not_affect_position():
    """Ala"""
    text_io = StringIO("Ala")
    r = TextIOReader(text_io)

    assert r.get_curr_char() == "A"
    assert r.get_position() == (1, 1)
    assert r.get_curr_char() == "A"
    assert r.get_position() == (1, 1)
    assert r.get_curr_char() == "A"
    assert r.get_position() == (1, 1)


def test_get_curr_char_changing_using_referance_does_not_affect_reader():
    """Ala"""
    text_io = StringIO("Ala")
    r = TextIOReader(text_io)

    curr_char = r.get_curr_char()
    curr_char = 'C'
    assert r.get_curr_char() == 'A'

def test_next_char_returns_none_but_advances_in_stream():
    """'a\n'\n"""
    text_io = StringIO("'a\n'\n")
    r = TextIOReader(text_io)

    assert r.get_curr_char() == "'"
    assert r.get_position() == (1, 1)
    assert r.next_char() is None
    assert r.get_position() == (1, 2)
    assert r.next_char() is None
    assert r.get_position() == (1, 3)
    assert r.next_char() is None
    assert r.get_position() == (2, 1)
    assert r.next_char() is None
    assert r.get_position() == (2, 2)
    for _ in range(10):
        assert r.next_char() is None
        assert r.get_position() == (3, 1)



    