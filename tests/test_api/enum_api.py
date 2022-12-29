import enum


class EnumAPI(enum.Enum):
    GEOCODE_JSON = "https://nominatim.openstreetmap.org/search?q=%CE%91%CE%B3%CE%AF%CE%B1+%CE%A4%CF%81%CE%B9%CE%AC%CE%B4%CE%B1%2C+%CE%91%CE%B4%CF%89%CE%BD%CE%B9%CE%B4%CE%BF%CF%82%2C+Athens%2C+Greece&format=geocodejson"
    REVERSE_JSON = "https://nominatim.openstreetmap.org/reverse?format=geocodejson&lat=38.005169699999996&lon=23.72949633941048"
    REVERSE_ZOOM = "https://nominatim.openstreetmap.org/reverse?format=geocodejson&lat=56.91231&lon=92.85655&zoom="
    SEARCH_OBJECT = "https://nominatim.openstreetmap.org/?addressdetails=1&q="
    SEARCH_XML = 'https://nominatim.openstreetmap.org/search?format=xml&addressdetails=1&q='
    REVERSE_OBJECT = "https://nominatim.openstreetmap.org/reverse?format=json&lat="
    LOOKUP_JSON = "https://nominatim.openstreetmap.org/lookup?format=json&osm_ids=W"


class EnumMessagesError(enum.Enum):
    NOT_200 = "Status code is not 200"
    LICENCE_WRONG = "Invalid license type"
    INVALID_QUERY = "Object data doesn't match"
    INVALID_ID = "Invalid place id"
    INVALID_TYPE = "Type must be a Point"
    INVALID_COORDINATES = "Invalid Coordinates"
    INVALID_NAME = "Invalid name object"
    INVALID_OSM_ID = "OSM_ID objects search and reverse requests is not equal"
    INVALID_LONGITUDE_LOOKUP = "Invalid longitude"
    INVALID_LATITUDE_LOOKUP = "Invalid latitude"
    INVALID_XML_FORMAT = "Invalid xml-format"
