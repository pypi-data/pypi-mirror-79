.. highlight:: shell

============
Installation
============

**textnets** is in the `Python Package Index`_, so it can be installed using
`pip`_.

.. _`Python Package Index`: https://pypi.org/project/textnets/
.. _pip: https://pip.pypa.io

.. note::

   Please note that **textnets** requires Python 3.7 or newer to run.

In a `virtual environment`_, run::

   $ pip install textnets

.. _`virtual environment`: https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments

This is the preferred method to install **textnets**, as it always installs
the most recent stable release.

If you don't have pip installed, the `Python installation guide`_ can guide you
through the process.

.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/
.. _conda: https://conda.io/

Plotting
--------

**textnets** installs the `Cairo`_ graphics library as a dependency for
plotting using the `cairocffi`_ package. In some cases you may have to `install
CFFI`_ separately for plotting to work.

.. _Cairo: https://www.cairographics.org/
.. _cairocffi: https://cairocffi.readthedocs.io/
.. _install CFFI: https://cffi.readthedocs.io/en/latest/installation.html

Language Support
----------------

Most likely you also have to install an appropriate `language model`_ by
issuing a command like::

   $ python -m spacy download en_core_web_sm

After updating **textnets** you may also need to update the language models.
Run the following command to check::

   $ python -m spacy validate

.. _`language model`: https://spacy.io/usage/models#download

If there are no language models available for your corpus language, there may
be some `basic support <https://spacy.io/usage/models#languages>`_. Even in
that case, some languages (including Korean, Vietnamese, Thai, Russian, and
Ukrainian) require additional installs for tokenization support. Consult the
spacy documentation for details.
