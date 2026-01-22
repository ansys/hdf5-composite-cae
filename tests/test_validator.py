import tempfile
from pathlib import Path

import h5py as h5

from ansys.hdf5_composite_cae.file_creation import create_minimal_h5_file
from ansys.hdf5_composite_cae.validate import validate_file


def test_validator_minimal():
    test_filename = "test_file.h5"
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / test_filename
        create_minimal_h5_file(filepath)
        validate_file(filepath, True)


def test_empty():
    test_filename = "test_file.h5"
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / test_filename
        with h5.File(filepath, "w") as f:
            _ = f.create_group("composite_cae")
        validate_file(filepath)


def test_validator_winding():
    test_filename = "ansys/hdf5_composite_cae/example_files/winding_example.h5"
    validate_file(test_filename, True)


def test_validator_3d_print():
    test_filename = "ansys/hdf5_composite_cae/example_files/example_3D_print.h5"
    validate_file(test_filename, True)
