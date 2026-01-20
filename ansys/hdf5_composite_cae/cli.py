# Copyright (C) 2026 ANSYS, Inc. and/or its affiliates.
# Unauthorized use, distribution, or duplication is prohibited.

import argparse
from importlib import resources
from pathlib import Path

from ansys.hdf5_composite_cae.validate import validate_file


def process_file(file_path: Path, throw):
    validate_file(file_path, throw)


def validate():
    parser = argparse.ArgumentParser(description="Validate composite cae h5 file")
    parser.add_argument("file", type=Path, help="H5 file")
    parser.add_argument(
        "--stop-on-first-error",
        action="store_true",
        help="Abort immediately on the first error",
    )
    args = parser.parse_args()
    process_file(args.file, args.stop_on_first_error)


def show_examples():
    parser = argparse.ArgumentParser(description="Show location of example files")
    _ = parser.parse_args()
    print(resources.files("ansys.hdf5_composite_cae").joinpath("example_files"))
