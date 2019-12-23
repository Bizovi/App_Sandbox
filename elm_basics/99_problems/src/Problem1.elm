module Problem1 exposing (..)
import Html exposing (..)
import Maybe



last : List a -> Maybe a
last xs = 
  -- the implementation
  List.reverse xs |> List.head


main : Html.Html a
main = 
  Html.text
    <| case test of
      0 -> 
        "Your implementation passed all tests"
      1 ->
        "Your implementation failed one test."
      x -> 
        "Your implementation failed " ++ (String.fromInt x) ++ " tests."


test : Int
test = 
  List.length
    <| List.filter ((==) False)
      [ last [ 1, 2, 3, 4 ] == Just 4
      , last [ 1 ] == Just 1
      , last [] == Nothing
      , last [ 'a', 'b', 'c' ] == Just 'c'
      ]