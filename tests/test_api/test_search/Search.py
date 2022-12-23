from tests.src.enum_api import EnumAPI, EnumMessagesError


class Search:
    def __init__(self, response):
        self.response = response
        self.response_json = response.json()
        self.status_code = response.status_code

    def validate(self, schema):
        schema.parse_obj(self.response_json['geocoding'])
        return schema
    def assert_status_code(self, status_code):
        assert self.status_code == status_code, EnumMessagesError.NOT_200.value
