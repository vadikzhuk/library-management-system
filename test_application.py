import pytest
import json
from class_book import Book
from class_library import Library
from class_application import Application


@pytest.fixture
def sample_library():
    library = Library()
    library.add_book(Book("Book 1", "Author A", 2001, book_id="id1"))
    library.add_book(Book("Book 2", "Author B", 2002, book_id="id2"))
    return library


@pytest.fixture
def app_with_library(sample_library):
    app = Application()
    app.library = sample_library
    return app


def test_controls():
    app = Application()
    controls = app.controls()
    assert "1 - показать список книг" in controls
    assert "9 - показать список команд" in controls


def test_handle_print_library(app_with_library, capsys):
    app = app_with_library
    app.handle_print_library()
    captured = capsys.readouterr()
    assert "Book 1" in captured.out
    assert "Book 2" in captured.out


def test_handle_print_library_empty(capsys):
    app = Application()
    app.handle_print_library()
    captured = capsys.readouterr()
    assert "Библиотека пуста" in captured.out


def test_handle_add_book(monkeypatch, capsys):
    inputs = iter(["New Book", "Author C", "2023"])
    app = Application()

    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    app.handle_add_book()

    captured = capsys.readouterr()
    assert "Книга New Book добавлена" in captured.out
    assert len(app.library.books) == 1
    assert any(book.title == "New Book" for book in app.library.books.values())


def test_handle_remove_book(app_with_library, monkeypatch, capsys):
    inputs = iter(["id1"])
    app = app_with_library

    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    app.handle_remove_book()

    captured = capsys.readouterr()
    assert "Книга c id" in captured.out
    assert len(app.library.books) == 1
    assert "id1" not in app.library.books


def test_handle_remove_book_invalid_id(app_with_library, monkeypatch, capsys):
    inputs = iter(["invalid_id"])
    app = app_with_library

    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    app.handle_remove_book()

    captured = capsys.readouterr()
    assert "Книги с id invalid_id нет в базе" in captured.out


def test_handle_change_status(app_with_library, monkeypatch, capsys):
    inputs = iter(["id1", "выдана"])
    app = app_with_library

    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    app.handle_change_status()

    captured = capsys.readouterr()
    assert "Статус книги Book 1 изменён на выдана" in captured.out
    assert not app.library.get_book_by_id("id1").status


def test_handle_change_status_invalid_id(app_with_library, monkeypatch, capsys):
    inputs = iter(["invalid_id", "выдана"])
    app = app_with_library

    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    app.handle_change_status()

    captured = capsys.readouterr()
    assert "Книги с id invalid_id нет в базе" in captured.out


def test_handle_change_status_invalid_status(app_with_library, monkeypatch, capsys):
    inputs = iter(["id1", "unknown_status"])
    app = app_with_library

    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    app.handle_change_status()

    captured = capsys.readouterr()
    assert "Неизвестный статус" in captured.out


def test_handle_search(app_with_library, monkeypatch, capsys):
    inputs = iter(["Book 1"])
    app = app_with_library

    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    app.handle_search()

    captured = capsys.readouterr()
    assert "Book 1" in captured.out
    assert "Author A" in captured.out


def test_handle_search_no_results(app_with_library, monkeypatch, capsys):
    inputs = iter(["Nonexistent"])
    app = app_with_library

    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    app.handle_search()

    captured = capsys.readouterr()
    assert "Книг по вашему запросу не найдено" in captured.out


def test_handle_load_from_file(tmp_path, monkeypatch, capsys):
    sample_books = [
        {"id": "id1", "title": "Book 1", "author": "Author A", "year": 2001, "status": True},
        {"id": "id2", "title": "Book 2", "author": "Author B", "year": 2002, "status": False},
    ]
    file_path = tmp_path / "library.json"
    file_path.write_text(json.dumps(sample_books))

    inputs = iter([str(file_path)])
    app = Application()

    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    app.handle_load_from_file()

    captured = capsys.readouterr()
    assert f"Файл библиотеки {file_path} загружен" in captured.out
    assert len(app.library.books) == 2
    assert "Book 1" in str(app.library)
    assert "Book 2" in str(app.library)


def test_handle_load_from_file_invalid_path(monkeypatch, capsys):
    inputs = iter(["invalid_path.json"])
    app = Application()

    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    app.handle_load_from_file()

    captured = capsys.readouterr()
    assert "Неверный путь к файлу" in captured.out


def test_handle_save_to_file(tmp_path, monkeypatch, capsys):
    file_path = tmp_path / "library.json"
    inputs = iter([str(file_path)])
    app = Application()
    app.library.add_book(Book("Book 1", "Author A", 2001, book_id="id1"))

    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    app.handle_save_to_file()

    captured = capsys.readouterr()
    assert f"Библиотека сохранена в {file_path}" in captured.out
    assert file_path.exists()
