# Capstone V - Database - Submitted by Bhavya Patteeswaran
import sqlite3
from tabulate import tabulate


class Book:
    def __init__(self, book_id, title, author, qty):
        self.Id = book_id
        self.Title = title
        self.Author = author
        self.Qty = qty

    def add_to_db(self):
        """
        Returns: Tuple needed to add to database
        """
        return (self.Id, self.Title, self.Author, self.Qty)


# ==========Functions outside the class==============
def print_table():
    """
    This function is used to print the list of books in the books table
    Returns:
    Display the output of [SELECT statement - display all rows from the books table]
    """
    results = []
    for book in cursor.execute("SELECT * FROM books"):
        results.append(book)
    print(tabulate(results, headers=["ID", "Title", "Author", "Qty"], tablefmt="sql"))


def add_book():
    """
    This function is used to add book in the database.
    1. Input the values from user.
    2. Creating new_book object and adding it to the database.
    Returns: The new book details are added in the database and committed successfully.
    """
    while True:
        try:
            int_id = int(input("Enter id: "))
            qty = int(input("Enter qty: "))
            break
        except ValueError:
            print("Enter only integer value!")
    title = input("Title: ")
    author = input("Author: ")

    # Creating new book object and adding it to the database
    new_book = Book(int_id, title, author, qty)
    cursor.execute("INSERT INTO books VALUES (?,?,?,?)", new_book.add_to_db())
    db.commit()
    print("The new book details are added to the database.")
    print_table()


def update_info():
    """
    Update the information in the books table.
    1. Handle the user input logic.
    2. Calling the function - find_what_to_use() -> returns int value from 1 to 4 which specifies the column name
    in the table books.
    3. Using the column number has key, find the value in the dictionary.
    4. Logic for user input getting new and old values to replace
    5. Update in the database relevant to the user's choices.
    Returns: Update the database and commit.
    """
    print("What do you want to update in the books detail?")
    val = find_what_to_use()
    print(f"What is the {DICT_OF_OPERATIONS[val]} you want to change to")

    while True:
        old_value = input("Old value: ")
        new_value = input("New Value: ")
        if val == 1 or val == 4:
            try:
                new_value = int(new_value)
                old_value = int(old_value)
                break
            except ValueError:
                print("Invalid value")
        else:
            break

    if val == 1:
        cursor.execute("UPDATE books SET Id = ? WHERE Id = ?", (new_value, old_value))
    if val == 2:
        cursor.execute("UPDATE books SET Title = ? WHERE Title = ?", (new_value, old_value))
    if val == 3:
        cursor.execute("UPDATE books SET Author = ? WHERE Author = ?", (new_value, old_value))
    if val == 4:
        cursor.execute("UPDATE books SET Qty = ? WHERE Qty = ?", (new_value, old_value))
    db.commit()
    print("The records are updated successfully. Please find the update in below table:")
    print_table()


def delete_book():
    """
    Deletes the book according to the id of the book.
    1. Logic to handle user input.
    2. Execute delete sql statement using ID.
    Returns: Delete the record using ID and commit the database.
    """
    while True:
        try:
            id_of_book = int(input("Enter id of book you want to delete: "))
            break
        except ValueError:
            print("Enter a valid id - only integer")

    cursor.execute("DELETE FROM books WHERE Id = ?", (id_of_book,))
    db.commit()
    if cursor.rowcount == 0:
        print("The records are not found.", cursor.rowcount, "record(s) deleted")
    else:
        print(cursor.rowcount, "record(s) deleted")


def search_book():
    """
    Searching for a book.
    1. Handle the user input logic.
    2. Calling the function - find_what_to_use() -> returns int value from 1 to 4 which specifies the column name
    in the table books.
    3. Using the column number has key, find the value in the dictionary.
    Above three steps are same logic used in the update function.
    4. User input to get what they are searching for. If the search on id or quantity then
    convert the value to integer.
    5. Search the value using if statement and display the search result.
    Returns: Display the search result in the console.
    """
    print("What do you want to search by?")
    val = find_what_to_use()
    print(f"What is the {DICT_OF_OPERATIONS[val]} you want to find?")

    while True:
        try:
            search_val = input("Enter search: ")
            if val == 1 or val == 4:
                search_val = int(search_val)
            break
        except ValueError:
            print("Enter a valid search value")

    book_found = False
    if val == 1:
        for i in cursor.execute("SELECT * FROM books WHERE Id = ?", (search_val,)):
            print("Your book")
            print(f"--{i}--")
            book_found = True

    elif val == 2:
        for i in cursor.execute("SELECT * FROM books WHERE Title = ?", (search_val,)):
            print("Your book")
            print(f"--{i}--")
            book_found = True

    elif val == 3:
        for i in cursor.execute("SELECT * FROM books WHERE Author = ?", (search_val,)):
            print("Your book")
            print(f"--{i}--")
            book_found = True

    elif val == 4:
        for i in cursor.execute("SELECT * FROM books WHERE Qty = ?", (search_val,)):
            print("Your book")
            print(f"--{i}--")
            book_found = True

    if not book_found:
        print("--There isn't a book matching the search--")


