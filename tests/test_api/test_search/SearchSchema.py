from typing import List

from pydantic import BaseModel, validator

from Data.places import places
from tests.src.enum_api import EnumMessagesError

"""
Классы для проверки возврата схемы ответа при search-запросе
(формат geocodejson)
"""


class GeocodingData(BaseModel):
    """
    Пример возврата json-схемы по ключу 'geocoding':
     "geocoding": {
        "version": "0.1.0",
        "attribution": "Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright",
        "licence": "ODbL",
        "query": "Αγία Τριάδα, Αδωνιδος, Athens, Greece"
    }
    """
    version: str
    attribution: str
    licence: str
    query: str

    @classmethod
    @validator('licence')
    def validator_licence(cls, licence):
        assert licence == "ODbL", EnumMessagesError.LICENCE_WRONG.value
        return licence

    @classmethod
    @validator('query')
    def validator_place(cls, query):
        query_list = query.split(', ')
        keys = ["name", "city", "region", "country"]
        query_dict = dict(zip(keys, query_list))
        for key, value in query_dict.items():
            assert value == places[0][key], EnumMessagesError.INVALID_QUERY.value
        return query


class PropertiesGeocodingData(BaseModel):
    """
    Пример возврата json-схемы по ключам:
    'features'-> 'properties' ->'geocoding'.
    "properties": {
    "geocoding": {
        "place_id": 123941922,
        "osm_type": "way",
        "osm_id": 82214001,
        "osm_key": "amenity",
        "osm_value": "place_of_worship",
        "type": "house",
        "label": "Αγία Τριάδα, ...",
        "name": "Αγία Τριάδα"
        }
    }
    """
    place_id: int
    osm_type: str
    osm_id: int
    osm_key: str
    osm_value: str
    type: str
    label: str
    name: str

    @classmethod
    @validator('place_id')
    def validator_place_id(cls, place_id):
        assert place_id == places[0]["place_id"], EnumMessagesError.INVALID_ID.value
        return place_id


class GeometryData(BaseModel):
    """
    Пример возврата json-схемы по ключам:
    'features'->'geometry'.
    'geometry': {
        "type": "Point",
        "coordinates": [
            23.72949633941048,
            38.005169699999996
            ]
    }
    """
    type: str
    coordinates: List[float]

    @classmethod
    @validator('type')
    def validator_type(cls, type):
        if type != "Point":
            raise ValueError(EnumMessagesError.INVALID_TYPE.value)
        return type

    @classmethod
    @validator('coordinates')
    def validator_coordinates(cls, coordinates):
        latitude = coordinates[1]
        longitude = coordinates[0]
        assert latitude == places[0]["latitude"], EnumMessagesError.INVALID_COORDINATES.value
        assert longitude == places[0]["longitude"], EnumMessagesError.INVALID_COORDINATES.value
        return coordinates
