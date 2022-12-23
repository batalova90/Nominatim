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
