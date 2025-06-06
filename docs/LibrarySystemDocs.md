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
from datetime import date

def connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="yourpassword",
        database="library_management_system"
    )
```

---

### 2. Add a Book

```python
def add_book(title, author, genre, published_year, price):
    db = connect()
    cursor = db.cursor()
    query = "INSERT INTO books (Title, Author, Genre, PublishedYear, Price) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (title, author, genre, published_year, price))
    db.commit()
    db.close()
    print("✅ Book added.")
```

### 3. Add a Member

```python
def add_member(first_name, last_name, email, phone):
    db = connect()
    cursor = db.cursor()
    query = "INSERT INTO members (FirstName, LastName, Email, Phone) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (first_name, last_name, email, phone))
    db.commit()
    db.close()
    print("✅ Member added.")
```

### 4. Issue a Book

```python
def issue_book(book_id, member_id):
    db = connect()
    cursor = db.cursor()
    query = "INSERT INTO transactions (BookID, MemberID, IssueDate) VALUES (%s, %s, CURDATE())"
    cursor.execute(query, (book_id, member_id))
    db.commit()
    db.close()
    print("📚 Book issued.")
```

### 5. Return a Book + Fine Calculation

```python
def return_book(transaction_id):
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT IssueDate FROM transactions WHERE ID = %s", (transaction_id,))
    issue_date = cursor.fetchone()[0]

    return_date = date.today()
    days_borrowed = (return_date - issue_date).days

    fine = 0
    if days_borrowed > 7:
        fine = (days_borrowed - 7) * 10  # ₹10 per day after 1 week

    cursor.execute("UPDATE transactions SET ReturnDate = %s WHERE ID = %s", (return_date, transaction_id))
    db.commit()
    db.close()
    print(f"✅ Book returned. Fine: ₹{fine}")
```

### 6. Display All Transactions with Book & Member Details

```python
def show_transactions():
    db = connect()
    cursor = db.cursor()
    query = """
        SELECT t.ID, b.Title, m.FirstName, m.LastName, t.IssueDate, t.ReturnDate
        FROM transactions t
        JOIN books b ON t.BookID = b.ID
        JOIN members m ON t.MemberID = m.ID
    """
    cursor.execute(query)
    for row in cursor.fetchall():
        print(row)
    db.close()
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
WHERE Genre = 'Science Fiction';
```

### Late vs On-Time Returns (in SQL)

```sql
SELECT *,
CASE
  WHEN DATEDIFF(ReturnDate, IssueDate) > 7 THEN 'Late Return'
  ELSE 'On Time'
END AS ReturnStatus
FROM transactions;
```

### Remove Inactive Members (no transactions in last 2 months)

```sql
DELETE FROM members
WHERE ID NOT IN (
    SELECT DISTINCT MemberID
    FROM transactions
    WHERE IssueDate >= CURDATE() - INTERVAL 2 MONTH
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
