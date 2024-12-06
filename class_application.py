import os.path
from class_library import Library
from class_book import Book


class Application:
    """
    Application class that serves as a command-line interface for managing a library system.
    It provides methods to view, load, save, add, remove, and modify books in a library.
    """

    def __init__(self):
        """
        Initializes the Application instance with a new Library object.
        """
        self.library = Library()

    def main_cycle(self):
        """
        Starts the main interaction loop for the application.
        Displays a menu of commands and processes user input to perform various library management actions.
        """
        print("Добро пожаловать в систему управления библиотекой! Вот список доступных команд:")
        print(self.controls())
        while True:
            command = input("Выберите действие (9 - показать список команд): ")
            match command:
                case "1":
                    self.handle_print_library()
                case "2":
                    self.handle_load_from_file()
                case "3":
                    self.handle_save_to_file()
                case "4":
                    self.handle_add_book()
                case "5":
                    self.handle_remove_book()
                case "6":
                    self.handle_change_status()
                case "7":
                    self.handle_search()
                case "8":
                    del self
                    break
                case "9":
                    print(self.controls())
                case _:
                    print("Код команды неверный, пожалуйста введите число от 1 до 9")

    def controls(self):
        """
        Returns a string representation of available commands in the application.
        """
        return """1 - показать список книг
2 - загрузить имеющуюся базу данных
3 - сохранить в файл
4 - добавить книгу
5 - удалить книгу
6 - изменить статус книги
7 - поиск книги
8 - выход
9 - показать список команд"""

    def handle_print_library(self):
        """
        Prints the current list of books in the library.
        """
        print(self.library)

    def handle_load_from_file(self):
        """
        Loads the library data from a JSON file provided by the user.
        Prompts the user for the file path and validates its existence before loading.
        """
        db_path = input("Укажите путь к имеющемуся файлу библиотеки .json: ")
        if os.path.exists(db_path):
            self.library = Library.load_from_json(db_path)
            print(f"Файл библиотеки {db_path} загружен")
        else:
            print("Неверный путь к файлу")

    def handle_save_to_file(self):
        """
        Saves the current library data to a JSON file.
        Prompts the user for the file name and confirms overwriting if the file already exists.
        """
        db_path = input("Укажите имя файла: ")
        if os.path.exists(db_path):
            rewrite = input("Файл уже существует. Перезаписать? (любой ответ кроме да == нет)")
            if rewrite.lower() == "да":
                self.library.dump_to_json(db_path)
                print(f"Библиотека сохранена в {os.path.abspath(db_path)}")
        else:
            self.library.dump_to_json(db_path)
            print(f"Библиотека сохранена в {os.path.abspath(db_path)}")

    def handle_add_book(self):
        """
        Adds a new book to the library.
        Prompts the user for the book's title, author, and year of publication.
        """
        print("Добавляем новую книгу")
        title = input("Укажите название: ")
        author = input("Укажите автора: ")
        year = input("Укажите год издания: ")
        new_book = Book(title, author, year)
        self.library.add_book(new_book)
        print(f"Книга {title} добавлена в библиотеку под id {new_book.id}")

    def handle_remove_book(self):
        """
        Removes a book from the library by its ID.
        Prompts the user for the book ID and validates its existence before removal.
        """
        removed_book_id = input("Укажите id книги, которую хотите удалить: ")
        # Trying to get a book by ID, if ID doesn't exist we got None
        remove_book = self.library.get_book_by_id(removed_book_id)
        if remove_book:
            self.library.remove_book(removed_book_id)
            print(f"Книга c id {remove_book} удалена")
        else:
            print(f"Книги с id {removed_book_id} нет в базе")

    def handle_change_status(self):
        """
        Changes the status of a book in the library.
        Prompts the user for the book ID and the new status, and updates the status if valid.
        """
        change_book_id = input("Укажите id книги у которой хотите поменять статус: ")
        # Trying to get a book by ID, if ID doesn't exist we got None
        change_book = self.library.get_book_by_id(change_book_id)
        if not change_book:
            print(f"Книги с id {change_book_id} нет в базе")
            return
        new_status = input("Задайте новый статус (в наличии/выдана): ")
        if new_status.lower() not in ["в наличии", "выдана"]:
            print("Неизвестный статус, возможные значения: в наличии, выдана")
            return
        self.library.change_book_status(change_book_id, new_status)
        print(f"Статус книги {change_book.title} изменён на {new_status.lower()}")

    def handle_search(self):
        """
        Searches for books in the library based on a user-provided query.
        Prompts the user for a search term and displays matching books.
        """
        prompt = input("Введите поисковый запрос (название/автор/год): ")
        result_list = self.library.search_book(prompt)
        if result_list:
            for book in result_list:
                print(book)
        else:
            print("Книг по вашему запросу не найдено")
