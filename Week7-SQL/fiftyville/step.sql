SELECT p2.name AS receiver
FROM phone_calls AS c
JOIN people AS p1 ON c.caller = p1.phone_number
JOIN people AS p2 ON c.receiver = p2.phone_number
WHERE p1.name = 'Bruce' AND c.year = 2023 AND c.month = 7 AND c.day = 28 AND c.duration < 60
