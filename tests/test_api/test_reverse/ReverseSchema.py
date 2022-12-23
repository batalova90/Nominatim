from pydantic import BaseModel, validator
from typing import List

from tests.src.enum_api import EnumMessagesError
from Data.places import places


class GeocodingDataReverse(BaseModel):
    version: str
    attribution: str
    licence: str
    query: str

    @classmethod
    @validator('licence')
    def validator_licence(cls, licence):
        assert licence == "ODbL", EnumMessagesError.LICENCE_WRONG.value

    @classmethod
    @validator('query')
    def validator_query(cls, query):
        latitude = float(query.split(',')[0]) - places[0]["latitude"]
        longitude = float(query.split(',')[1]) - places[0]["longitude"]
        assert longitude < 10**-6, EnumMessagesError.INVALID_COORDINATES.value
        assert latitude < 10**-6, EnumMessagesError.INVALID_COORDINATES.value
