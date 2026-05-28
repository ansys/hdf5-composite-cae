# Copyright (C) 2026 ANSYS, Inc. and/or its affiliates.
# Unauthorized use, distribution, or duplication is prohibited.

"""Test module for package metadata.

This module verifies that package metadata such as version information
is correctly defined and accessible.
"""

from ansys.hdf5_composite_cae import __version__


def test_pkg_version():
    """Test that the package version is correctly defined.

    This test ensures that the __version__ attribute is accessible and
    matches the expected version string for the current development build.

    Notes
    -----
    The version string "0.1.dev0" indicates this is a development version.
    This test may need to be updated when the version changes during release.
    """
    # Verify the package version matches the expected development version
    assert __version__ == "0.1.dev0"
