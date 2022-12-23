import enum


class EnumAPI(enum.Enum):
    GEOCODE_JSON = "https://nominatim.openstreetmap.org/search?q=%CE%91%CE%B3%CE%AF%CE%B1+%CE%A4%CF%81%CE%B9%CE%AC%CE%B4%CE%B1%2C+%CE%91%CE%B4%CF%89%CE%BD%CE%B9%CE%B4%CE%BF%CF%82%2C+Athens%2C+Greece&format=geocodejson"
    REVERSE_JSON = "https://nominatim.openstreetmap.org/reverse?format=geocodejson&lat=38.005169699999996&lon=23.72949633941048"


class EnumMessagesError(enum.Enum):
    NOT_200 = "Status code is not 200"
    LICENCE_WRONG = "Invalid license type"
    INVALID_QUERY = "Object data doesn't match"
    INVALID_ID = "Invalid place id"
    INVALID_TYPE = "Type must be a Point"
    INVALID_COORDINATES = "Invalid Coordinates"
    INVALID_NAME = "Invalid name object"
