from .ReverseSchema import GeocodingDataReverse


def test_status_code_reverse(reverse_fixture):
    reverse_fixture.assert_status_code(200)


def test_geocoding_data_reverse(reverse_fixture):
    reverse_fixture.validate_geocoding_data(GeocodingDataReverse)
