from tests.src.enum_api import EnumMessagesError


class Search:
    def __init__(self, response):
        self.response = response
        self.response_json = response.json()
        self.status_code = response.status_code

    def validate_geocoding_data(self, schema):
        schema.parse_obj(self.response_json['geocoding'])

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

    def assert_status_code(self, status_code):
        assert self.status_code == status_code, EnumMessagesError.NOT_200.value
