import argparse
import os
import sys
import typing

from . import process_from_file
from .utils import info, error

def main(args: typing.List[str]) -> int:
    parser = argparse.ArgumentParser(prog='dotpruner')
    parser.add_argument('filename', type=str)
    parser.add_argument('--dest', '-d', type=str, default=None)
    parser.add_argument('--overwrite', '-o', type=bool, default=False)

    parsed_args = parser.parse_args(args)
    if parsed_args.dest is None:
        parsed_args.dest = parsed_args.filename
        parsed_args.overwrite = True

    final_graph = process_from_file(parsed_args.filename)

    if os.path.exists(parsed_args.dest) and not parsed_args.overwrite:
        error(f'Path exists but overwrite flag not specified: "{parsed_args.dest}"')
        return 1

    try:
        with open(parsed_args.dest, 'w') as output_file:
            output_file.write(final_graph.to_string())
    except OSError:
        error(f'Error writing to file: "{parsed_args.dest}"')
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))