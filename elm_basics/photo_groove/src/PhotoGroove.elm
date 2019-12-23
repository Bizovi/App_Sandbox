module PhotoGroove exposing (main)

import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (onClick)

import Array exposing (Array)
import Random
import Http

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

type Status
    = Loading
    | Loaded (List Photo) String
    | Errored String

type ThumbnailSize
    = Small
    | Medium
    | Large

type alias Model = 
    { status : Status
    , chosenSize : ThumbnailSize
    }

type Msg 
    = ClickedPhoto String
    | ClickedSize ThumbnailSize
    | ClickedSurpriseMe 
    | GotRandomPhoto Photo
    | GotPhotos (Result Http.Error String)


-- define the initial model (describing state by records)
initialModel : Model
initialModel = 
    { status = Loading
    , chosenSize = Medium
    }


initialCmd : Cmd Msg
initialCmd = 
    Http.get
        { url = "http://elm-in-action.com/photos/list"
        , expect = Http.expectString GotPhotos
        }



update : Msg -> Model -> ( Model, Cmd Msg )
update msg model = 
    {- Expected message is in the following format
       msg.description = "ClickedPhoto"
     , msg.data = "2.jpeg"
    -}
    case msg of 
        GotRandomPhoto photo -> 
            ( { model | status = selectUrl photo.url model.status }
            , Cmd.none 
            )

        ClickedPhoto url ->
            ( { model | status = selectUrl url model.status }
            , Cmd.none 
            )
        
        ClickedSize size ->
            ( { model | chosenSize = size }, Cmd.none )
        
        ClickedSurpriseMe ->
            case model.status of 
                Loaded (firstPhoto :: otherPhotos) _ ->
                    Random.uniform firstPhoto otherPhotos
                        |> Random.generate GotRandomPhoto
                        |> Tuple.pair model
                
                Loaded [] _ ->
                    ( model, Cmd.none )
                
                Loading ->
                    ( model, Cmd.none )
                
                Errored errorMessage -> 
                    ( model, Cmd.none )
        
        GotPhotos result ->
            case result of
                Ok responseStr -> 
                    case String.split "," responseStr of
                        (firstUrl :: _) as urls ->
                            let 
                                photos = 
                                    List.map Photo urls
                            in 
                            ( { model | status = Loaded photos firstUrl }, Cmd.none )
                        
                        [] ->
                            ( { model | status = Errored "0 photos found" }, Cmd.none)
                
                Err httpError -> 
                    ( { model | status = Errored "Server Errorr!" }, Cmd.none )


selectUrl : String -> Status -> Status
selectUrl url status = 
    case status of
        Loaded photos _ ->
            Loaded photos url
        
        Loading -> 
            status
        
        Errored errorMessage -> 
            status

view : Model -> Html Msg
view model = 
    {- Function to render the HTML for the app
    * model - the current state
    -}
    div [ class "content" ] <|
        case model.status of 
            Loaded photos selectedUrl ->
                viewLoaded photos selectedUrl model.chosenSize
            
            Loading ->
                []

            Errored errorMessage ->
                [ text ("Error: " ++ errorMessage) ]
        

viewLoaded : List Photo -> String -> ThumbnailSize -> List (Html Msg)
viewLoaded photos selectedUrl chosenSize =
    [ h1 [] [ text "Photo Groove" ]
    , button [ onClick ClickedSurpriseMe ] [ text "Surprise Me!" ]
    , h3 [] [ text "Thumbnail Size" ]
    , div [ id "choose-size" ]
        (List.map viewSizeChooser [ Small, Medium, Large ])
    , div [ id "thumbnails"
          , class (sizeToString chosenSize)
          ] 
        (List.map (viewThumbnail selectedUrl) photos)
    , img [ class "large"
          , src (urlPrefix ++ "large/" ++ selectedUrl)
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
        { init = \flags -> ( initialModel, initialCmd )
        , view = view
        , update = update
        , subscriptions = \model -> Sub.none
        }
