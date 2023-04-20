from voluptuous import Schema, PREVENT_EXTRA

user_schema = Schema(
    {
        "id": int,
        "token": str
    },
    extra=PREVENT_EXTRA,
    required=True
)
