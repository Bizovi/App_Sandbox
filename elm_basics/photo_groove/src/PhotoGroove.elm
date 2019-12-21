module PhotoGroove exposing (main)

import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (onClick)
import Array exposing (Array)

import Browser

-- the base url for images
urlPrefix : String
urlPrefix = 
    "http://elm-in-action.com/"


{- Defining the types for:
* Model
* View
* Records
-}
type alias Photo = 
    { url : String }

type alias Model = 
    { photos : List Photo
    , selectedUrl : String
    }

type alias Msg = 
    { description : String, data: String }


-- define the initial model (describing state by records)
initialModel : Model
initialModel = 
    { photos = 
        [ { url = "1.jpeg" }
        , { url = "2.jpeg" }
        , { url = "3.jpeg" }
        ]
    , selectedUrl = "2.jpeg"
    }

photoArray : Array Photo
photoArray = 
    Array.fromList initialModel.photos


update : Msg -> Model -> Model
update msg model = 
    {- Expected message is in the following format
       msg.description = "ClickedPhoto"
     , msg.data = "2.jpeg"
    -}
    if msg.description == "ClickedPhoto" then
        { model | selectedUrl = msg.data }
    else
        model -- whatever happens, should return a new model


view : Model -> Html Msg
view model = 
    {- Function to render the HTML for the app
    * model - the current state
    -}
    div [ class "content" ]
        [ h1 [ align "center" ] [ text "Photo Groove" ]
        , br [] []
        , div [ id "thumbnails", align "center"] 
            -- the following works because of partial application of function
            -- (\photo -> vT model.selectedUrl photo)
            ( List.map (viewThumbnail model.selectedUrl) model.photos )
        , img
            [ class "large"
            , src (urlPrefix ++ "large/" ++ model.selectedUrl)
            ] []    
        ]


viewThumbnail : String -> Photo -> Html Msg
viewThumbnail selectedUrl thumb = 
    {- Helper function to render the images and send the message
    Notice the currying happening ...
    * selectedUrl (current selection)
    * thumb - a given thumbnail
    -}
    img 
        [ src (urlPrefix ++ thumb.url) 
        , classList [ ( "selected", selectedUrl == thumb.url ) ]
        , onClick { description = "ClickedPhoto", data = thumb.url }
        ] []


main = 
    Browser.sandbox
        { init = initialModel
        , view = view
        , update = update
        }
