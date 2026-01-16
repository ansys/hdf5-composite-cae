# hdf5-composite-cae


## Build

Install uv following these instructions, https://docs.astral.sh/uv/getting-started/installation/#standalone-installer.
Then, create a virtual environment using you preferred Python version `>= 3.10` (you can list available ones with `uv python list`):

```
uv venv --python 3.12.9
.venv\Scripts\activate
```

Install the `ansys.hdf5_composite_cae` package in editable mode with all dev dependencies

```
uv sync
```