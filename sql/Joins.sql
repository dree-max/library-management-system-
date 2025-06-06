/* Joins:
*/

-- • Fetch the transaction details (TransactionID, Book Title, Member Name, Issue Date) 
-- by joining Transactions, Books, and Members.
USE library_management_system;
SELECT transactions.ID, books.title, members.FirstName, members.LastName, transactions.IssueDate
FROM transactions
LEFT JOIN books on books.ID = transactions.BookID
LEFT JOIN Members on members.ID = transactions.MemberID;


-- • List all books along with the transaction details, including books that haven’t been issued yet.
USE library_management_system;
SELECT books.ID, 
books.title, 
books.Author, 
books.Genre, 
books.Price, 
books.PublishedYear,
transactions.IssueDate,
transactions.ReturnDate,
transactions.FineAmount
FROM books
LEFT JOIN transactions ON books.ID = transactions.BookID;
/* NOTE 
Books with 'NULL' in issuedate & returndate are books that have not been issued yet 
*/

-- • Find all members and their issued books, including members who haven't issued any 
-- books and books that haven’t been issued. Hint: Use UNION to simulate a full outer 
-- join (MySQL does not natively support FULL OUTER JOIN).
USE library_management_system;
SELECT m.ID AS memberID,
m.FirstName,
m.LastName,
m.Email,
m.Phone,
b.title,
b.Author,
b.Genre,
b.Price,
b.PublishedYear
FROM members m
LEFT JOIN transactions t ON m.ID = t.MemberID
LEFT JOIN books b ON b.ID = t.BookID

UNION 

SELECT m2.ID, 
m2.FirstName,
m2.LastName,
m2.Email,
m2.Phone,
b2.title,
b2.Author,
b2.Genre,
b2.Price,
b2.PublishedYear
FROM books b2
LEFT JOIN transactions t2 ON b2.ID = t2.BookID
LEFT JOIN members m2 ON m2.ID = t2.MemberID;



-- • RIGHT JOIN for Members and Their Issued Books
USE library_management_system;
SELECT m.ID AS memberID,
m.FirstName,
m.LastName,
m.Email,
m.Phone,
b.title,
b.Author,
b.Genre,
b.Price,
b.PublishedYear
FROM members m
RIGHT JOIN transactions t ON m.ID = t.MemberID
RIGHT JOIN books b ON b.ID = t.BookID

UNION 

SELECT m2.ID, 
m2.FirstName,
m2.LastName,
m2.Email,
m2.Phone,
b2.title,
b2.Author,
b2.Genre,
b2.Price,
b2.PublishedYear
FROM books b2
RIGHT JOIN transactions t2 ON b2.ID = t2.BookID
RIGHT JOIN members m2 ON m2.ID = t2.MemberID;
