import json
from class_book import Book
import os
from typing import Optional


class Library:
    """
    A class representing a library that manages a collection of books.
    Provides methods to add, remove, search, and manipulate books, as well as
    loads/reads the library's state to/from JSON files.
    """

    def __init__(self):
        """
        Initializes the Library instance with an empty collection of books.
        """
        self.books = {}

    def __str__(self) -> str:
        """
        Returns a string representation of the library.
        """
        if not self.books:
            return "Библиотека пуста"
        return '\n'.join(str(book) for book in self.books.values())

    @classmethod
    def load_from_json(cls, filename: str):
        """
        Loads a library from a JSON file.

        Args:
            filename (str): Path to the JSON file containing serialized book data.

        Returns:
            Library or None: A Library instance populated with books from the file,
            or None if the file does not exist.
        """
        try:
            # Check if file exists
            if not os.path.exists(filename):
                print(f"File {filename} does not exist.")
                return None

            # Create a new library instance
            existing_library = cls()

            # Attempt to open and parse the file
            with open(filename, 'r') as f:
                book_data = json.load(f)

            # Validate that json.load returned a list
            if not isinstance(book_data, list):
                print(f"Invalid JSON format in {filename}. Expected a list of books.")
                return None

            # Add books, with additional error handling for individual book parsing
            for book in book_data:
                try:
                    existing_library.add_book(Book.from_dict(book))
                except Exception as book_error:
                    print(f"Error parsing book: {book_error}")

            return existing_library

        except FileNotFoundError:
            print(f"File {filename} not found.")
            return None
        except json.JSONDecodeError as e:
            print(f"Invalid JSON in {filename}: {e}")
            return None
        except PermissionError:
            print(f"Permission denied when trying to read {filename}.")
            return None
        except Exception as e:
            print(f"Unexpected error loading library from {filename}: {e}")
            return None

    def dump_to_json(self, path_to_database: str):
        """
        Saves the current state of the library to a JSON file.

        Args:
            path_to_database (str): Path to the file where the library data will be saved.
        """
        try:
            # Prepare the book data
            book_data = [book.to_dict() for book in self.books.values()]

            # Get absolute path to the file
            absolute_path_to_database = os.path.abspath(path_to_database)

            # Ensure the directory exists
            os.makedirs(os.path.dirname(absolute_path_to_database), exist_ok=True)

            # Write to file with error handling
            with open(path_to_database, 'w') as f:
                json.dump(book_data, f, indent=4)

        except PermissionError:
            print(f"Error: No permission to write to {path_to_database}")
        except OSError as e:
            print(f"OS error occurred while saving library: {e}")
        except TypeError as e:
            print(f"Error serializing library data: {e}")
        except Exception as e:
            print(f"Unexpected error saving library to {path_to_database}: {e}")

    def add_book(self, book: Book):
        """
        Adds a book to the library. If a book with the same ID exists, regenerates a new ID.

        Args:
            book (Book): The book instance to add to the library.
        """
        # Check if ID already exists
        if book.id in self.books:
            # If ID exists, regenerate, however the possibility is very low
            book.id = book._generate_id()
        self.books[book.id] = book

    def remove_book(self, book_id: str):
        """
        Removes a book from the library by its ID.

        Args:
            book_id (str): The ID of the book to remove.
        """
        if book_id in self.books:
            # If a book exists remove it from a library
            del self.books[book_id]

    def get_book_by_id(self, book_id: str) -> Optional[Book]:
        """
        Retrieves a book from the library by its ID.

        Args:
            book_id (str): The ID of the book to retrieve.

        Returns:
            Book or None: The book instance if found, otherwise None.
        """
        return self.books.get(book_id)

    def search_book(self, prompt: str) -> list[Book]:
        """
        Searches for books in the library that match the provided query.
        Matches are determined by title, author, or publication year.

        Args:
            prompt (str): The search query (case insensitive).

        Returns:
            list[Book]: A list of books that match the query, or an empty list if no matches are found.
        """
        # Converting prompt to all lower case
        prompt = prompt.lower()
        # Creating an empty list to store search results
        results = []

        for book in self.books.values():
            if (prompt in book.title.lower() or
                    prompt in book.author.lower() or
                    prompt in str(book.year).lower()):
                results.append(book)

        return results

    def change_book_status(self, id: str, status: str):
        """
        Changes the status of a book in the library to either 'available' or 'checked out'.

        Args:
            id (str): The ID of the book whose status is to be updated.
            status (str): The new status of the book ("в наличии" for available, "выдана" for checked out).
        """
        if id in self.books:
            # Getting a book by ID
            book = self.get_book_by_id(id)
            match status.lower():
                case "в наличии":
                    book.status = True
                case "выдана":
                    book.status = False
