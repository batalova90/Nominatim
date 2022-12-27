from tests.src.enum_api import EnumMessagesError


"""
    Класс для проверки формата ответа при search-запросе.
    Формат - geocodejson
"""


class Search:
    def __init__(self, response):
        self.response = response
        self.response_json = response.json()
        self.status_code = response.status_code

    def validate_geocoding_data(self, schema):
        """
        Проверка формата ответа по ключу 'geocoding'.
        Валидация полей: 'licence', 'query'.
        """
        schema.parse_obj(self.response_json['geocoding'])
        return schema

    def validate_properties_geocoding_data(self, schema):
        """
         Проверка формата ответа по ключам:
         'features'-> 'properties' ->'geocoding'.
         Валидация полей: 'place_id', 'name', 'label' и т.д.
        """
        if isinstance(self.response_json['features'], list):
            for features in self.response_json['features']:
                schema.parse_obj(features['properties']['geocoding'])
        else:
            schema.parse_obj(
                self.response_json['features']['properties']['geocoding']
            )
        return schema

    def validate_geometry_data(self, schema):
        """
        Проверка формата ответа по ключам:
        'features'->'geometry'.
        Валидация полей: 'type', 'coordinates'.
        """
        if isinstance(self.response_json['features'], list):
            for features in self.response_json['features']:
                schema.parse_obj(features['geometry'])
        else:
            schema.parse_obj(
                self.response_json['features']['geometry']
            )
        return schema

    def assert_status_code(self, status_code):
        """
        Проверка статуса кода ответа сервера
        """
        assert self.status_code == status_code,\
            EnumMessagesError.NOT_200.value

    @staticmethod
    def get_osm_id(response_search_json, coordinates):
        """
        Получение osm_id и координат объекта
        """
        coordinates.append(response_search_json["lat"])
        coordinates.append(response_search_json["lon"])
        return response_search_json["osm_id"]
