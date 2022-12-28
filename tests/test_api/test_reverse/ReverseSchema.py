from typing import Dict

from pydantic import BaseModel, validator

from Data.places import places
from tests.test_api.enum_api import EnumMessagesError


class GeocodingDataReverse(BaseModel):
    """
    Пример возврата json-схемы по ключу 'geocoding':
    "geocoding": {
        "version": "0.1.0",
        "attribution": "Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright",
        "licence": "ODbL",
       "query": "38.0051697,23.72949633941"
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

    @classmethod
    @validator('query')
    def validator_query(cls, query):
        latitude = float(query.split(',')[0]) - places[0]["latitude"]
        longitude = float(query.split(',')[1]) - places[0]["longitude"]
        assert longitude < 10**-6, EnumMessagesError.INVALID_COORDINATES.value
        assert latitude < 10**-6, EnumMessagesError.INVALID_COORDINATES.value


class PropertiesGeocodingDataReverse(BaseModel):
    """
        Пример возврата json-схемы по ключам:
        'features'-> 'properties' ->'geocoding'.
        "properties": {
        "geocoding": {
             "place_id": 123941922,
                    "osm_type": "way",
                    "osm_id": 82214001,
                    "type": "house",
                    "accuracy": 0,
                    "label": "Αγία Τριάδα, ...",
                    "name": "Αγία Τριάδα",
                    "country": "Ελλάς",
                    "postcode": "112 53",
                    "state": "Αποκεντρωμένη Διοίκηση Αττικής",
                    "county": "Περιφερειακή Ενότητα Κεντρικού Τομέα Αθηνών",
                    "city": "Αθήνα",
                    ...
            }
        }
    """

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
        assert street == places[0]["city"], EnumMessagesError.INVALID_STREET.value
        return street
