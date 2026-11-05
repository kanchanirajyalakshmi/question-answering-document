from app.utils.text_cleaner import clean_text


def test_clean_text():

    text = "Hello     World\n\n\nPython"

    result = clean_text(text)

    assert result == "Hello World\n\nPython"


def test_empty_text():

    result = clean_text("")

    assert result == ""


def test_null_characters():

    result = clean_text("Hello\x00World")

    assert result == "HelloWorld"