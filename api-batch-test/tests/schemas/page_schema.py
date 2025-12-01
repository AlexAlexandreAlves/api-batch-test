PAGE_SCHEMA = {
    "type": "object",
    "required": ["count", "next", "previous", "results"],
    "properties": {
        "count": {"type": "integer", "minimum": 0},
        "next": {"type": ["string", "null"]},
        "previous": {"type": ["string", "null"]},
        "results": {"type": "array"},
    },
    "additionalProperties": True,
}