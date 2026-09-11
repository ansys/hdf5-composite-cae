# Copyright (C) 2026 ANSYS, Inc. and/or its affiliates.
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
