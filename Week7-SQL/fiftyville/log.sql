-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Check the crime_scene_reports at July 28th.
SELECT description
FROM crime_scene_reports
WHERE month = 7 AND day= 28
AND street = 'Humphrey Street'
/* Result:
Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery.
Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery.
Littering took place at 16:36. No known witnesses.
*/

-- Check Bakery Witnesses
SELECT * FROM interviews
WHERE month = 7 AND day= 28
AND transcript LIKE '%bakery%'
/* Result:
Ruth - Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away.
    If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.
Eugene - I don't know the thief's name, but it was someone I recognized. Earlier this morning,
    before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.
Raymond - As the thief was leaving the bakery, they called someone who talked to them for less than a minute.
    In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket.
*/

-- According to what Ruth said and checking bakery security logs
SELECT *
FROM bakery_security_logs
WHERE year = 2023 AND month = 7 AND day= 28
AND hour = 10 AND minute BETWEEN 15 AND 25

-- Check against license plates
SELECT p.name, bsl.activity, bsl.license_plate, bsl.year, bsl.day, bsl.minute
FROM bakery_security_logs AS bsl
JOIN people AS p ON p.license_plate = bsl.license_plate
WHERE bsl.year = 2023 AND bsl.month = 7 AND bsl.day = 28
AND bsl.hour = 10 AND bsl.minute BETWEEN 15 AND 25

-- According to what witness 2: Eugene said and checking atm transaction
SELECT * FROM atm_transactions
WHERE atm_location = 'Leggett Street'
AND year = 2023 AND month = 7 AND day = 28

-- Add name of withdraws from atm
SELECT a.*, p.name
FROM atm_transactions AS a
JOIN bank_accounts AS b ON a.account_number = b.account_number
JOIN people AS p ON b.person_id = p.id
WHERE a.atm_location = 'Leggett Street' AND a.year = 2023 AND a.month = 7 AND a.day = 28
AND a.transaction_type = 'withdraw'

-- According to what witness 3: Raymond said and checking phone calls
SELECT *
FROM phone_calls
WHERE year = 2023 AND month = 7 AND day = 28 AND duration < 60

-- Add name to call list of callers and reciever
SELECT pc.name as caller_name ,pr.name as receiver_name, c.caller, c.receiver, c.year, c.month, c.day, c.duration
FROM phone_calls AS c
JOIN people AS pc ON c.caller = pc.phone_number
JOIN people AS pr ON c.receiver = pr.phone_number
WHERE c.year = 2023 AND c.month = 7 AND c.day = 28 AND c.duration < 60

-- Find fiftyville's airport data
SELECT * FROM airports
WHERE city = 'Fiftyville'
/* Result:
    id | abbreviation |          full_name          |    city
    8  | CSF          | Fiftyville Regional Airport | Fiftyville
*/

-- Find first flights out from fiftyville id(8)
SELECT f.*, ori.full_name AS origin_airport, des.full_name AS destination_airport
FROM flights AS f
JOIN airports AS ori ON f.origin_airport_id = ori.id
JOIN airports AS des ON f.destination_airport_id = des.id
WHERE ori.id =8 AND f.year = 2023 AND f.month = 7 AND f.day = 29
ORDER BY f.hour, f.minute
/* Result:
    id | origin_airport_id | destination_airport_id | year | month | day | hour | minute |       origin_airport        |         destination_airport         |
    36 | 8                 | 4                      | 2023 | 7     | 29  | 8    | 20     | Fiftyville Regional Airport | LaGuardia Airport
*/

-- Find destination airport
SELECT * FROM airports
WHERE id = 4
/* Result:
    id | abbreviation |     full_name     |     city      |
    4  | LGA          | LaGuardia Airport | New York City |
*/

-- Combine all info
SELECT p.name
FROM bakery_security_logs AS bsl
JOIN people AS p ON p.license_plate = bsl.license_plate
JOIN bank_accounts AS b ON b.person_id = p.id
JOIN atm_transactions AS a ON a.account_number = b.account_number
JOIN phone_calls AS c ON c.caller = p.phone_number
WHERE bsl.year = 2023 AND bsl.month = 7 AND bsl.day = 28 AND bsl.hour = 10 AND bsl.minute BETWEEN 15 AND 25
AND a.atm_location = 'Leggett Street' AND a.year = 2023 AND a.month = 7 AND a.day = 28 AND a.transaction_type = 'withdraw'
AND c.year = 2023 AND c.month = 7 AND c.day = 28 AND c.duration < 60
/* Result:
    Bruce ,Diana
*/

-- Check who is on flight
SELECT p.name
FROM people AS p
JOIN passengers AS ps ON p.passport_number = ps.passport_number
WHERE ps.flight_id = 36
AND p.name IN ('Bruce', 'Diana')
/* Result:
    Bruce
*/

-- Find who did Bruce call
SELECT p2.name AS receiver
FROM phone_calls AS c
JOIN people AS p1 ON c.caller = p1.phone_number
JOIN people AS p2 ON c.receiver = p2.phone_number
WHERE p1.name = 'Bruce' AND c.year = 2023 AND c.month = 7 AND c.day = 28 AND c.duration < 60
/* Result:
    Robin
*/
