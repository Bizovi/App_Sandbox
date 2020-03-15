{-
    An example of a basic web app - which highlights elm's architecture
        At first it can be confusing to read, but becomes clear once 
        you draw a diagram of the circular flow of information.
    That is, exactly, the ELM Architecture.
-}
module Main exposing (..)

import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (onClick, onInput)
import Browser
import String exposing (fromInt, toInt)

import Debug exposing (log)

{-
    main is a special value, which describes what is shown on screen
    basically, a high level description of the program
    
    Browser.sandbox is a basic app, takes a record as a parameter
-}
main = -- no parameters
    Browser.sandbox
        {
              init   = init   -- Initial model (bunch of data)
            , view   = view   -- view : model -> virtual DOM
            , update = update -- update : msg -> model -> model (updated)
        }

{-  
    Types and data models are super important - capture all details of app data
    Can be very well a record for simple cases
    -- TODO(Mihai) a deep dive into types
-}

-- Add : Messages
-- ChangedAddText <function> : String.String -> Messages
type Messages = -- choice type for messages
    Add 
    | ChangedAddText String  
    | Reset
    | IncrementByTen
    | InputTextReversed String
    | Name String
    | Password String
    | PasswordAgain String
    | InputTemperature String


type PasswordStatus = 
    OK | TooShort | NotMatching

-- Model <function> : Int -> Int -> Model
type alias Model = 
    { value : Int
    , numberToAdd : Int
    , textString : String
    , name : String
    , password : String
    , passwordAgain : String
    , temperature : String
    }

init : Model
init = -- initialize the model
    { value = 0
    , numberToAdd = 0
    , textString = ""
    , name = ""
    , password = ""
    , passwordAgain = ""
    , temperature = ""
    }

{-
    Update function, handles the changes in data over time. Returns new model
    update : msg -> model -> model

    -- helper function to parse the text input provided by the user
-}
parseNumber : String -> Int 
parseNumber text =
    let
        theMaybe = toInt text -- used for error handling
    in
        case theMaybe of 
            Just val -> 
                val
            Nothing -> 
                0


update : Messages -> Model -> Model
update msg model =  -- item and value
    let -- used for debugging purposes at the beginning
        logmessage = log "msg" msg
        logmodel = log "model" model
    in
    case msg of -- returning a new model
        Add -> 
            { model | value = model.value + model.numberToAdd }
        ChangedAddText texttyped ->
            { model | numberToAdd = parseNumber texttyped }
        IncrementByTen -> 
            { model | value = model.value + 10 }
        Reset -> 
            { model | value = 0 }
        InputTextReversed txt -> 
            { model | textString = txt}
        Name name -> 
            { model | name = name}
        Password pass -> 
            { model | password = pass }
        PasswordAgain pass -> 
            { model | passwordAgain = pass}
        InputTemperature temp ->
            { model | temperature = temp }

{-
    View function, tells Elm how to display stuff 
    view : model -> virtual DOM
        has a list of attributes and list of contents
        e.g. div [<attributes>] [<content1> ... <contentk>]
    Messages generated go to the update function
-}
view : Model -> Html Messages
view model = 
    div [] 
        [ viewIncrement model -- Incrementing numbers and reset
        , viewReverse model   -- Reverse a string and show length 
        , div [] 
            [ viewInput "text" "Name" model.name Name
            , viewInput "password" "Password" model.password Password
            , viewInput "password" "Confirm Password" model.passwordAgain PasswordAgain
            , viewValidation model
            ]
        , viewConverter model
        ] 


viewIncrement : Model -> Html Messages
viewIncrement model = 
    div [] 
        [ text (fromInt model.value)
        , text "\n"
        , div [] []
        , input [ onInput ChangedAddText ] [] -- generate Msg when enters
        , button [ onClick Add ] [ text "Add" ]  -- generate Msg when clicks
        , button [ onClick IncrementByTen ] [ text "Increment by 10" ]
        , button [ onClick Reset ] [ text "Reset" ]
        , br [] []
        , hr [] []
        ]


viewReverse : Model -> Html Messages
viewReverse model = 
    div [] 
        [ input [ placeholder "Text to reverse"
                , value model.textString
                , onInput InputTextReversed 
                ] []
        , div [] [ text (String.reverse model.textString) ]
        , div [] [ text ( "Length: " ++ String.fromInt (String.length  model.textString)) ]
        , br [] [] 
        , hr [] []
        ]


viewConverter : Model -> Html Messages
viewConverter model = 
    case String.toFloat model.temperature of 
        Just celsius ->
            viewTempConverter model.temperature "blue" (String.fromFloat (celsius * 1.8 + 32))
        Nothing ->
            viewTempConverter model.temperature "red" "???"


viewTempConverter : String -> String -> String -> Html Messages
viewTempConverter temperature color farenheit = 
    span []
        [ br [] []
        , br [] []
        , input [ value temperature, onInput InputTemperature, style "width" "40px"] []
        , text "°C = "
        , span [ style "color" color ] [text farenheit]
        , text "°F"
        ]

viewValidation : Model -> Html msg
viewValidation model = 
    let
        status = passwordValidation model.password model.passwordAgain
    in
    case status of 
        OK -> 
            div [ style "color" "green" ] [ text "OK!" ]
        TooShort -> 
            div [ style "color" "red" ] [ text "Password too short. Min 9 chars" ]
        NotMatching ->
            div [ style "color" "red" ] [text "Passwords do not match!" ]


passwordValidation : String -> String -> PasswordStatus
passwordValidation password passwordAgain = 
    if (password == passwordAgain) && 
       ((String.length password) > 8) then
        OK
    else if (String.length password) <= 8 then
        TooShort
    else
        NotMatching


viewInput : String -> String -> String -> (String -> msg) -> Html msg
viewInput t p v toMsg = 
    input [ type_ t, placeholder p, value v, onInput toMsg] []