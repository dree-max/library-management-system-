# Library Management System - Project Documentation

## 📘 Overview

The Library Management System is a Python + MySQL-based application designed to manage books, members, and transactions (book issuance and returns) within a library environment. This system provides functionalities to:

* Add new books and members
* Issue books to members
* Return books and calculate fines
* Display transactions with joined book and member details
* Apply rules (e.g., late returns, discounts, pricing updates)

---

## 🏗️ Database Design

### Tables:

#### 1. `books`

```sql
CREATE TABLE books (
  ID INT NOT NULL AUTO_INCREMENT,
  Title VARCHAR(100),
  Author VARCHAR(100),
  Genre VARCHAR(50),
  PublishedYear INT,
  Price DECIMAL(10,2),
  PRIMARY KEY (ID)
);
```

#### 2. `members`

```sql
CREATE TABLE members (
  ID INT NOT NULL AUTO_INCREMENT,
  FirstName VARCHAR(50) NOT NULL,
  LastName VARCHAR(50) NOT NULL,
  Email VARCHAR(50) UNIQUE,
  Phone VARCHAR(10),
  PRIMARY KEY (ID)
);
```

#### 3. `transactions`

```sql
CREATE TABLE transactions (
  ID INT NOT NULL AUTO_INCREMENT,
  BookID INT,
  MemberID INT,
  IssueDate DATE,
  ReturnDate DATE,
  PRIMARY KEY (ID),
  FOREIGN KEY (BookID) REFERENCES books(ID),
  FOREIGN KEY (MemberID) REFERENCES members(ID)
);
```

---

## ⚙️ Python Functionalities

### 1. Database Connection

Establishes connection with the MySQL server.

```python
import mysql.connector
from mysql.connector import Error
from datetime import datetime

#connect to the database
def connect ():
    return mysql.connector.connect(
    host ="localhost",
    user ="root",
    password ="your-passowrd"
)

myDB = connect()
```

---

### 2. Add a Book

```python
#add_book function

def add_book():
    myDB = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your-password",
        database="library_management_system"
    )
    cursor = myDB.cursor()

    #Accept input or use hardcoded values
    title = input("Enter book title: ")
    Author = input("Enter author name: ")
    Genre = input("Enter genre")
    Year = input("Enter Published Year: ")
    Price = input("Enter price: ")

    try:
        query = "INSERT INTO books (title, Author, Genre, PublishedYear, Price) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (title, Author, Genre, Year, Price))
        myDB.commit()
        print("✅ Book added successfully.")
    except Exception as e:
        print("❌ Error adding book:", e)
    finally:
        myDB.close()

#Show All books
def show_books():
    myDB = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your-password"
        database="library_management_system"

    )   
    cursor = myDB.cursor()
    cursor.execute("SELECT * FROM books")

    result = cursor.fetchall()

    print("📚 Books in database:")  
    for row in result:
        print(row)
    myDB.close()           

#use the functions
#add_book()
#show_books()

```

### 3. Add a Member

```python
#ADD NEW MEMBER

def add_member():
    myDB = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your-password",
        database="library_management_system"
    )

    FirstName = input("Enter your First Name:")
    LastName  = input("Enter Last Name:")
    Email     = input("Enter your email address:")
    Phone     = input("Enter your Phone number:")


    cursor = myDB.cursor()
    query = "INSERT INTO members (FirstName, LastName, Email, Phone) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (FirstName, LastName, Email, Phone))
    
    print("✅ new member added.")

    myDB.close()

#add_member()
```

### 4. Issue a Book

```python
# Issue a book with user input and validation
def issue_book(bookID=None, memberID=None):
    myDB = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your-password",
        database="library_management_system"
    )
    if myDB is None:
        return

    try:
        cursor = myDB.cursor()

        # Prompt for input
        #book_id = int(input("Enter Book ID to issue: "))
        #member_id = int(input("Enter Member ID: "))
        if bookID is None:
            bookID = int(input("Enter Book ID to issue: "))
            
        if memberID is None:
            memberID = int(input("Enter Member ID: "))

        # Check if book exists
        cursor.execute("SELECT title FROM books WHERE ID = %s", (bookID,))
        book = cursor.fetchone()
        if not book:
            print("❌ Book ID not found.")
            return

        # Check if member exists
        cursor.execute("SELECT name FROM members WHERE ID = %s", (memberID,))
        member = cursor.fetchone()
        if not member:
            print("❌ Member ID not found.")
            return

        # Check if the book is already issued and not returned
        cursor.execute("""
            SELECT *
            FROM transactions
            WHERE BookID = %s AND ReturnDate IS NULL
        """, (bookID,))
        already_issued = cursor.fetchone()
        if already_issued:
            print("⚠️ This book is currently issued and hasn't been returned.")
            return

        # Issue the book
        cursor.execute("""
            INSERT INTO transactions (BookID, MemberID, IssueDate)
            VALUES (%s, %s, CURDATE())
        """, (bookID, memberID))
        myDB.commit()

        print(f"📚 Book '{book[0]}' successfully issued to {member[0]}.")
    except ValueError:
        print("❌ Invalid input. Please enter numeric IDs.")
    except Error as e:
        print(f"❌ Database error: {e}")
    finally:
        myDB.commit()

```