def find_what_to_use():
    """
    Duplicate code used in search and update_info
    1. Handle the input from user on which column they want to update or search.
    Display the column, 1.ID 2.Title 3.Author 4.Qty
    Returns: Int
    The value from 1 to 4 - value specifies which column they want to update or search.
    """
    print("1. ID\n2. Title\n3. Author\n4. Qty")
    while True:
        try:
            val = int(input(": "))
            if val in range(1, 5):
                break
            else:
                print("Enter a value from 1 to 4")
        except ValueError:
            print("Enter a value from 1 to 4")
    return val


def main():
    """
    1. It will print the table initially.
    2. Display the options for user input.
    3. According to the user input, the corresponding functions are called to execute.
    4. Function will execute in loop until the user input 0-Exit to break the loop.
    Returns: Execute the specified functions and display the result.
    """
    print_table()

    is_running = True
    while is_running:
        # Displaying the user options
        print("\nSelect one of the following options")
        print("1. Enter book\n2. Update book\n3. Delete book\n4. Search book\n5. View all books\n0. Exit")
        # Logic for user input
        while True:
            try:
                user_choice = int(input("Enter: "))
                if 0 <= user_choice < 6:
                    break
                print("Enter a valid choice 1 to 5")
            except ValueError:
                print("Enter a valid choice 1 to 5")

        if user_choice == 1:
            add_book()
        elif user_choice == 2:
            update_info()
        elif user_choice == 3:
            delete_book()
        elif user_choice == 4:
            search_book()
        elif user_choice == 5:
            print_table()
        elif user_choice == 0:
            is_running = False


if __name__ == '__main__':
    # Setting constant dictionary for reference
    DICT_OF_OPERATIONS = {1: "Id", 2: "Title", 3: "Author", 4: "Qty"}

    try:
        db = sqlite3.connect("ebookstore.db")
        cursor = db.cursor()

        # Create the table books and commit the db
        cursor.execute('''
    CREATE TABLE IF NOT EXISTS books 
    (
    Id INTEGER PRIMARY KEY, 
    Title TEXT, 
    Author TEXT, 
    Qty INTEGER
    )
    ''')
        db.commit()
        print('Created the books table successfully!')

        # This is what is initially added when database is created.
        book_1 = Book(3001, "A Tale of Two Cities", "Charles Dickens", 30)
        book_2 = Book(3002, "Harry Potter and the Philosopher's Stone", "J.K Rowling", 40)
        book_3 = Book(3003, "The Lion, the Witch and the Wardrobe", "C.S Lewis", 25)
        book_4 = Book(3004, "The Lord of the Rings", "J.R.R Tolkien", 37)
        book_5 = Book(3005, "Alice in Wonderland", "Lewis Carroll", 12)

        # List of book objects
        books = [
            book_1.add_to_db(),
            book_2.add_to_db(),
            book_3.add_to_db(),
            book_4.add_to_db(),
            book_5.add_to_db()
        ]
        # Insert the records in the database and commit the db
        cursor.executemany("INSERT INTO books VALUES (?,?,?,?)", books)
        db.commit()
        print('Inserted 5 initial records in books table successfully!')
        # cursor.execute("SELECT * FROM books")
        # records = cursor.fetchall()
        # print(tabulate(records, headers=["ID", "Title", "Author", "Qty"], tablefmt="sql"))

        main()

    except Exception as e:
        # Roll back any change if something goes wrong
        db.rollback()
        raise e

    finally:
        # Drop the books table
        cursor.execute('''DROP TABLE books''')
        db.commit()
        print("\nDrop the table books to re-execute the code without error")
        db.close()
        print("DB Connection is closed")
        print("GoodBye!!!")
