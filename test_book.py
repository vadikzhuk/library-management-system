from uuid import UUID
from class_book import Book


def test_book_initialization_with_id():
    book = Book("Test Title", "Test Author", 2023, book_id="1234")
    assert book.title == "Test Title"
    assert book.author == "Test Author"
    assert book.year == "2023"
    assert book.status is True
    assert book.id == "1234"


def test_book_initialization_without_id():
    book = Book("Another Title", "Another Author", 2022, status=False)
    assert book.title == "Another Title"
    assert book.author == "Another Author"
    assert book.year == "2022"
    assert book.status is False
    assert UUID(book.id)


def test_display_status_in_stock():
    book = Book("Available Book", "Author", 2023, status=True)
    assert book.display_status() == "в наличии"


def test_display_status_checked_out():
    book = Book("Checked Out Book", "Author", 2023, status=False)
    assert book.display_status() == "выдана"


def test_to_dict():
    book = Book("Dict Book", "Dict Author", 2020, status=True, book_id="custom-id")
    book_dict = book.to_dict()
    assert book_dict == {
        'id': "custom-id",
        'title': "Dict Book",
        'author': "Dict Author",
        'year': "2020",
        'status': True
    }


def test_from_dict():
    book_data = {
        'id': "dict-id",
        'title': "From Dict Title",
        'author': "From Dict Author",
        'year': "2021",
        'status': False
    }
    book = Book.from_dict(book_data)
    assert book.id == "dict-id"
    assert book.title == "From Dict Title"
    assert book.author == "From Dict Author"
    assert book.year == "2021"
    assert book.status is False


def test_str_representation():
    book = Book("Str Book", "Str Author", 2019, status=True, book_id="str-id")
    assert str(book) == "ID: str-id; Название: Str Book, Автор: Str Author, Год: 2019 -> в наличии"


def test_str_representation_checked_out():
    book = Book("Str Book 2", "Str Author 2", 2020, status=False, book_id="str-id-2")
    assert str(book) == "ID: str-id-2; Название: Str Book 2, Автор: Str Author 2, Год: 2020 -> выдана"
