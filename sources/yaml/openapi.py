def get_value(data, path):
    keys = path.split("/")
    for key in keys:
        if isinstance(data, dict) and key in data:
            data = data[key]
        else:
            return None
    return data

def resolve_refs(data, root=None):
    if root is None:
        root = data

    if isinstance(data, dict):
        for key, value in list(data.items()):
            if key == "$ref" and isinstance(value, str):
                resolved_value = get_value(root, value.lstrip('#'))
                if resolved_value is not None:
                    return resolved_value
            else:
                data[key] = resolve_refs(value, root)

    elif isinstance(data, list):
        for i in range(len(data)):
            data[i] = resolve_refs(data[i], root)

    return data