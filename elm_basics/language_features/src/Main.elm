{-
    An example of a basic web app - which highlights elm's architecture
        At first it can be confusing to read, but becomes clear once 
        you draw a diagram of the circular flow of information.
    That is, exactly, the ELM Architecture.
-}
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

-- TODO(Mihai) a deep dive into types
type Messages = 
    Add
    | ChangedAddText String

{-
    The super basic model (state) - data to display
    Can be very well a record for simple cases
-}
init = 
    { value = 0
    , numberToAdd = 0
    }

{-
    View function, tells Elm how to display stuff 
    view : model -> virtual DOM
        has a list of attributes and list of contents
        e.g. div [<attributes>] [<content1> ... <contentk>]
-}
view model = 
    div [] [
        text (fromInt model.value)
        , text "\n"
        , div [] []
        , input [ onInput ChangedAddText ] []
        , button [ onClick Add ] [ text "Add" ]
    ] 

-- helper function to parse the text input provided by the user
parseNumber text =
    let
        theMaybe = toInt text
    in
        case theMaybe of 
            Just val -> 
                val
            Nothing -> 
                0

{-
    Update function, handles the changes in data over time. Returns new model
    update : msg -> model -> model
-}
update msg model =  -- item and value
    let 
        a = 1
        b = 2
        logmessage = log "msg" msg
        logmodel = log "model" model
    in
    case msg of -- returning a new model
        Add -> 
            { model | value = model.value + model.numberToAdd }
        ChangedAddText texttyped ->
            { model | numberToAdd = parseNumber texttyped }


main = -- no parameters
    Browser.sandbox -- basic app, takes a record as a parameter
        {
              init   = init   -- Initial model (bunch of data)
            , view   = view   -- view : model -> virtual DOM
            , update = update -- update : msg -> model -> model (updated)
        }