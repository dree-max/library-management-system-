/* 
Conditional Queries: 
*/

-- • Find the return date for all transactions and display "Not Returned" if the book hasn't been returned yet.
SELECT 
    transactions.ID, 
    IF(transactions.ReturnDate IS NULL, 'Not Returned', transactions.ReturnDate) AS ReturnDate
FROM transactions;

-- • Write a query to calculate fines for all transactions. If a book is returned within 14 
-- days, the fine should be NULL.
SELECT 
    ID,
    IssueDate,
    ReturnDate,
    CASE
        WHEN ReturnDate IS NULL THEN DATEDIFF(CURDATE(), IssueDate) - 14
        WHEN DATEDIFF(ReturnDate, IssueDate) <= 14 THEN NULL
        ELSE DATEDIFF(ReturnDate, IssueDate) - 14
    END AS FineAmount
FROM transactions;


-- • Write a query to categorize books by their price range:
-- 1. "Low Price" for books under $10
-- 2. "Medium Price" for books between $10 and $20
-- 3. "High Price" for books above $20
USE library_management_system;
SELECT ID,
title,
Author,
Genre,
Price,
PublishedYear,
CASE WHEN Price < 10 then "Low Price"
 WHEN Price between 10 and 20 then "Medium Price"
 WHEN Price > 20 then "High Price" END AS Price_range
FROM books;

-- • Write a query to mark books as "Expensive" if their price is above $20; otherwise,mark them as "Affordable".
SELECT ID,
title,
Author,
Genre,
Price,
PublishedYear,
IF (Price > 20, "Expensive", "Affordable") AS Price_Category
FROM books;


-- • Show Transactions with "Late Return" or "On Time"
SELECT *,
CASE WHEN ReturnDate IS NULL then "Not Returned"
WHEN datediff(ReturnDate, IssueDate) > 20 then "Late Return"
ELSE "On Time"
END AS Return_Pace
FROM transactions;
