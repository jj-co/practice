import os
import sys


def unpack(directory: str, files: list = []) -> list:
    for entry in os.scandir(directory):
        if entry.is_dir():
            files = unpack(entry, files=files)
        elif entry.is_file():
            files.append(entry)
    return files


def find_stats(files: list) -> dict:
    extensions = {}
    for entry in files:
        if "." not in entry.name:
            continue

        ext_name = entry.name.split(".")[1]
        ext_size = os.path.getsize(entry)
        if (new_name := ext_name) not in extensions.keys():
            extensions[new_name] = {
                "number": 1,
                "largest": ext_size,
                "total": ext_size,
            }

        else:
            extensions[ext_name]["largest"] = max(
                ext_size, extensions[ext_name]["largest"]
            )
            extensions[ext_name]["number"] += 1
            extensions[ext_name]["total"] += extensions[ext_name]["largest"]

    return extensions


def format_result(extensions):
    table_data = []
    result = ""
    for ext in extensions:
        result = (
            result
            + "."
            + ext
            + " "
            + str(extensions[ext]["number"])
            + " "
            + str(extensions[ext]["largest"])
            + " "
            + str(extensions[ext]["total"])
            + "\n"
        )

        table_data.append(
            [
                "." + ext,
                extensions[ext]["number"],
                extensions[ext]["largest"],
                extensions[ext]["total"],
            ]
        )

    return table_data


def main():
    directory = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    files = unpack(directory)
    extensions = find_stats(files)
    table = format_result(extensions)
    for row in table:
        print("{: <20} {: >10} {: >20} {: >20}".format(*row))


if __name__ == "__main__":
    main()
