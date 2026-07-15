import string

DEFAULT_MIN = 0
DEFAULT_MAX = 1000
DEFAULT_STRING_LENGTH = 8


def generate_number(field_schema: dict, rng):
    options = field_schema.get("x-generator", {})
    minimum = options.get("min", DEFAULT_MIN)
    maximum = options.get("max", DEFAULT_MAX)

    if field_schema.get("type") == "integer":
        return rng.randint(int(minimum), int(maximum))
    return rng.uniform(float(minimum), float(maximum))


def generate_string(field_schema: dict, rng, seq: int = 0) -> str:
    options = field_schema.get("x-generator", {})

    if "pattern" in options:
        return options["pattern"].format(seq=seq)

    if "choices" in options:
        return rng.choice(options["choices"])

    alphabet = string.ascii_letters + string.digits
    return "".join(rng.choice(alphabet) for _ in range(DEFAULT_STRING_LENGTH))


def generate_boolean(field_schema: dict, rng) -> bool:
    options = field_schema.get("x-generator", {})
    true_ratio = options.get("true_ratio", 0.5)
    return rng.random() < true_ratio
