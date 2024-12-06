import uuid
from typing import Optional


class Book:
    """
    A class representing a book in a library system.
    Each book has a title, author, year of publication, availability status, and a unique ID.
    """

    def __init__(self, title: str, author: str, year: str | int,
                 status: Optional[bool] = True, book_id: Optional[str] = None):
        """
        Initializes a new Book instance with the given details.

        Args:
            title (str): The title of the book.
            author (str): The author of the book.
            year (str | int): The year the book was published.
            status (Optional[bool], optional): The availability status of the book.
                                               Defaults to True (в наличии).
            book_id (Optional[str], optional): The unique ID of the book. If not provided, a new UUID is generated.
        """
        self.title = title
        self.author = author
        self.year = str(year)

        if not status:
            self.status = status
        else:
            self.status = True

        if not book_id:
            self.id = self._generate_id()
        else:
            self.id = book_id

    def __str__(self) -> str:
        """
        Returns a string representation of the book with its details and status.

        Returns:
            str: A formatted string containing the book's ID, title, author, year, and status.
        """
        return f"ID: {self.id}; Название: {self.title}, Автор: {self.author}, Год: {self.year} -> {self.display_status()}"

    def _generate_id(self) -> str:
        """
        Generates a unique identifier for the book using UUID.

        Returns:
            str: A unique string identifier.
        """
        return str(uuid.uuid4())

    def display_status(self) -> str:
        """
        Displays the current availability status of the book.

        Returns:
            str: "в наличии" if the book is available, otherwise "выдана".
        """
        if self.status:
            return "в наличии"
        return "выдана"

    def to_dict(self) -> dict:
        """
        Converts the book's data into a dictionary format for serialization.

        Returns:
            dict: A dictionary containing the book's ID, title, author, year, and status.
        """
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'status': self.status
        }

    @classmethod
    def from_dict(cls, book_data: dict):
        """
        Creates a Book instance from a dictionary of book data.

        Args:
            book_data (dict): A dictionary containing the book's details.

        Returns:
            Book: A new Book instance initialized with the provided data.
        """
        return cls(
            title=book_data['title'],
            author=book_data['author'],
            year=book_data['year'],
            status=book_data['status'],
            book_id=book_data['id']
        )
