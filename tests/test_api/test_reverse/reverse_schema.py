from typing import Dict

from pydantic import BaseModel, validator, ValidationError

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

    @validator('licence')
    def validator_licence(cls, licence):
        assert licence == "ODbL", EnumMessagesError.LICENCE_WRONG.value


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

