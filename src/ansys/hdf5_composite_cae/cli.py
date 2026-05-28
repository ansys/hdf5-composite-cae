# Copyright (C) 2026 ANSYS, Inc. and/or its affiliates.
# Unauthorized use, distribution, or duplication is prohibited.

import argparse
from importlib import resources
from pathlib import Path

from ansys.hdf5_composite_cae.validate import validate_file


def process_file(file_path: Path, throw):
    """Process and validate a composite CAE HDF5 file.

    Parameters
    ----------
    file_path : Path
        Path to the HDF5 file to validate.
    throw : bool
        If True, stops validation on the first error encountered.
        If False, collects and reports all validation errors.
    """
    validate_file(file_path, throw)


def validate():
    """Command-line interface for validating composite CAE HDF5 files.

    This function serves as the entry point for the validation CLI tool.
    It parses command-line arguments and validates the specified HDF5 file.

    Command-line Arguments
    ----------------------
    file : Path
        Path to the HDF5 file to validate.
    --stop-on-first-error : flag, optional
        If provided, validation aborts immediately on the first error.
        Otherwise, all errors are collected and reported.
    """
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
    """Command-line interface for displaying the location of example files.

    This function serves as the entry point for the examples CLI tool.
    It prints the directory path where example HDF5 files are located
    within the ansys.hdf5_composite_cae package.
    """
    parser = argparse.ArgumentParser(description="Show location of example files")
    _ = parser.parse_args()
    print(resources.files("ansys.hdf5_composite_cae").joinpath("example_files"))
