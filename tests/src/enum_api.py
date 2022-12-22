import enum


class EnumAPI(enum.Enum):
    GEOCODE_JSON= "https://nominatim.openstreetmap.org/search?q=%CE%91%CE%B3%CE%AF%CE%B1+%CE%A4%CF%81%CE%B9%CE%AC%CE%B4%CE%B1%2C+%CE%91%CE%B4%CF%89%CE%BD%CE%B9%CE%B4%CE%BF%CF%82%2C+Athens%2C+Greece&format=geocodejson"


class EnumMessagesError(enum.Enum):
    NOT_200 = "Status code is not 200"
