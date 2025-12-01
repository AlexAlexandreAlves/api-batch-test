PEOPLE_ITEM_SCHEMA = {
    "type": "object",
    "required": ["name", "url"],
    "properties": {
        "name": {"type": "string", "minLength": 1},
        "url": {"type": "string", "pattern": "^https?://"},
    },
    "additionalProperties": True,
}