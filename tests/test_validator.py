# Copyright (C) 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
        with pytest.raises(RuntimeError, match="Missing key 'components'"):
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
