import requests

from Data.data_zoom import zoom_label
from tests.test_api.enum_api import EnumMessagesError

"""
    Класс для проверки формата ответа при reverse-запросе.
    (формат json)
"""


class Reverse:
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

    def assert_status_code(self, status_code):
        """
        Проверка статуса кода ответа сервера
        """
        assert self.status_code == status_code,\
            EnumMessagesError.NOT_200.value

    def validate_properties_geocoding_data(self, schema):
        """
        Проверка формата ответа по ключам:
        'features'-> 'properties' ->'geocoding'.
        Валидация полей: 'place_id', 'name', 'street' и т.д.
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
            schema.parse_obj(self.response_json['features']['geometry'])
        return schema

    def set_response_json(self, url_default, zoom=None):
        """
        Метод для изменения поля класса
        self.response.json
        """
        if zoom is None:
            self.response_json = self.response.json()
        else:
            get_url = url_default + zoom
            self.response_json = requests.get(
                get_url
            ).json()

    def validate_zoom(self, zoom):
        """
        Проверка отображения поля
        label при изменении параметра zoom в запросе
        """
        label_answer = self.response_json['features'][0]['properties']['geocoding']['label']
        assert label_answer == zoom_label[zoom]
