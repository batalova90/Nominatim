GetSearchSchema = {
    "type": "object",
    "properties": {
        "type": {"type": "string"},
    },
    "additionalProperties": {
        "type": "object",
        "required": [
            "version",
            "atribute",
            "lecence",
            "query"
        ],
        "properties": {
            "version": {
                "type": "string"
            },
            "atribute": {
                "type": "string",
            },
            "lecence": {
                "type": "string",
            },
            "query": {
                "type": "string"
            }
        },

        "features": {"type": "list"},
        "geometry": {"type": "dictionary"}
    },
    #"required": ["geometry"]
}


class GetSearch(BaseModel):
    #type: str
    geocoding: Dict[str, str]








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