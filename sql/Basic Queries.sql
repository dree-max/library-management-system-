/*
Basic Queries: 
*/

-- • Write a query to retrieve the details of all books where the price is greater than $15. 
USE library_management_system;
SELECT *
FROM Books
WHERE Price > 15;


-- • Fetch the first and last names of all members who have "Smith" in their last name. 
SELECT FirstName, LastName
FROM MEMBERS
WHERE LastName = 'Smith';


-- • Fetch all books ordered by their price in descending order. 
SELECT*
FROM books
ORDER BY Price Desc;


-- • Count the number of books in each genre, and display only genres with more than 1 book. 
SELECT Genre, COUNT(*) AS book_genre_count
FROM Books
GROUP BY Genre
HAVING COUNT(*) > 1;


-- • Find all members whose first name starts with the letter 'A' (use a wildcard in WHERE). 
SELECT*
FROM members
WHERE FirstName LIKE 'A%';


-- • Retrieve Books Published After 2010 and Sort Alphabetically 
SELECT*
FROM books
WHERE PublishedYear > 2010 
ORDER BY title ASC;


-- • Count Transactions for Each Member (with HAVING Clause)
SELECT MemberID, count(*) AS Mem_transaction
FROM transactions
GROUP BY MemberID
HAVING Mem_transaction >= 1;




