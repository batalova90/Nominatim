from typing import List

from pydantic import BaseModel, validator

from tests.test_api.enum_api import EnumMessagesError


"""
Классы для проверки схемы ответа при search-запросе
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

    @validator('licence')
    def validator_licence(cls, licence):
        assert licence == "ODbL", EnumMessagesError.LICENCE_WRONG.value
        return licence


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

    @validator('type')
    def validator_type(cls, type):
        if type != "Point":
            raise ValueError(EnumMessagesError.INVALID_TYPE.value)
        return type
