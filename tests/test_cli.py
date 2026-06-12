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

"""Test module for command-line interface (CLI) functionality.

This module tests the CLI commands provided by the hdf5_composite_cae package,
ensuring that command-line tools work correctly.
"""

import sys

from ansys.hdf5_composite_cae.cli import show_examples


def test_cli(capsys, monkeypatch):
    """Test the show_examples CLI command.

    This test verifies that the show_examples CLI function executes without
    errors when invoked through the command-line interface.

    Parameters
    ----------
    capsys : pytest.CaptureFixture
        Pytest fixture for capturing stdout and stderr output.
    monkeypatch : pytest.MonkeyPatch
        Pytest fixture for safely modifying system attributes and environment
        variables during testing.

    Notes
    -----
    The test uses monkeypatch to mock sys.argv to simulate command-line
    invocation without actual command-line arguments.
    """
    # Mock command-line arguments to simulate CLI invocation
    monkeypatch.setattr(sys, "argv", ["cli"])

    # Execute the show_examples function to verify it runs without errors
    show_examples()
