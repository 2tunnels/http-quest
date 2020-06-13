import pytest

from http_quest.utils import base64_decode, base64_encode, mask


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


def test_mask_password_is_bigger_than_secret() -> None:
    with pytest.raises(ValueError) as excinfo:
        mask("mark", "jon", "jon")

    assert str(excinfo.value) == "Password and secret should be the same length"


def test_mask_secret_is_bigger_than_password() -> None:
    with pytest.raises(ValueError) as excinfo:
        mask("jon", "mark", "mark")

    assert str(excinfo.value) == "Password and secret should be the same length"


def test_mask() -> None:
    assert mask("mark", "alex", "alex") == "mark"
    assert mask("mark", "alex", "alem") == "mar*"
    assert mask("mark", "alex", "olix") == "*a*k"
    assert mask("mark", "alex", "bill") == "****"
    assert mask("mark", "alex", "billy") == "****"
    assert mask("mark", "alex", "jon") == "****"
