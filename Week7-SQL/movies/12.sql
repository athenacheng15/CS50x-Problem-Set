-- write a SQL query to list the titles of all movies in which both Bradley Cooper and Jennifer Lawrence starred.
SELECT movies.title
FROM movies
JOIN stars AS stars1 ON stars1.movie_id = movies.id
JOIN stars AS stars2 ON stars2.movie_id = movies.id
JOIN people AS people1 ON people1.id = stars1.person_id
JOIN people AS people2 ON people2.id = stars2.person_id
WHERE people1.name = 'Bradley Cooper' AND people2.name = 'Jennifer Lawrence'
GROUP BY movies.title;
