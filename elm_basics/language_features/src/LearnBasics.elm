{-
    This script explores the basic syntax of Elm, not diving into web apps
    It is meant to be run in the REPL and is not a working app otherwise.
-}

-- loading packages
import Tuple exposing (..)

{-
    ==== Variables, constants, expressions and control flow =====
    =============================================================
-}
pi_message = 
    "Pi has the value of (around) " ++ String.fromFloat pi ++ "."

my_name = "Mihai"  -- can't reassign it later (constant)
greet_name = 
    if my_name == "Mihai" then "Hello, Mihai!" else "Hello, Stranger!"

{-
    Boolean operations look like this, similar to other programming languages
    Except the weird sign for not equal '/='
    -- 1 + 1 == 2
    -- (1 + 1 /= 2) || (True && False)
-}

{-
    ==== Functions, lists and elements of Functional Programming =====
    ==================================================================
-}
elf_counts = List.range -1 5
nameOfElf elfCount = 
    if elfCount == 1 then
        "elf"
    else if elfCount >= 0 then 
        "elves"
    else
        "anti-elves"

-- note that << is a function composition operator
elf_counts |> List.map (String.toUpper << nameOfElf) 


-- isKeepable : Char -> Bool
isKeepable character = character /= '-'

-- normalizePhoneNumber : String -> String
normalizePhoneNumber number = 
    String.filter isKeepable number
phone_number = normalizePhoneNumber "800-555-1234"

-- Scoping in elm with a let statement
withoutDashes number = 
    let 
        dash = '-'
        isKeepable2 character = character /= dash
    in
    String.filter isKeepable2 number

withoutDashes "800-555-1234"

-- these are equivalent for the use-case
String.filter (\ x -> Char.isDigit x ) "800-555-1234"
String.filter Char.isDigit "800-555-1234"
String.filter (\ x -> x /= '-') "(800)-555-1234"
["(800)-555-1234", "800-555-1234"] |> List.map (String.filter Char.isDigit)
 
-- interesting question of a safeDivide function
negate 42

List.length (List.range 1 12 |> 
    List.filter (\x -> x // 2 > 3)) |> 
        (\ x -> x^2 ) |> (*) 2


celebrateBirthday person = 
    { person | age = person.age + 1 }

curry = { first = "Curry", last = "Haskell", age = 60 }
celebrateBirthday curry

{-
    ==== Basic data structures: lists, tuples and records =====
    ===========================================================
-}

-- Tuples
-- isValidName String -> ( Bool, String )
isValidName name =
    if String.length name <= 20 then
        (True, "name accepted!")
    else
        (False, "name way too long; max 20 characters")
isValidName "Tom"
isValidName "Khaleesi queen of targariens from the house of ..."

Tuple.mapFirst (String.toUpper << String.reverse) ("stressed", 2)

multiply (x, y, z) = x * y * z  -- unpacking tupled arguments, as in python
multiply (2, 3, 5)


-- Lists
concatendated_list = [1, 2, 3] ++ [4, 5] ++ List.range -2 4


-- Records
catClub = { name = "Li", cats = 2 }
catClub2 = { catClub | cats = 3}
catClub3 = {catClub2 | name = "Cat Lord", cats = 77}
String.toUpper catClub3.name

List.map .name [catClub, catClub2, catClub3]
