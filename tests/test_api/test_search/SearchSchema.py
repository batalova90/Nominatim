from typing import List

from pydantic import BaseModel, validator

from Data.places import places
from tests.src.enum_api import EnumMessagesError


class GeocodingData(BaseModel):
    version: str
    attribution: str
    licence: str
    query: str

    @validator('licence')
    def validator_licence(cls, licence):
        assert licence == "ODbL", EnumMessagesError.LICENCE_WRONG.value
        return licence

    @validator('query')
    def validator_place(cls, query):
        query_list = query.split(', ')
        keys = ["name", "city", "region", "country"]
        query_dict = dict(zip(keys, query_list))
        for key, value in query_dict.items():
            # убрать [0]!!!
            assert value == places[0][key], EnumMessagesError.INVALID_QUERY.value
        return query


class PropertiesGeocodingData(BaseModel):
    place_id: int
    osm_type: str
    osm_id: int
    osm_key: str
    osm_value: str
    type: str
    label: str
    name: str

    @validator('place_id')
    def validator_place_id(cls, place_id):
        assert place_id == places[0]["place_id"], EnumMessagesError.INVALID_ID.value
        return place_id


class GeometryData(BaseModel):
    type: str
    coordinates: List[float]

    @validator('type')
    def validator_type(cls, type):
        if type != "Point":
            raise ValueError(EnumMessagesError.INVALID_TYPE.value)
        return type

    @validator('coordinates')
    def validator_coordinates(cls, coordinates):
        latitude = coordinates[1]
        longitude = coordinates[0]
        assert latitude == places[0]["latitude"], EnumMessagesError.INVALID_COORDINATES.value
        assert longitude == places[0]["longitude"], EnumMessagesError.INVALID_COORDINATES.value

