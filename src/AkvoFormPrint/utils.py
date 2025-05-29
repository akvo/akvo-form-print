def parse_int(val, default_val=None):
    try:
        val = int(float(val))
        return val
    except (TypeError, ValueError):
        return default_val
