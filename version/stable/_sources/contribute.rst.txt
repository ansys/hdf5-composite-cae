.. _contribute:

Contribute
##########

Thank you for your interest in contributing to the HDF5 Composite CAE project.

Contribution guidelines
-----------------------

All contributions must follow the guidelines outlined in the
`PyAnsys Developer's Guide <https://dev.docs.pyansys.com/index.html>`_.

For general guidance, see the `Contributing <https://dev.docs.pyansys.com/how-to/contributing.html>`__ section in the *PyAnsys Developer's Guide*.

You must follow these guidelines before contributing to the HDF5 composite CAE package.

The guide includes:

- Code style and formatting
- Testing practices
- Documentation requirements
- Pull request workflow
- Code review process

Code of conduct
---------------

All contributions must follow the project's Code of Conduct to ensure a welcoming
and inclusive environment.

See the ``CODE_OF_CONDUCT.md`` file in the repository.

How to contribute
-----------------

Set up your development environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Clone the repository.
2. Install development dependencies:

.. code-block:: bash

    # Install uv package manager
    # See: https://docs.astral.sh/uv/getting-started/installation/

    # Create virtual environment with Python >= 3.10
    uv venv --python 3.12

    # Activate the virtual environment
    # Windows:
    .venv\Scripts\activate
    # Linux/macOS:
    source .venv/bin/activate

    # Install package with all development dependencies
    uv sync --all-groups

Run tests
~~~~~~~~~

Run the test suite before submitting changes:

.. code-block:: bash

    pytest

Ensure all tests pass.

Build documentation
~~~~~~~~~~~~~~~~~~~

Build the documentation locally to preview changes:

.. code-block:: bash

    python scripts/build.py build_doc

The generated documentation is in the ``_build/html`` directory.

Submit changes
~~~~~~~~~~~~~~

1. Create a feature branch.
2. Make your changes.
3. Commit using clear, descriptive messages.
4. Push your branch to the repository.
5. Open a pull request with a detailed description of your changes.
6. Address any feedback from code reviewers.

Types of contributions
----------------------

You can contribute in the following ways:

Report bugs
~~~~~~~~~~~

Open an issue and include:

- Description of the issue.
- Steps to reproduce.
- Expected versus actual behavior.
- Environment details (Python version, OS, etc.).

Request features
~~~~~~~~~~~~~~~~

Open an issue that describes:

- The proposed feature.
- Why it is useful.
- Any suggested implementation.

Contribute code
~~~~~~~~~~~~~~~

When submitting code:

- Follow the code style guidelines.
- Add or update tests.
- Update documentation as needed.
- Ensure all tests pass.

Improve documentation
~~~~~~~~~~~~~~~~~~~~~

Contribute documentation improvements, such as:

- Fixing errors or clarifying content.
- Adding examples or tutorials.
- Improving API documentation.
- Translating documentation.

Questions and support
---------------------

If you have questions, you can:

- Review existing documentation and issues.
- Open a new issue for discussion.
- Refer to the `PyAnsys Developer's Guide <https://dev.docs.pyansys.com/index.html>`__.

License
-------

By contributing, you agree that your contributions are licensed
under the project's Apache 2.0 License.

