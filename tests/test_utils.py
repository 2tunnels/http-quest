import pytest

from http_quest.utils import base64_decode, base64_encode, get_masked_password


def test_base64_encode() -> None:
    assert base64_encode("foo") == "Zm9v"
    assert base64_encode("bar") == "YmFy"
    assert (
        base64_encode("Beautiful is better than ugly.")
        == "QmVhdXRpZnVsIGlzIGJldHRlciB0aGFuIHVnbHku"
    )


def test_base64_decode() -> None:
    assert base64_decode("Zm9v") == "foo"
    assert base64_decode("YmFy") == "bar"
    assert (
        base64_decode("QmVhdXRpZnVsIGlzIGJldHRlciB0aGFuIHVnbHku")
        == "Beautiful is better than ugly."
    )


def test_get_masked_password_password_is_bigger_than_secret() -> None:
    with pytest.raises(ValueError) as excinfo:
        get_masked_password("mark", "jon", "jon")

    assert str(excinfo.value) == "Password and secret should be the same length"


def test_get_masked_password_secret_is_bigger_than_password() -> None:
    with pytest.raises(ValueError) as excinfo:
        get_masked_password("jon", "mark", "mark")

    assert str(excinfo.value) == "Password and secret should be the same length"


def test_get_masked_password() -> None:
    assert get_masked_password("mark", "alex", "alex") == "mark"
    assert get_masked_password("mark", "alex", "alem") == "mar*"
    assert get_masked_password("mark", "alex", "olix") == "*a*k"
    assert get_masked_password("mark", "alex", "bill") == "****"
    assert get_masked_password("mark", "alex", "billy") == "****"
    assert get_masked_password("mark", "alex", "jon") == "****"
