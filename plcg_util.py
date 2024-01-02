def log_msg(msg: str):
    print(f"[PLCG]: {msg}")


def try_cast_integer(val: str) -> (bool, int):
    out = 0
    try:
        out = int(val)
    except ValueError:
        if len(val) == 0:
            return False, 0
        return False, 0
    return True, out


def clear_plcg_rgba_buffer(width, height):
    return [(0, 0, 0, 0)] * (width * height)
