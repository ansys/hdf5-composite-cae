# Copyright (C) 2026 ANSYS, Inc. and/or its affiliates.
# Unauthorized use, distribution, or duplication is prohibited.

from ansys.hdf5_composite_cae import __version__


def test_pkg_version():
    assert __version__ == "0.1.dev0"
