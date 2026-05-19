# Copyright (C) 2026 ANSYS, Inc. and/or its affiliates.
# Unauthorized use, distribution, or duplication is prohibited.

import sys

from ansys.hdf5_composite_cae.cli import show_examples


def test_cli(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["cli"])
    show_examples()
