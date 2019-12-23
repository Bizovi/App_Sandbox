module AddToList exposing (..)

import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)

-- for simple applications
import Browser exposing (sandbox)

main = 
    Browser.sandbox 
    { 
      init = model
    , view = view
    , update = update }


type alias Model = 
    { entries : List String
    , results : List String
    , filter  : String
    }

type Msg
    = Filter String
    | Add

model : Model  -- model function of type model
model = 
    { entries = []
    , results = []
    , filter  = ""
    }

update : Msg -> Model -> Model
update msg model_curr = 
    case msg of 
        Filter filter -> 
            { model_curr
                | results = List.filter (String.contains filter) model_curr.entries
                , filter = filter
            }
        
        Add -> 
            { model 
                | entries = model_curr.filter :: model_curr.entries
                , results = model_curr.filter :: model_curr.results
            }

view : Model -> Html Msg
view model_curr = 
    div []
        [ input [ placeholder "Filter...", onInput Filter ] []
        , button [ onClick Add ] [ text "Add New" ]
        , ul [] (List.map viewEntry model_curr.results)
        ]

viewEntry : String -> Html Msg
viewEntry entry = 
    li [] [ text entry]