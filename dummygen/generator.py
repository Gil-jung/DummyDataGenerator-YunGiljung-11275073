DEFAULT_MIN = 0
DEFAULT_MAX = 1000


def generate_number(field_schema: dict, rng):
    options = field_schema.get("x-generator", {})
    minimum = options.get("min", DEFAULT_MIN)
    maximum = options.get("max", DEFAULT_MAX)

    if field_schema.get("type") == "integer":
        return rng.randint(int(minimum), int(maximum))
    return rng.uniform(float(minimum), float(maximum))
