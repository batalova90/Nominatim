from .SearchSchema import GeocodingData, PropertiesGeocodingData, GeometryData


def test_status_code_search(search_fixture):
    search_fixture.assert_status_code(200)


def test_geocoding_data_search(search_fixture):
    search_fixture.validate_geocoding_data(GeocodingData)


def test_properties_geocoding_data_search(search_fixture):
    search_fixture.validate_properties_geocoding_data(PropertiesGeocodingData)


def test_geometry_data_search(search_fixture):
    search_fixture.validate_geometry_data(GeometryData)

