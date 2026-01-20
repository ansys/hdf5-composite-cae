import tempfile
from pathlib import Path

from ansys.hdf5_composite_cae.file_creation import create_minimal_h5_file
from ansys.hdf5_composite_cae.validate import validate_file


def test_validator_minimal():
    test_filename = "test_file.h5"
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / test_filename
        create_minimal_h5_file(filepath)
        validate_file(filepath)


def test_validator_winding():
    test_filename = "ansys/hdf5_composite_cae/example_files/winding_example.h5"
    validate_file(test_filename)


def test_validator_3d_print():
    test_filename = "ansys/hdf5_composite_cae/example_files/example_3D_print.h5"
    validate_file(test_filename)
