#!/usr/bin/env python3
"""
Library Management System
A comprehensive Python + MySQL application for managing books, members, and transactions.
"""

import mysql.connector
from mysql.connector import Error
from datetime import datetime
import logging
from typing import Optional, List, Tuple, Union
import sys

# Import configuration
from config import DB_CONFIG, APP_CONFIG, LOG_CONFIG

class LibraryManagementSystem:
    """Main class for Library Management System operations."""
    
    def __init__(self):
        """Initialize the Library Management System."""
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        self.connection = None
        
    def setup_logging(self) -> None:
        """Set up logging configuration."""
        logging.basicConfig(
            level=getattr(logging, LOG_CONFIG["level"]),
            format=LOG_CONFIG["format"],
            handlers=[
                logging.FileHandler(LOG_CONFIG["file"]),
                logging.StreamHandler(sys.stdout)
            ]
        )
    
    def connect_database(self) -> Optional[Union[mysql.connector.MySQLConnection, mysql.connector.PooledMySQLConnection]]: # type: ignore
        """Establish database connection with error handling."""
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            if connection.is_connected():
                self.logger.info("Successfully connected to MySQL database")
                return connection
        except Error as e:
            self.logger.error(f"Error connecting to MySQL database: {e}")
            return None
    
    def execute_query(self, query: str, params: Optional[Tuple] = None, fetch: bool = False) -> Union[Optional[List[Tuple]], bool]:
        """Execute database query with proper error handling."""
        connection = self.connect_database()
        if not connection:
            return None
            
        try:
            cursor = connection.cursor()
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchall()
                return result
            else:
                connection.commit()
                return True
                
        except Error as e:
            self.logger.error(f"Database error: {e}")
            return None
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()
    
    def validate_input(self, value: str, field_type: str, required: bool = True) -> bool:
        """Validate user input based on field type."""
        if required and not value.strip():
            print(f"❌ {field_type} is required and cannot be empty.")
            return False
            
        if field_type == "email" and value:
            if "@" not in value or "." not in value:
                print("❌ Invalid email format.")
                return False
                
        if field_type == "phone" and value:
            if not value.isdigit() or len(value) < 10:
                print("❌ Phone number must be at least 10 digits.")
                return False
                
        if field_type == "year" and value:
            try:
                year = int(value)
                if year < 1000 or year > datetime.now().year + 1:
                    print("❌ Invalid year.")
                    return False
            except ValueError:
                print("❌ Year must be a number.")
                return False
                
        if field_type == "price" and value:
            try:
                price = float(value)
                if price <= 0:
                    print("❌ Price must be greater than 0.")
                    return False
            except ValueError:
                print("❌ Price must be a number.")
                return False
                
        return True
    
    def add_book(self) -> bool:
        """Add a new book to the library."""
        print("\n📚 Add New Book")
        print("-" * 30)
        
        # Get input with validation
        title = input("Enter book title: ").strip()
        if not self.validate_input(title, "title"):
            return False
            
        author = input("Enter author name: ").strip()
        if not self.validate_input(author, "author"):
            return False
            
        genre = input("Enter genre: ").strip()
        
        year_input = input("Enter published year: ").strip()
        if not self.validate_input(year_input, "year"):
            return False
        year = int(year_input)
        
        price_input = input("Enter price: ").strip()
        if not self.validate_input(price_input, "price"):
            return False
        price = float(price_input)
        
        # Insert into database
        query = "INSERT INTO books (title, Author, Genre, PublishedYear, Price) VALUES (%s, %s, %s, %s, %s)"
        result = self.execute_query(query, (title, author, genre, year, price))
        
        if result:
            print("✅ Book added successfully.")
            self.logger.info(f"Book added: {title} by {author}")
            return True
        else:
            print("❌ Error adding book.")
            return False
    
    def show_books(self) -> None:
        """Display all books in the library."""
        query = "SELECT ID, title, Author, Genre, PublishedYear, Price FROM books ORDER BY title"
        result = self.execute_query(query, fetch=True)
        
        if isinstance(result, list):
            print("\n📚 Books in Library")
            print("-" * 80)
            print(f"{'ID':<4} {'Title':<25} {'Author':<20} {'Genre':<15} {'Year':<6} {'Price':<8}")
            print("-" * 80)
            for row in result:
                print(f"{row[0]:<4} {row[1]:<25} {row[2]:<20} {row[3] or 'N/A':<15} {row[4]:<6} ${row[5]:<8}")
        else:
            print("❌ No books found or error retrieving books.")
    
    def add_member(self) -> bool:
        """Add a new member to the library."""
        print("\n👤 Add New Member")
        print("-" * 30)
        
        first_name = input("Enter first name: ").strip()
        if not self.validate_input(first_name, "first name"):
            return False
            
        last_name = input("Enter last name: ").strip()
        if not self.validate_input(last_name, "last name"):
            return False
            
        email = input("Enter email address: ").strip()
        if not self.validate_input(email, "email"):
            return False
            
        phone = input("Enter phone number: ").strip()
        if not self.validate_input(phone, "phone"):
            return False
        
        # Insert into database
        query = "INSERT INTO members (FirstName, LastName, Email, Phone) VALUES (%s, %s, %s, %s)"
        result = self.execute_query(query, (first_name, last_name, email, phone))
        
        if result:
            print("✅ Member added successfully.")
            self.logger.info(f"Member added: {first_name} {last_name}")
            return True
        else:
            print("❌ Error adding member. Email might already exist.")
            return False
    
    def show_members(self) -> None:
        """Display all members."""
        query = "SELECT ID, FirstName, LastName, Email, Phone FROM members ORDER BY LastName, FirstName"
        result = self.execute_query(query, fetch=True)
        
        if isinstance(result, list):
            print("\n👥 Library Members")
            print("-" * 70)
            print(f"{'ID':<4} {'Name':<25} {'Email':<25} {'Phone':<15}")
            print("-" * 70)
            for row in result:
                full_name = f"{row[1]} {row[2]}"
                print(f"{row[0]:<4} {full_name:<25} {row[3]:<25} {row[4]:<15}")
        else:
            print("❌ No members found or error retrieving members.")
    
    def issue_book(self) -> bool:
        """Issue a book to a member."""
        print("\n📖 Issue Book")
        print("-" * 30)
        
        try:
            book_id = int(input("Enter Book ID to issue: "))
            member_id = int(input("Enter Member ID: "))
        except ValueError:
            print("❌ Invalid input. Please enter numeric IDs.")
            return False
        
        # Check if book exists
        book_query = "SELECT title FROM books WHERE ID = %s"
        book_result = self.execute_query(book_query, (book_id,), fetch=True)
        if not book_result:
            print("❌ Book ID not found.")
            return False
        
        # Check if member exists
        member_query = "SELECT CONCAT(FirstName, ' ', LastName) as name FROM members WHERE ID = %s"
        member_result = self.execute_query(member_query, (member_id,), fetch=True)
        if not member_result:
            print("❌ Member ID not found.")
            return False
        
        # Check if book is already issued
        issued_query = "SELECT * FROM transactions WHERE BookID = %s AND ReturnDate IS NULL"
        issued_result = self.execute_query(issued_query, (book_id,), fetch=True)
        if issued_result:
            print("⚠️ This book is currently issued and hasn't been returned.")
            return False
        
        # Check member's current book count
        count_query = "SELECT COUNT(*) FROM transactions WHERE MemberID = %s AND ReturnDate IS NULL"
        count_result = self.execute_query(count_query, (member_id,), fetch=True)
        if isinstance(count_result, list) and count_result[0][0] >= APP_CONFIG["max_books_per_member"]:
            print(f"⚠️ Member has reached maximum limit of {APP_CONFIG['max_books_per_member']} books.")
            return False
        
        # Issue the book
        issue_query = "INSERT INTO transactions (BookID, MemberID, IssueDate) VALUES (%s, %s, CURDATE())"
        result = self.execute_query(issue_query, (book_id, member_id))
        
        if result and isinstance(book_result, list) and isinstance(member_result, list):
            book_title = book_result[0][0]
            member_name = member_result[0][0]
            print(f"✅ Book '{book_title}' successfully issued to {member_name}.")
            self.logger.info(f"Book issued: {book_title} to {member_name}")
            return True
        else:
            print("❌ Error issuing book.")
            return False
    
    def return_book(self) -> bool:
        """Return a book and calculate fine."""
        print("\n📚 Return Book")
        print("-" * 30)
        
        try:
            transaction_id = int(input("Enter Transaction ID: "))
        except ValueError:
            print("❌ Invalid input. Please enter numeric Transaction ID.")
            return False
        
        # Check if transaction exists and book is not returned
        check_query = """
            SELECT t.BookID, t.MemberID, t.IssueDate, b.title, 
                   CONCAT(m.FirstName, ' ', m.LastName) as member_name
            FROM transactions t
            JOIN books b ON t.BookID = b.ID
            JOIN members m ON t.MemberID = m.ID
            WHERE t.ID = %s AND t.ReturnDate IS NULL
        """
        check_result = self.execute_query(check_query, (transaction_id,), fetch=True)
        
        if not check_result:
            print("❌ Transaction not found or book already returned.")
            return False
        
        # Update return date
        return_query = "UPDATE transactions SET ReturnDate = CURDATE() WHERE ID = %s"
        result = self.execute_query(return_query, (transaction_id,))
        
        if result:
            # Calculate fine
            fine_query = """
                SELECT 
                    CASE 
                        WHEN DATEDIFF(ReturnDate, IssueDate) > %s 
                        THEN (DATEDIFF(ReturnDate, IssueDate) - %s) * %s
                        ELSE 0
                    END AS fine
                FROM transactions
                WHERE ID = %s
            """
            fine_result = self.execute_query(
                fine_query, 
                (APP_CONFIG["grace_period_days"], APP_CONFIG["grace_period_days"], 
                 APP_CONFIG["fine_rate_per_day"], transaction_id), 
                fetch=True
            )
            
            fine = fine_result[0][0] if isinstance(fine_result, list) and fine_result else 0
            
            # Update fine amount
            if fine > 0:
                update_fine_query = "UPDATE transactions SET FineAmount = %s WHERE ID = %s"
                self.execute_query(update_fine_query, (fine, transaction_id))
            
            if isinstance(check_result, list):
                book_title = check_result[0][3]
                member_name = check_result[0][4]
                print(f"✅ Book '{book_title}' returned by {member_name}.")
                print(f"💰 Fine: ${fine:.2f}")
                self.logger.info(f"Book returned: {book_title} by {member_name}, Fine: ${fine:.2f}")
                return True
        
        print("❌ Error returning book.")
        return False
    
    def show_transactions(self) -> None:
        """Display transaction history with book and member details."""
        query = """
            SELECT 
                t.ID AS TransactionID,
                b.title AS BookTitle,
                CONCAT(m.FirstName, ' ', m.LastName) AS MemberName,
                t.IssueDate,
                t.ReturnDate,
                t.FineAmount,
                CASE 
                    WHEN t.ReturnDate IS NULL THEN 'Issued'
                    ELSE 'Returned'
                END AS Status
            FROM transactions t
            JOIN books b ON t.BookID = b.ID
            JOIN members m ON t.MemberID = m.ID
            ORDER BY t.IssueDate DESC
        """
        result = self.execute_query(query, fetch=True)
        
        if isinstance(result, list):
            print("\n📋 Transaction History")
            print("-" * 100)
            print(f"{'ID':<4} {'Book Title':<25} {'Member':<20} {'Issue Date':<12} {'Return Date':<12} {'Fine':<8} {'Status':<10}")
            print("-" * 100)
            for row in result:
                return_date = row[4].strftime('%Y-%m-%d') if row[4] else 'N/A'
                fine = f"${row[5]:.2f}" if row[5] else "$0.00"
                print(f"{row[0]:<4} {row[1]:<25} {row[2]:<20} {row[3]:<12} {return_date:<12} {fine:<8} {row[6]:<10}")
        else:
            print("❌ No transactions found.")
    
    def search_books(self) -> None:
        """Search books by keyword."""
        keyword = input("Enter search keyword: ").strip()
        if not keyword:
            print("❌ Search keyword cannot be empty.")
            return
        
        query = "SELECT ID, title, Author, Genre, PublishedYear, Price FROM books WHERE title LIKE %s OR Author LIKE %s"
        result = self.execute_query(query, (f'%{keyword}%', f'%{keyword}%'), fetch=True)
        
        if isinstance(result, list):
            print(f"\n🔍 Search Results for '{keyword}'")
            print("-" * 80)
            print(f"{'ID':<4} {'Title':<25} {'Author':<20} {'Genre':<15} {'Year':<6} {'Price':<8}")
            print("-" * 80)
            for row in result:
                print(f"{row[0]:<4} {row[1]:<25} {row[2]:<20} {row[3] or 'N/A':<15} {row[4]:<6} ${row[5]:<8}")
        else:
            print(f"❌ No books found matching '{keyword}'.")
    
    def most_issued_books(self) -> None:
        """Display analytics for most issued books."""
        try:
            limit = int(input("Enter number of top books to display (default 5): ") or "5")
        except ValueError:
            limit = 5
        
        query = """
            SELECT b.title, b.Author, COUNT(t.ID) as times_issued
            FROM transactions t
            JOIN books b ON t.BookID = b.ID
            GROUP BY t.BookID, b.title, b.Author
            ORDER BY times_issued DESC
            LIMIT %s
        """
        result = self.execute_query(query, (limit,), fetch=True)
        
        if isinstance(result, list):
            print(f"\n📊 Top {limit} Most Issued Books")
            print("-" * 60)
            print(f"{'Title':<30} {'Author':<20} {'Times Issued':<12}")
            print("-" * 60)
            for row in result:
                print(f"{row[0]:<30} {row[1]:<20} {row[2]:<12}")
        else:
            print("❌ No transaction data found.")
    
    def show_menu(self) -> None:
        """Display the main menu."""
        print("\n" + "="*50)
        print("📚 LIBRARY MANAGEMENT SYSTEM")
        print("="*50)
        print("1.  Add Book")
        print("2.  Show All Books")
        print("3.  Add Member")
        print("4.  Show All Members")
        print("5.  Issue Book")
        print("6.  Return Book")
        print("7.  Show Transactions")
        print("8.  Search Books")
        print("9.  Most Issued Books")
        print("10. Exit")
        print("-"*50)
    
    def run(self) -> None:
        """Main application loop."""
        print("🚀 Starting Library Management System...")
        
        # Test database connection
        if not self.connect_database():
            print("❌ Failed to connect to database. Please check your configuration.")
            return
        
        while True:
            try:
                self.show_menu()
                choice = input("Enter your choice (1-10): ").strip()
                
                if choice == '1':
                    self.add_book()
                elif choice == '2':
                    self.show_books()
                elif choice == '3':
                    self.add_member()
                elif choice == '4':
                    self.show_members()
                elif choice == '5':
                    self.issue_book()
                elif choice == '6':
                    self.return_book()
                elif choice == '7':
                    self.show_transactions()
                elif choice == '8':
                    self.search_books()
                elif choice == '9':
                    self.most_issued_books()
                elif choice == '10':
                    print("👋 Thank you for using Library Management System!")
                    self.logger.info("Application terminated by user")
                    break
                else:
                    print("❌ Invalid choice. Please enter a number between 1-10.")
                
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\n👋 Application terminated by user.")
                self.logger.info("Application terminated by KeyboardInterrupt")
                break
            except Exception as e:
                print(f"❌ An unexpected error occurred: {e}")
                self.logger.error(f"Unexpected error: {e}")


def main():
    """Main entry point of the application."""
    try:
        lms = LibraryManagementSystem()
        lms.run()
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        logging.error(f"Failed to start application: {e}")


if __name__ == "__main__":
    main()
