.. _contribute:

**********
Contribute
**********

Thank you for your interest in contributing to the HDF5 Composite CAE project!

Contribution guidelines
=======================

All contributions to this project should follow the guidelines outlined in the
`PyAnsys Developer's Guide <https://dev.docs.pyansys.com/index.html>`_.

The PyAnsys Developer's Guide covers:

- Code style and formatting requirements
- Testing standards and practices
- Documentation requirements
- Pull request procedures
- Code review process

Code of conduct
===============

All contributions are subject to the project's Code of Conduct. Please review and
follow these guidelines to ensure a welcoming and inclusive environment for all
contributors.

You can find the Code of Conduct in the ``CODE_OF_CONDUCT.md`` file in the
project repository.

How to contribute
=================

Setting up your development environment
----------------------------------------

1. Clone the repository
2. Install the development dependencies:

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

Running tests
-------------

Run the test suite to ensure your changes don't break existing functionality:

.. code-block:: bash

    pytest

Building documentation
----------------------

Build the documentation locally to preview your changes:

.. code-block:: bash

    python scripts/build.py build_doc

The built documentation will be available in the ``_build/html`` directory.

Submitting changes
------------------

1. Create a new branch for your changes
2. Make your changes and commit them with clear, descriptive messages
3. Push your branch to the repository
4. Create a pull request with a detailed description of your changes
5. Address any feedback from code reviewers

Types of contributions
======================

We welcome various types of contributions:

Bug reports
-----------

If you find a bug, please open an issue with:

- A clear description of the problem
- Steps to reproduce the issue
- Expected vs. actual behavior
- Your environment (Python version, OS, etc.)

Feature requests
----------------

Have an idea for a new feature? Open an issue describing:

- The feature you'd like to see
- Why it would be useful
- Any implementation ideas you have

Code contributions
------------------

Code contributions are welcome! Please:

- Follow the code style guidelines
- Add tests for new functionality
- Update documentation as needed
- Ensure all tests pass

Documentation improvements
--------------------------

Documentation improvements are always appreciated, including:

- Fixing typos or clarifying existing content
- Adding examples or tutorials
- Improving API documentation
- Translating documentation

Questions and support
=====================

If you have questions about contributing, please:

- Check the existing documentation and issues
- Reach out through the project's issue tracker
- Refer to the `PyAnsys Developer's Guide <https://dev.docs.pyansys.com/index.html>`_

License
=======

By contributing to this project, you agree that your contributions will be licensed
under the same license as the project (MIT License).

Thank you for contributing!

