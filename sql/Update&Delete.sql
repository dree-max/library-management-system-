/* 
Update/Delete:
*/

/* This is to modify/add character length(varchar) for the table 'books' title
ALTER TABLE books
MODIFY title VARCHAR(150);
*/

-- • Increase the price of all books in the "Science Fiction" genre by 10%.

USE library_management_system;

/* This is a preview before changing the data in the table
SELECT*
FROM books
WHERE Genre = 'Fiction';
*/

UPDATE books
SET Price = Price * 1.10
WHERE Genre = 'Fiction';


-- • Change the issue date for a specific transaction to January 1, 2025, for a transaction with TransactionID = 101.

/* This is a preview before deletion
SELECT *
FROM transactions
WHERE transactions.ID = '20';
*/

UPDATE transactions
SET IssueDate = "2025-01-01"
WHERE transactions.ID = '20';


-- • Mark all books published before 2015 as discounted by adding the word "Discounted" to their title.

/* This is a preview before deletion
SELECT *
FROM books;

 UPDATE books
SET title = REGEXP_REPLACE(title, '^Discounted - ?', '') -- used this query to clean up my titke data
WHERE title LIKE 'Discounted -%';
*/

UPDATE books
SET title = LEFT(CONCAT('Discounted - ', title), 100)
WHERE PublishedYear < 2015
  AND title NOT LIKE 'Discounted -%';


-- • Remove all members who haven't made a transaction in the past 2 MONTHS.

/*This is a preview before deletion
SELECT*
FROM transactions
WHERE MemberID NOT IN (
SELECT DISTINCT MemberID
FROM transactions
WHERE IssueDate >= curdate() - INTERVAL 5 month
);
*/

DELETE FROM members
WHERE MemberID NOT IN (
SELECT DISTINCT MemberID
FROM transactions
WHERE IssueDate >= curdate() - INTERVAL 5 month
);


-- • Delete transactions where the book has not been returned (ReturnDate IS NULL) and the issue date is over 4 months old.

/* This is a preview before deletion
SELECT *
FROM transactions
WHERE  transactions.ID NOT IN (
    SELECT DISTINCT BookID
    FROM books
    WHERE IssueDate >= CURDATE() - INTERVAL 4 MONTH
    AND ReturnDate IS NULL
);
*/

DELETE 
FROM transactions
WHERE transactions.ID NOT IN (
SELECT DISTINCT BookID
FROM books
WHERE IssueDate >= curdate() - INTERVAL 4 month 
AND ReturnDate IS NULL
);


-- • Remove all books that were published before 2000 and haven't been issued in the last 5 years

/* This is a preview before deleting
SELECT *
FROM books
WHERE PublishedYear < 2000
  AND ID NOT IN (
      SELECT DISTINCT BookID
      FROM transactions
      WHERE IssueDate >= CURDATE() - INTERVAL 5 YEAR
  );
*/

DELETE FROM books
WHERE PublishedYear < 2000
AND ID NOT IN (
SELECT DISTINCT BookID
FROM transactions
WHERE IssueDate >= curdate() - interval 5 YEAR
)