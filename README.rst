=====
hulks
=====

|CI Build Status|

----

Olist custom pre-commit plugins


Usage
~~~~~

To configure custom pre-commit hooks, create or add an entry in your ``.pre-commit-config.yaml``
as follows:

.. code-block:: yaml

    repos:
      - repo: git@github.com:olist/hulks.git
      rev: main
      hooks:
        - id: check-invalid-domains


Update pre-commit plugins::

    pre-commit autoupdate

Test the custom hook(s) against all your codebase::

    pre-commit run -a -v


The list of available hooks could be found on pre_commit_hooks_file_ or using ``setup.py show_hooks`` command::

    python setup.py -q show_hooks


Development
~~~~~~~~~~~

Create an virtualenv using ``Python 3.6+`` and install the development requirements::

    pip install -r requirements-dev.txt


Optionally, add the package in your current virtualenv for easier access::

    python setup.py develop
    # now you should be able to call any hook by the entry name:
    # my-hook <files>

To execute the repository tests::

    make tests


Creating new hooks
~~~~~~~~~~~~~~~~~~

To create a new hook:

* Copy the example hook: ``cp hulks/example.py hulks/my_hulk.py``
* Add an entry in ``.pre-commit-hooks.yaml`` (more options in pre-commit-documentation_)
* Develop and test your hook following the guidelines below
* Update ``CHANGES.rst`` properly


Guidelines
~~~~~~~~~~

Keep in mind that all plugins are installed via ``setup.py`` script by ``pre-commit``.

The following guides should help us when creating new hooks:

* Add an entry in ``.pre-commit-hooks.yaml``

    * the ``name`` entry should be the hook path (eg ``hulks.my_hook``)

* Your hook entrypoint is always a function named ``main``
* Add your hook dependencies in ``requirements.txt``


Testing
~~~~~~~

To test a newly added hook, you can:

* Follow these instructions_. (you must commit your code before testing)
* Add the hook to another project ``.pre-commit-config.yaml``. (you must commit your code before testing)
* Update ``pre-commit`` (``pre-commit autoupdate``)
* Or simple run ``python -m hulks.my_new_hook <filenames>``.


Release
~~~~~~~

Check if ``CHANGES.rst`` contains the correct version number (follow semver_).
Create the proper tags with::

    make release


.. _instructions: https://pre-commit.com/#developing-hooks-interactively
.. _pre-commit-documentation: https://pre-commit.com/#new-hooks
.. _pre_commit_hooks_file:  https://github.com/olist/hulks/blob/main/.pre-commit-hooks.yaml
.. _semver: https://semver.org/
.. |CI Build Status| image:: https://github.com/olist/hulks/actions/workflows/test.yml/badge.svg
