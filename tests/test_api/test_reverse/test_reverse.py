import pytest

from .ReverseSchema import GeocodingDataReverse, PropertiesGeocodingDataReverse
from ..test_search.SearchSchema import GeometryData
from tests.src.enum_api import EnumAPI


def test_status_code_reverse(reverse_fixture):
    reverse_fixture.assert_status_code(200)


def test_geocoding_data_reverse(reverse_fixture):
    reverse_fixture.validate_geocoding_data(GeocodingDataReverse)


def test_properties_geocoding_data_reverse(reverse_fixture):
    reverse_fixture.validate_properties_geocoding_data(PropertiesGeocodingDataReverse)


def test_geometry_data_reverse(reverse_fixture):
    reverse_fixture.validate_geometry_data(GeometryData)


@pytest.mark.parametrize("zoom",
                         ['3', '6', '8', '12', '14', '18'])
def test_zoom_reverse(reverse_fixture, zoom):
    reverse_fixture.set_response_json(EnumAPI.REVERSE_ZOOM.value, zoom)
    reverse_fixture.validate_zoom(zoom)
    reverse_fixture.set_response_json(EnumAPI.REVERSE_JSON.value)
