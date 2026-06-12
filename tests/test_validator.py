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

"""Test module for HDF5 file validation functionality.

This module contains tests for validating composite CAE HDF5 files,
including tests for minimal valid files, invalid files, and example files
with different manufacturing processes (winding and 3D printing).
"""

import tempfile
from pathlib import Path

import h5py as h5
import pytest

from ansys.hdf5_composite_cae.file_creation import create_minimal_h5_file
from ansys.hdf5_composite_cae.validate import validate_file


def test_validator_minimal():
    """Test validation of a minimal valid HDF5 file.

    This test creates a minimal HDF5 file with the required structure
    and verifies that it passes validation without errors.

    Notes
    -----
    The test uses a temporary directory to create and validate the file,
    which is automatically cleaned up after the test completes.
    """
    test_filename = "test_file.h5"
    # Use a temporary directory that is automatically cleaned up after the test
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / test_filename
        # Create a minimal valid HDF5 file with required structure
        create_minimal_h5_file(filepath)
        # Validate the file and stop on first error if any
        validate_file(filepath, True)


def test_empty():
    """Test validation of an incomplete HDF5 file.

    This test creates an HDF5 file with only the root group but missing
    required attributes and datasets. It verifies that the validator
    correctly identifies and reports validation errors.

    Notes
    -----
    The test expects a RuntimeError to be raised with a message containing
    "Validation errors" when the incomplete file is validated.
    """
    test_filename = "test_file.h5"
    # Use a temporary directory that is automatically cleaned up after the test
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / test_filename
        # Create an incomplete HDF5 file with only the root group
        with h5.File(filepath, "w") as f:
            _ = f.create_group("composite_cae")
        # Verify that validation raises an error for the incomplete file
        with pytest.raises(RuntimeError, match="Validation errors"):
            validate_file(filepath)


def test_validator_winding():
    """Test validation of a winding process example file.

    This test validates a pre-existing example HDF5 file that represents
    a composite part manufactured using the filament winding process.
    It ensures that the example file conforms to the expected schema.
    """
    # Path to the example winding file included in the package
    test_filename = "src/ansys/hdf5_composite_cae/example_files/winding_example.h5"
    # Validate the example file and stop on first error if any
    validate_file(test_filename, True)


def test_validator_3d_print():
    """Test validation of a 3D printing process example file.

    This test validates a pre-existing example HDF5 file that represents
    a composite part manufactured using additive manufacturing (3D printing).
    It ensures that the example file conforms to the expected schema.
    """
    # Path to the example 3D printing file included in the package
    test_filename = "src/ansys/hdf5_composite_cae/example_files/example_3D_print.h5"
    # Validate the example file and stop on first error if any
    validate_file(test_filename, True)
