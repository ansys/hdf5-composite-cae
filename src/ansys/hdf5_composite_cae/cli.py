# Copyright (C) 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
from importlib import resources
from pathlib import Path

from ansys.hdf5_composite_cae import create_minimal_h5_file
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
    print("Validating file:", args.file)
    try:
        process_file(args.file, args.stop_on_first_error)
        print(
            "Validation completed successfully. File is a valid composite CAE h5 file."
        )
    except RuntimeError as e:
        print("Validation failed due to the following error(s) :", str(e))
        if args.stop_on_first_error:
            print("Stopping on first error.")


def show_examples():
    """Command-line interface for displaying the location of example files.

    This function serves as the entry point for the examples CLI tool.
    It prints the directory path where example HDF5 files are located
    within the ansys.hdf5_composite_cae package.
    """
    parser = argparse.ArgumentParser(description="Show location of example files")
    _ = parser.parse_args()
    print(resources.files("ansys.hdf5_composite_cae").joinpath("example_files"))


def create_minimal_file():
    """Command-line interface for creating a minimal composite CAE HDF5 file."""
    parser = argparse.ArgumentParser(
        description="Create minimal composite CAE HDF5 file."
    )
    parser = argparse.ArgumentParser(description="Validate composite cae h5 file")
    parser.add_argument("output_file", type=Path, help="H5 file")

    args = parser.parse_args()
    create_minimal_h5_file(args.output_file)
    print("Minimal composite CAE HDF5 file created at:", args.output_file)
