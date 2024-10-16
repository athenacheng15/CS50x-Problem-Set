-- write a SQL query to list the names of all people who starred in a movie in which Kevin Bacon also starred.
SELECT DISTINCT people.name
FROM people
JOIN stars AS stars1 ON stars1.person_id = people.id
JOIN stars AS stars2 ON stars2.movie_id = movies.id
JOIN movies ON movies.id = stars1.movie_id
JOIN people AS people2 ON people2.id = stars2.person_id
WHERE people2.name = 'Kevin Bacon' AND people2.birth = 1958 AND people.name <> 'Kevin Bacon';
