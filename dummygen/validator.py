from dummygen.generator import _evaluate_sum_formula


def validate_consistency(record: dict, schema: dict) -> list:
    errors = []
    _check(record, schema, record, "", errors)
    return errors


def _check(node, schema, root, path, errors):
    field_type = schema.get("type")

    if field_type == "object":
        for name, sub_schema in schema.get("properties", {}).items():
            sub_path = f"{path}.{name}" if path else name
            options = sub_schema.get("x-generator", {})
            if "derivedFrom" in options:
                source = root.get(options["derivedFrom"], [])
                expected = _evaluate_sum_formula(source, options["formula"])
                actual = node.get(name)
                if actual != expected:
                    errors.append(f"{sub_path}: expected {expected}, got {actual}")
            else:
                _check(node[name], sub_schema, root, sub_path, errors)
    elif field_type == "array":
        item_schema = schema.get("items", {})
        for index, item in enumerate(node):
            _check(item, item_schema, root, f"{path}[{index}]", errors)
