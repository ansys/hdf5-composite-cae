# Copyright (C) 2026 ANSYS, Inc. and/or its affiliates.
# Unauthorized use, distribution, or duplication is prohibited.

"""
hdf5-composite-cae.

library
"""

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

__version__ = importlib_metadata.version(__name__.replace(".", "-"))

from .file_creation import (
    create_minimal_h5_file,
)
from .validate import (
    validate_file,
)

__all__ = ("create_minimal_h5_file", "validate_file", "__version__")
