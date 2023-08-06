def chunks(list_, count):
    for i in range(0, len(list_), count):
        yield list_[i : i + count]


def write_file(path: str, contents: str):
    with open(path, "w") as f:
        f.write(contents)
