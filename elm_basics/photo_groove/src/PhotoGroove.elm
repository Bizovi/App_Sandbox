module PhotoGroove exposing (main)

import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (onClick)

import Array exposing (Array)
import Random

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
    , chosenSize : ThumbnailSize
    }

type ThumbnailSize
    = Small
    | Medium
    | Large

type Msg 
    = ClickedPhoto String
    | ClickedSize ThumbnailSize
    | ClickedSurpriseMe 
    | GotSelectedIndex Int


-- define the initial model (describing state by records)
initialModel : Model
initialModel = 
    { photos = 
        [ { url = "1.jpeg" }
        , { url = "2.jpeg" }
        , { url = "3.jpeg" }
        ]
    , selectedUrl = "2.jpeg"
    , chosenSize = Large
    }

-- need an array to be able to access elements
photoArray : Array Photo
photoArray = 
    Array.fromList initialModel.photos

-- helper to get the photo url from index
getPhotoUrl : Int -> String
getPhotoUrl index = 
    case Array.get index photoArray of 
        -- cover all possible values of maybe (Just, Nothing)
        Just photo ->  -- Just : smth -> Maybe smth (<= 1 element)
            photo.url
        
        Nothing ->
            ""

randomPhotoPicker : Random.Generator Int
randomPhotoPicker =
    Random.int 0 (Array.length photoArray - 1)


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model = 
    {- Expected message is in the following format
       msg.description = "ClickedPhoto"
     , msg.data = "2.jpeg"
    -}
    case msg of 
        GotSelectedIndex index -> 
            ( { model | selectedUrl = getPhotoUrl index }, Cmd.none )

        ClickedPhoto url ->
            ( { model | selectedUrl = url }, Cmd.none )
        
        ClickedSize size ->
            ( { model | chosenSize = size }, Cmd.none )
        
        ClickedSurpriseMe ->
            ( model, Random.generate GotSelectedIndex randomPhotoPicker )


view : Model -> Html Msg
view model = 
    {- Function to render the HTML for the app
    * model - the current state
    -}
    div [ class "content" ]
        [ h1 [ align "center" ] [ text "Photo Groove" ]
        , br [] []
        -- add button for choosing the size of thumbnail
        , button [ onClick ClickedSurpriseMe ] 
            [ text "Surprise Me!" ]
        -- end of buttons
        -- radio buttons for thumbnail size
        , h3 [] [ text "Thumbnail Size:" ]
        , div [ id "choose-size" ] 
            (List.map viewSizeChooser [ Small, Medium, Large ])
        -- end of radio buttons
        , div [ id "thumbnails", align "left", class (sizeToString model.chosenSize) ] 
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
        , onClick (ClickedPhoto thumb.url)
        ] []


viewSizeChooser : ThumbnailSize -> Html Msg
viewSizeChooser size = 
    label []
        [ input [ type_ "radio"
                , name "size"
                , onClick (ClickedSize size) 
                ] []
        , text (sizeToString size)
        ]

sizeToString : ThumbnailSize -> String
sizeToString size = 
    case size of 
        Small ->
            "small"
        Medium -> 
            "med"
        Large ->
            "large"


main : Program () Model Msg  -- () is an unit
main = 
    Browser.element
        { init = \flags -> ( initialModel, Cmd.none )
        , view = view
        , update = update
        , subscriptions = \model -> Sub.none
        }
        