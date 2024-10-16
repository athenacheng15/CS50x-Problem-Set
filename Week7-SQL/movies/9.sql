-- write a SQL query to list the names of all people who starred in a movie released in 2004, ordered by birth year.
SELECT people.name
FROM people
JOIN stars ON stars.person_id = people.id
JOIN movies ON movies.id = stars.movie_id
WHERE movies.year = 2004 AND people.birth IS NOT NULL
ORDER BY people.birth;
