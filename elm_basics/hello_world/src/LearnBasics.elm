-- This file is meant to be ran in REPL
import Tuple exposing (..)

pi_message = 
    "Pi has the value of (around) " ++ String.fromFloat pi ++ "."


my_name = "Mihai"  -- can't reassign it later (const)

greet_name = 
    if my_name == "Mihai" then "Ceva" else "Altceva"


-- 1 + 1 == 2
-- (1 + 1 /= 2) || (True && False)

elfLabel value = 
    if value == 1 then "elf" else "elves"


elfLabel 1


elfCounts = [0, 1, 2, 3, -1]
nameOfElf elfCount = 
    if elfCount == 1 then
        "elf"
    else if elfCount >= 0 then 
        "elves"
    else
        "anti-elves"

List.map nameOfElf elfCounts

-- isKeepable : Char -> Bool
isKeepable character = character /= '-'
String.filter isKeepable "800-555-1234"

-- wrapping it up in a function
-- normalizePhoneNumber : String -> String
normalizePhoneNumber number = 
    String.filter isKeepable number

normalizePhoneNumber "800-555-1234"

{-
Scoping in elm with a let statement
-}
withoutDashes number = 
    let 
        dash = '-'
        isKeepable2 character = 
            character /= dash
    in
    String.filter isKeepable2 number


withoutDashes "800-555-1234"

-- these are equivalent
String.filter (\ x -> Char.isDigit x ) "800-555-1234"
String.filter Char.isDigit "800-555-1234"

String.filter (\ x -> x /= '-') "(800)-555-1234"

-- interesting question of a safeDivide function
negate 42


List.length (List.range 1 12 |> 
    List.filter (\x -> x // 2 > 3)) |> 
        (\ x -> x^2 ) |> (*) 2


[1, 2, 3] ++ [4, 5]


catClub = { name = "Li", cats = 2 }
catClub2 = { catClub | cats = 3}
catClub3 = {catClub2 | name = "Cat Lord", cats = 77}


Tuple.mapFirst String.reverse ("stressed", 2)

multiply (x, y, z) = x * y * z
multiply (2, 3, 4)


