from AkvoFormPrint.utils import parse_int


def test_parse_int_with_valid_integer():
    assert parse_int("123") == 123


def test_parse_int_with_valid_float():
    assert parse_int("123.45") == 123


def test_parse_int_with_invalid_string():
    assert parse_int("abc", 0) == 0


def test_parse_int_with_none():
    assert parse_int(None, -1) == -1


def test_parse_int_with_empty_string():
    assert parse_int("", 100) == 100


def test_parse_int_without_default():
    assert parse_int("abc") is None
