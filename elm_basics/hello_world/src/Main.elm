module Main exposing (..)

import Html exposing (div, text, input, button, p)
import Html.Events exposing (onClick, onInput)
import Browser
import String exposing (fromInt, toInt)

import Debug exposing (log)


-- elm will not compile code not utilized!
my_function : String -> String
my_function x 
    = "Hello " ++ x ++ "!" 

add a  b = a + b

type Messages = 
    Add -- kinda' like constants
    | ChangedAddText String

-- Three parts of the architecture:
-- View: something to display
-- Model: data to display
-- Update function: handles the changes in data over time
--    new value of the model

init = 
    { value = 0
    , numberToAdd = 0
    }

view model = -- list of attributes and list of contents
    div [] [
        text (fromInt model.value)
        , text "\n"
        , div [] []
        , input [ onInput ChangedAddText] []
        , button [ onClick Add ][text "Add"]
    ] 

parseNumber text = 
    let
        theMaybe = toInt text
    in
        case theMaybe of 
            Just val -> 
                val
            Nothing -> 
                0


update msg model =  -- item and value
    let 
        a = 1
        b = 2
        logmessage = log "msg" msg
        logmodel = log "model" model
    in

    -- returning
    case msg of
        Add -> 
            { model | value = model.value + model.numberToAdd }
        ChangedAddText texttyped ->
            { model | numberToAdd = parseNumber texttyped }


main = -- no parameters
    Browser.sandbox -- basic app, takes a record as a parameter
        {
            init = init -- property 1: initial model
            , view = view -- something which draws
            , update = update -- reducer function (comprehension)
        }
    -- Html.text "Hello!"
