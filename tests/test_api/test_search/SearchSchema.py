from pydantic import BaseModel, Field
from typing import Dict, List, Optional


class GetSearch(BaseModel):
    #type: str
    geocoding: Dict[str, str]
    #features: List[Dict[str, str]]







    """""
    type: str
    geocoding: dict(
        {
            "version": str,
            "attribution": str,
            "licence": str,
            "query": str,
        })
    features: list[
        dict[{
            "type": str,
            "properties": dict({
                "geocoding": dict({
                    "place_id": int,
                    "osm_type": str,
                    "osm_id": int,
                    "osm_key": str,
                    "osm_value": str,
                    "type": str,
                    "label": str,
                    "name": str,
                })
            }),
            "geometry": dict({
                "type": str,
                "coordinates": list([
                    int,
                    int
                ])
            })
        }]
    ]
"""""