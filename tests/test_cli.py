import sys

from ansys.hdf5_composite_cae.cli import show_examples


def test_cli(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["cli"])
    show_examples()
