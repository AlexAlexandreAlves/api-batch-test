PEOPLE_ITEM_SCHEMA = {
    "type": "object",
    "required": ["name", "height", "mass", "hair_color", "skin_color", "eye_color", "birth_year", "gender", "homeworld", "films", "species", "vehicles", "starships", "created", "edited", "url"],
    "properties": {
        "name": {"type": "string", "minLength": 1},
        "height": {"type": "string"},
        "mass": {"type": "string"},
        "hair_color": {"type": "string"},
        "skin_color": {"type": "string"},
        "eye_color": {"type": "string"},
        "birth_year": {"type": "string"},
        "gender": {"type": "string"},
        "homeworld": {"type": "string", "pattern": "^https?://"},
        "films": {
            "type": "array",
            "items": {"type": "string", "pattern": "^https?://"}
        },
        "species": {
            "type": "array",
            "items": {"type": "string", "pattern": "^https?://"}
        },
        "vehicles": {
            "type": "array",
            "items": {"type": "string", "pattern": "^https?://"}
        },
        "starships": {
            "type": "array",
            "items": {"type": "string", "pattern": "^https?://"}
        },
        "created": {"type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}T"},
        "edited": {"type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}T"},
        "url": {"type": "string", "pattern": "^https?://"},
    },
    "additionalProperties": False,
}