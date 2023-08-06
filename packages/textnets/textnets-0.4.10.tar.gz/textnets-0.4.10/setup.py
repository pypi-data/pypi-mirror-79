#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

requirements = [
    "Click>=7.0",
    "pandas==1.0.4",
    "cairocffi==1.1.0",
    "python-igraph==0.8.2",
    "spacy==2.3.0",
    "scipy==1.4.1",
    "toolz==0.10.0",
    "leidenalg==0.8.1",
]

test_requirements = [
    "pytest>=4.6.5",
    "Click",
    "pandas",
    "python-igraph",
    "spacy",
    "scipy",
    "toolz",
    "leidenalg",
]

dev_requirements = [
    "pip==19.2.3",
    "bump2version==0.5.11",
    "wheel==0.33.6",
    "watchdog==0.9.0",
    "flake8==3.7.8",
    "tox==3.14.0",
    "coverage==4.5.4",
    "twine==3.1.1",
    "pytest==4.6.5",
    "pytest-runner==5.1",
    "black==19.3b0",
    "mypy==0.770",
]

setup(
    author="John D. Boy",
    author_email="jboy@bius.moe",
    python_requires=">=3.7",
    name="textnets",
    version="0.4.10",
    description="Automated text analysis with networks",
    long_description=readme,
    url="https://textnets.readthedocs.io",
    packages=find_packages(include=["textnets", "textnets.*"]),
    entry_points={"console_scripts": ["textnets=textnets.cli:main"]},
    include_package_data=True,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords="textnets",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Sociology",
    ],
    test_suite="tests",
    install_requires=requirements,
    extras_require={
        ":python_version<'3.8'": ["typing_extensions", "cached-property"],
        "test": test_requirements,
        "dev": dev_requirements,
        "doc": [
            "Sphinx>=3.0.4",
            "sphinx_rtd_theme",
            "jupyter_sphinx",
            "sphinxcontrib-bibtex",
        ],
    },
)
