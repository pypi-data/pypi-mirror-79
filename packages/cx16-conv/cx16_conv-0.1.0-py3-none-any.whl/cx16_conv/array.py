from .util import chunks


def convert(format_: str, symbol_name: str, bytes_: bytes) -> str:
    if format_ == "C-array":
        return bytes_to_c_array(symbol_name, bytes_)
    raise NotImplementedError(format_)


def bytes_to_c_array(symbol_name: str, bytes_: bytes) -> str:
    value = f"uint8_t {symbol_name}[{len(bytes_)}] = " + "{\n"
    for substring in chunks(bytes_, 16):
        value += "    "
        for byte in substring:
            value += f"{hex(byte)}, "
        value = value.strip()
        value += "\n"
    value = value[:-2]

    return value + "\n};"
