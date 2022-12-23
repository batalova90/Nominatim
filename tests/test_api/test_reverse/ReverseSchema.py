from pydantic import BaseModel, validator
from typing import List, Dict

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


class PropertiesGeocodingDataReverse(BaseModel):
    place_id: str
    osm_type: str
    osm_id: int
    type: str
    accuracy: int
    label: str
    name: str
    country: str
    postcode: str
    state: str
    country: str
    city: str
    district: str
    locality: str
    street: str
    admin: Dict[str, str]


    @classmethod
    @validator('place_id')
    def validator_place_id(cls, place_id):
        assert place_id == places[0]["place_id"], EnumMessagesError.INVALID_ID.value
        return place_id

    @classmethod
    @validator('name')
    def validator_name(cls, name):
        assert name == places[0]["name"], EnumMessagesError.INVALID_NAME.value
        return name

    @classmethod
    @validator('street')
    def validator_street(cls, street):
        assert street == places[0]["city"], EnumMessagesError.INVALID_STREET
        return street



