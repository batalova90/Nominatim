import requests

from Data.data_zoom import zoom_label
from tests.src.enum_api import EnumMessagesError


class Reverse:
    def __init__(self, response):
        self.response = response
        self.response_json = response.json()
        self.status_code = response.status_code

    def validate_geocoding_data(self, schema):
        schema.parse_obj(self.response_json['geocoding'])

    def assert_status_code(self, status_code):
        assert self.status_code == status_code, EnumMessagesError.NOT_200.value

    def validate_properties_geocoding_data(self, schema):
        if isinstance(self.response_json['features'], list):
            for features in self.response_json['features']:
                schema.parse_obj(features['properties']['geocoding'])
        else:
            schema.parse_obj(self.response_json['features']['properties']['geocoding'])
        return schema

    def validate_geometry_data(self, schema):
        if isinstance(self.response_json['features'], list):
            for features in self.response_json['features']:
                schema.parse_obj(features['geometry'])
        else:
            schema.parse_obj(self.response_json['features']['geometry'])
        return schema

    def set_response_json(self, url_default, zoom=None):
        if zoom is None:
            self.response_json = self.response.json()
        else:
            get_url = url_default + zoom
            self.response_json = requests.get(get_url).json()

    def validate_zoom(self, zoom):
        label_answer = self.response_json['features'][0]['properties']['geocoding']['label']
        assert label_answer == zoom_label[zoom]

