# Library Management System (Console Application)

## Overview

This is a console-based library management system developed as a test project to demonstrate object-oriented programming, error handling, and basic data persistence. The system allows users to manage a collection of books with functionalities to add, remove, search, display, and update the status of books.

All requirements to the application are stated in the task.md file

### Book Details
- **ID**: A unique identifier generated automatically
- **Title**: The title of the book
- **Author**: The author of the book
- **Year**: The year the book was published
- **Status**: Indicates whether the book is "available" or "checked out"

## Features

- **Add Book**: Add a book to the library by providing its title, author, and year
- **Remove Book**: Remove a book from the library using its unique ID
- **Search Book**: Search for books by title, author, or year of publication
- **Display All Books**: View all books currently in the library with their details
- **Update Book Status**: Change the status of a book (e.g., "available" or "checked out")
- **Data Persistence**: Save and load the library data in JSON format
- **Error Handling**: Properly handle invalid inputs and operations on non-existent books

## Project Structure

```
├── main.py               # Entry point for the application
├── class_application.py  # Application class with main logic and user interaction
├── class_library.py      # Library class for managing books
├── class_book.py         # Book class for representing individual books
├── test_application.py   # Pytest tests covering Application class functionality
├── test_library.py       # Pytest tests covering Library class functionality
├── test_book.py          # Pytest tests covering Book class functionality
├── test.json             # Sample database for testing
└── README.md             # Project documentation
```

## How to Run

1. Clone the repository:
```bash
git clone https://github.com/vadikzhuk/library-management-system.git
cd library-management-system
```

2. Ensure you have Python 3.8+ installed on your machine.

3. Run the main.py script:
```bash
python3 main.py
```

4. Follow the on-screen instructions to interact with the library system.

## Example Usage

Launch the application:
```bash
python3 main.py
```

Follow the command menu:
```
1 - показать список книг
2 - загрузить имеющуюся базу данных
3 - сохранить в файл
4 - добавить книгу
5 - удалить книгу
6 - изменить статус книги
7 - поиск книги
8 - выход
9 - показать список команд
```

Add a book:
```
Укажите название: The Catcher in the Rye
Укажите автора: J.D. Salinger
Укажите год издания: 1951
```

Display all books to verify:
```
ID: <generated-id>; Название: The Catcher in the Rye, Автор: J.D. Salinger, Год: 1951 -> в наличии
```

## Sample Data

A sample JSON database `test.json` is included to help you get started. You can load this database by selecting option 2 from the menu and providing the path `test.json`.

## Testing

This project includes a comprehensive suite of tests to ensure the reliability and correctness of its components. The tests are written using the **pytest** framework and are organized into three modules corresponding to the main classes in the project:

1. **`test_book.py`**: Tests the `Book` class, covering:
   - Initialization of book objects with correct attributes.
   - Unique ID generation.
   - Status display and manipulation.
   - Serialization and deserialization of books using dictionaries.

2. **`test_library.py`**: Tests the `Library` class, including:
   - Adding, removing, and retrieving books by ID.
   - Searching for books by title, author, or publication year.
   - Changing the status of books.
   - Loading and saving the library's state to and from JSON files.

3. **`test_application.py`**: Tests the `Application` class, focusing on:
   - The interaction flow of the application.
   - Handling user inputs for adding, removing, and searching for books.
   - Proper management of library operations.

### Running the Tests

To run the tests, make sure you have pytest installed. You can install it using:

```bash
pip install pytest
```

Then, from the project directory use one of the following commands to execute the tests:

- Run all tests in the project:

```bash
pytest
```
- Run a specific test module:

```bash
pytest test_book.py
```

### Test Coverage

The tests ensure that all critical functionalities are thoroughly verified, including edge cases like invalid user inputs, duplicate book IDs, and incorrect file paths. This helps maintain the integrity of the library system and ensures the application behaves as expected.

## Technologies Used

- **Language**: Python 3.8+
- **Persistence**: JSON for saving and loading book data
- **Libraries**: Standard Python libraries (json, os, uuid, typing, pytest)

## Design Approach

- **Object-Oriented Programming**: The system is implemented using three main classes:
  - **Book**: Represents individual book objects
  - **Library**: Manages a collection of books and provides operations like add, remove, search, and update
  - **Application**: Handles user interaction and acts as the entry point

- **Error Handling**: Handles invalid inputs (e.g., non-existent IDs, invalid file paths)
- **Additional Error Handling**: File writing and reading operations additionally wrapped with try-except blocks handling common file errors (Permissions, File Not Found and OS errors, Data serialization errors)
- **Documentation**: Includes detailed docstrings for all classes and methods
- **Type Annotations**: Utilizes type hints for improved readability and debugging

## Future Enhancements

- Implement advanced search filters
- Enhance user interface with colors and formatting for better usability
- Consider importing/exporting data in other formats (CSV)
- Implement Book import from file
- Add logging with levels to track application workflow and more convenient debug

## Licence

As this is just a test exercise purely for demonstration purposes and I don't mind others doing absolutely anything with it I decided to leave this project Unlicenced. For more information see the LICENCE file.

## Author

- **Name**: Vadims Žuks
- **GitHub**: vadikzhuk
