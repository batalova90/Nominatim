from .ReverseSchema import GeocodingDataReverse, PropertiesGeocodingDataReverse
from ..test_search.SearchSchema import GeometryData



def test_status_code_reverse(reverse_fixture):
    reverse_fixture.assert_status_code(200)


def test_geocoding_data_reverse(reverse_fixture):
    reverse_fixture.validate_geocoding_data(GeocodingDataReverse)


def test_properties_geocoding_data_reverse(reverse_fixture):
    reverse_fixture.validate_properties_geocoding_data(PropertiesGeocodingDataReverse)


def test_geometry_data_reverse(reverse_fixture):
    reverse_fixture.validate_geometry_data(GeometryData)
