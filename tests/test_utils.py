from http_quest.utils import base64_decode, base64_encode


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
