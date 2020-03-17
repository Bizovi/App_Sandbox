module DesignSystems exposing (..)

{-
    Library mdgriffith/elm-ui implementing a design system
    In order not to write css and be consistend in declaring design
-}
import Element exposing (..)
import Element.Background as Background
import Element.Font as Font
import Element.Border as Border
import Element.Input as Input
import Element.Region as Region

import Bootstrap.Card as Card
import Bootstrap.Card.Block as Block
import Html

import Browser
import Html.Attributes


main = 
    Browser.sandbox 
        { init   = init
        , view   = view
        , update = update
        }

type alias Person = 
    { firstName : String
    , lastName : String
    }

persons : List Person
persons = 
    [ { firstName = "David"
      , lastName  = "Bowie"
      }
    , { firstName = "Florence"
      , lastName  = "Welch"
      }
    ]

type Lunch = 
    Burrito
    | Taco
    | Gyro

type alias Model = 
    { welcome : String
    , message : String
    , username : String
    , password : String
    , agreeTOS : Bool
    , comment : String
    , lunch : Lunch
    , spiciness : Float
    }

init : Model 
init = 
    { welcome = "Cybernetics Done Right"
    , message = "We're experimenting with design Systems"
    , username = ""
    , password = ""
    , agreeTOS = False
    , comment = "Extra hot sauce?\n\n\nYes pls"
    , lunch = Gyro
    , spiciness = 2
    }


type Msg = 
    GreetingConfig
    | TopicChange
    | Update Model

update : Msg -> Model -> Model
update msg model = 
    case msg of
        Update new -> 
            new
        _ -> model


