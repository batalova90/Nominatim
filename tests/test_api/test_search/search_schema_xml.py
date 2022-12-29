from typing import Optional

import pydantic_xml as pxml
import pydantic


class Place(pxml.BaseXmlModel, tag="place"):
    house_number: int = pxml.element()
    road: str = pxml.element()
    hamlet: str = pxml.element()
    town: str = pxml.element()
    village: str = pxml.element()
    city: str = pxml.element()
    ISO3166_lvl18: Optional[str] = pxml.element(tag="ISO3166-2-lvl8")
    state_district: str = pxml.element()
    state: str = pxml.element()
    ISO3166_lvl14: Optional[str] = pxml.element(tag="ISO3166-2-lvl4")
    postcode: str = pxml.element()
    country: str = pxml.element()
    country_code: str = pxml.element()


class SearchResultsXML(pxml.BaseXmlModel, tag="searchresults"):
    place: Place = pxml.element(tag='place')
