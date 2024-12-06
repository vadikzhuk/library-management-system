import pytest
import os
import json
from class_book import Book
from class_library import Library


@pytest.fixture
def sample_books():
    return [
        Book("Book 1", "Author A", 2001, book_id="id1"),
        Book("Book 2", "Author B", 2002, book_id="id2"),
        Book("Book 3", "Author C", 2003, book_id="id3"),
    ]


@pytest.fixture
def library_with_books(sample_books):
    library = Library()
    for book in sample_books:
        library.add_book(book)
    return library


def test_library_initialization():
    library = Library()
    assert len(library.books) == 0
    assert str(library) == "Библиотека пуста"


def test_add_book():
    library = Library()
    book = Book("New Book", "Author", 2023)
    library.add_book(book)
    assert len(library.books) == 1
    assert book.id in library.books


def test_add_book_duplicate_id():
    library = Library()
    book1 = Book("Book 1", "Author 1", 2001, book_id="id1")
    book2 = Book("Book 2", "Author 2", 2002, book_id="id1")
    library.add_book(book1)
    library.add_book(book2)
    assert len(library.books) == 2
    assert book1.id != book2.id


def test_remove_book(library_with_books):
    library = library_with_books
    library.remove_book("id1")
    assert len(library.books) == 2
    assert "id1" not in library.books


def test_get_book_by_id(library_with_books):
    library = library_with_books
    book = library.get_book_by_id("id1")
    assert book is not None
    assert book.title == "Book 1"


def test_get_book_by_invalid_id(library_with_books):
    library = library_with_books
    book = library.get_book_by_id("invalid_id")
    assert book is None


def test_search_book(library_with_books):
    library = library_with_books
    results = library.search_book("Author B")
    assert len(results) == 1
    assert results[0].title == "Book 2"


def test_search_book_no_matches(library_with_books):
    library = library_with_books
    results = library.search_book("Nonexistent Author")
    assert len(results) == 0


def test_change_book_status(library_with_books):
    library = library_with_books
    library.change_book_status("id1", "выдана")
    book = library.get_book_by_id("id1")
    assert book.status is False


def test_change_book_status_invalid_id(library_with_books):
    library = library_with_books
    library.change_book_status("invalid_id", "в наличии")
    # Ensure no changes were made to existing books
    assert all(book.status for book in library.books.values())


def test_dump_to_json(library_with_books, tmp_path):
    library = library_with_books
    file_path = tmp_path / "library.json"
    library.dump_to_json(file_path)
    assert os.path.exists(file_path)
    with open(file_path, "r") as f:
        data = json.load(f)
    assert len(data) == 3
    assert data[0]["title"] == "Book 1"


def test_load_from_json(tmp_path, sample_books):
    file_path = tmp_path / "library.json"
    book_data = [book.to_dict() for book in sample_books]
    with open(file_path, "w") as f:
        json.dump(book_data, f)

    library = Library.load_from_json(file_path)
    assert library is not None
    assert len(library.books) == 3
    assert library.get_book_by_id("id1").title == "Book 1"


def test_load_from_json_file_not_found():
    library = Library.load_from_json("nonexistent.json")
    assert library is None