### 5. Return a Book + Fine Calculation

```python
# Return a book and calculate fine
def return_book(transactionID):
    myDB = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your-password",
        database="library_management_system"
    )
    if myDB is None:
        return
    try:
        cursor = myDB.cursor()
        cursor.execute("UPDATE transactions SET ReturnDate = CURDATE() WHERE ID = %s", (transactionID,))
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN DATEDIFF(ReturnDate, IssueDate) > 14 THEN (DATEDIFF(ReturnDate, IssueDate) - 14) * 5
                    ELSE 0
                END AS fine
            FROM transactions
            WHERE ID = %s
        """, (transactionID,))
        fine = cursor.fetchone()[0]
        print(f"✅ Book returned. Fine: ₹{fine}")
        myDB.commit()
    except Error as e:
        print(f"❌ Error returning book: {e}")
    finally:
        myDB.close()
```

### 6. Display All Transactions with Book & Member Details

```python
#Show full transaction history using JOINs
def show_transactions():
    myDB = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your-password",
        database="library_management_system"
        
    )
    if myDB is None:
        return
    try:
        cursor = myDB.cursor()
        query = """
        SELECT 
            t.ID AS TransactionID,
            b.title AS BookTitle,
            CONCAT(m.FirstName, ' ', m.LastName) AS MemberName,
            t.IssueDate,
            t.ReturnDate
        FROM transactions t
        JOIN books b ON t.BookID = b.ID
        JOIN members m ON t.MemberID = m.ID
        ORDER BY t.IssueDate DESC
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except Error as e:
        print(f"❌ Error fetching transactions: {e}")
    finally:
        myDB.close()

```
### 6. Analytics: Display Most issued books
```python
#Analytics: Most issued books

def most_issued_books(limit=5):
    myDB = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your-password",
        database="library_management_system"

    )
    if myDB is None:
        return
    try:
        cursor = myDB.cursor()
        query = """
        SELECT b.title, COUNT(t.ID) as times_issued
        FROM transactions t
        JOIN books b on t.BookID = b.ID
        GROUP BY t.BookID
        ORDER BY times_issued DESC
        LIMIT %s
        """
        cursor.execute(query, (limit,))  # Added comma to make it a tuple
        results = cursor.fetchall()
        print("📊 Most Issued Books:")
        for row in results:
            print(f"{row[0]} - {row[1]} times")
    except Error as e:
        print(f"❌ Error fetching analytics: {e}")
    finally:
        myDB.close()

```
### 7.Search books by keyword
```python
#search books by keyword
def search_books(keyword):
    myDB = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your-password",
        database="library_management_system"
        
    )
    if myDB is None:
        return
    try:
        cursor = myDB.cursor()
        query  = "SELECT * FROM books WHERE title LIKE %s"
        cursor.execute(query, ('%' + keyword + '%',))
        results = cursor.fetchall()

        for book in results:
            print(book)
    except Error as e:
        print(f"❌ Error searching books: {e}")   
    finally:
        myDB.close()         

```

---

## 🔄 SQL Utilities

### Discount Old Books

```sql
UPDATE books
SET Title = CONCAT('Discounted-', Title)
WHERE PublishedYear < 2015;
```

### Increase Sci-Fi Book Prices by 10%

```sql
UPDATE books
SET Price = Price * 1.10
WHERE Genre = 'Fiction';
```

### Late vs On-Time Returns (in SQL)

```sql
SELECT *,
CASE WHEN ReturnDate IS NULL then "Not Returned"
WHEN datediff(ReturnDate, IssueDate) > 20 then "Late Return"
ELSE "On Time"
END AS Return_Pace
FROM transactions;
```

### Remove Inactive Members (no transactions in last 2 months)

```sql
DELETE FROM members
WHERE MemberID NOT IN (
SELECT DISTINCT MemberID
FROM transactions
WHERE IssueDate >= curdate() - INTERVAL 2 month
);
```

---

## 🧠 Additional Features

* Input validation & error handling in Python
* Future-ready for adding:

  * Book search
  * Most-issued books analysis
  * Genre-based statistics

---

## 🚧 Troubleshooting Notes

* `AUTO_INCREMENT` requires column to be `PRIMARY KEY` or `UNIQUE`
* Avoid inserting `ID` manually if auto-increment is active
* Errors like `Field 'ID' doesn't have a default value` happen when `AUTO_INCREMENT` is missing
* Foreign key constraints may prevent `DROP` or `MODIFY` statements

---

## ✅ Conclusion

This Library Management System provides a hands-on way to understand relational databases, SQL operations, and CRUD application design in Python. It balances real-world use cases with academic simplicity for learning and expansion.