view model = 
    Element.layout  -- turns elements into html
        [ Background.color (rgba 1 1 1 1)
        , Font.color (rgba 0 0 0 1)
        , Font.size 20
        , Font.family
            [ Font.external
                { url = "https://fonts.googleapis.com/css?family=EB+Garamond"
                , name = "EB Garamond"
                }
            , Font.sansSerif
            ]
        ]
    <| Element.column [width (px 800), height shrink, centerX, spacing 36, padding 10]
        [ el [ Region.heading 1
            , centerX
            , Font.size 36
            , centerY
             -- , Font.italic
            ]
                (text model.welcome)
        ,Element.row [ paddingXY 10 5, spacing 90]
            [ el [Font.size 42] (text "[")
            , el [Background.color grey, padding 10, alignLeft] (text "ceva")
            , el [Background.color grey, padding 10] (text "ceva")
            , el [Background.color red,  padding 10] (text "ceva")
            , el [Font.size 42] (text "]")
            ]
        , paragraph 
            [ padding 20, spacing 8
            , Font.wordSpacing 1
            ]
            [ el [ alignLeft, padding 0, Font.size <| 2 * 20 + 2 * 8, spacing 0] 
              (text "T")
            , Element.image 
                [ width (px 250), alignRight]
                { src = "https://scontent-lga3-1.xx.fbcdn.net/v/t1.0-9/s960x960/89783983_118657309737278_5020761814917447680_o.jpg?_nc_cat=110&_nc_sid=110474&_nc_ohc=mwhdQBdCMokAX_XeVkB&_nc_ht=scontent-lga3-1.xx&_nc_tp=7&oh=07364ce1ecf566030179464d4a4ada0a&oe=5E96AA16"
                , description = "Excitement of math"
                }
            , text """his blog is about things I’m passionate about. 
I can hardly imagine myself in a place of narrow specialization 
and the exploration of connections between fields brings me a lot of joy I love writing about economics, machine learning, 
applied mathematics, solving business problems with statistical 
models and operationalizing them."""
            ]
        , Input.radio
            [ spacing 12
            , Background.color grey
            , padding 15
            ]
            { selected = Just model.lunch
            , onChange = \new -> Update { model | lunch = new }
            , label = Input.labelAbove [ Font.size 14, paddingXY 0 12 ] (text "What would you like for lunch?")
            , options =
                [ Input.option Gyro (text "Gyro")
                , Input.option Burrito (text "Burrito")
                , Input.option Taco (text "Taco")
                ]
            }
        , Input.username
            [ spacing 12
            , width shrink
            , below
                (el
                    [ Font.color red
                    , Font.size 14
                    , alignRight
                    , moveDown 6
                    ]
                    (text "This one is wrong")
                )
            ]
            { text = model.username
            , placeholder = Just (Input.placeholder [] (text "username"))
            , onChange = \new -> Update { model | username = new }
            , label = Input.labelAbove [ Font.size 14 ] (text "Username")
            }
        , Input.currentPassword [ spacing 12, width shrink ]
            { text = model.password
            , placeholder = Nothing
            , onChange = \new -> Update { model | password = new }
            , label = Input.labelAbove [ Font.size 14 ] (text "Password")
            , show = False
            }
        , Input.button
            [ Background.color blue
            , Font.color white
            , Border.color darkBlue
            , paddingXY 32 16
            , Border.rounded 3
            , width (px 300)
            ]
            { onPress = Nothing
            , label = Element.text "Place your lunch order!"
            }
        , Input.multiline
            [ height shrink
            , spacing 12

            -- , padding 6
            ]
            { text = model.comment
            , placeholder = Just (Input.placeholder [] (text "Extra hot sauce?\n\n\nYes pls"))
            , onChange = \new -> Update { model | comment = new }
            , label = Input.labelAbove [ Font.size 14 ] (text "Leave a comment!")
            , spellcheck = False
            }
        , Input.checkbox []
            { checked = model.agreeTOS
            , onChange = \new -> Update { model | agreeTOS = new }
            , icon = Input.defaultCheckbox
            , label = Input.labelRight [] (text "Agree to Terms of Service")
            }
        , Input.slider
            [ Element.height (Element.px 30)
            , Element.behindContent
                (Element.el
                    [ Element.width Element.fill
                    , Element.height (Element.px 2)
                    , Element.centerY
                    , Background.color grey
                    , Border.rounded 2
                    ]
                    Element.none
                )
            ]
            { onChange = \new -> Update { model | spiciness = new }
            , label = Input.labelAbove [] (text ("Spiciness: " ++ String.fromFloat model.spiciness))
            , min = 0
            , max = 3.2
            , step = Nothing
            , value = model.spiciness
            , thumb =
                Input.defaultThumb
            }
        , Input.slider
            [ Element.width (Element.px 40)
            , Element.height (Element.px 200)
            , Element.behindContent
                (Element.el
                    [ Element.height Element.fill
                    , Element.width (Element.px 2)
                    , Element.centerX
                    , Background.color grey
                    , Border.rounded 2
                    ]
                    Element.none
                )
            ]
            { onChange = \new -> Update { model | spiciness = new }
            , label = Input.labelAbove [] (text ("Spiciness: " ++ String.fromFloat model.spiciness))
            , min = 0
            , max = 3.2
            , step = Nothing
            , value = model.spiciness
            , thumb =
                Input.defaultThumb
            }
        , Element.table
            [ Element.centerX
            , Element.centerY
            , Element.spacing 5
            , Element.padding 10
            ]
            { data = persons
            , columns = 
                [ { header = Element.text "First Name"
                , width = px 200
                , view = \person -> Element.text person.firstName
                }
                , { header = Element.text "Last Name"
                , width = fill
                , view = \person -> Element.text person.lastName
                }
                ]
            }
        , Element.row [] 
            [
            Element.html
            (Html.div [] 
                [ Card.config [ Card.outlineInfo ]
                    |> Card.headerH1 [] [ Html.text "My Card Info" ]
                    |> Card.footer [] [ Html.text "Some footer" ]
                    |> Card.block []
                        [ Block.titleH1 [] [ Html.text "Block title" ]
                        , Block.text [] [ Html.text "Some block content" ]
                        , Block.link [ Html.Attributes.href "#" ] [ Html.text "MyLink" ]
                        ]
                    |> Card.view
                ])
            , text "Some custom HTML At the left"
            ]
            
        ]

white : Color
white = Element.rgb 1 1 1

grey : Color
grey = Element.rgb 0.9 0.9 0.9

blue : Color
blue = Element.rgb 0 0 0.8

red : Color
red = Element.rgb 0.8 0 0

darkBlue : Color
darkBlue = Element.rgb 0 0 0.9