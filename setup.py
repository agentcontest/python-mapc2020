#!/usr/bin/env python

import os.path
import setuptools

setuptools.setup(
    name="mapc2020",
    version="0.1.0",  # Remember to update version in __init__.py and changelog
    author="Niklas Fiekas <nf11@tu-clausthal.de>, Tabajara Krausburg <tkr19@tu-clausthal.de>",
    description="A client for the 2020/21 edition of the Multi-Agent Programming Contest.",
    long_description=open(os.path.join(os.path.dirname(__file__), "README.rst")).read(),
    long_description_content_type="text/x-rst",
    license="GPL-3.0+",
    keywords="agent multi-agent contest",
    url="https://github.com/agentcontest/python-mapc2020",
    packages=["mapc2020"],
    zip_safe=False,  # For mypy
    package_data={
        "mapc2020": ["py.typed"],
    },
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Education",
        "Topic :: Games/Entertainment :: Turn Based Strategy",
        "Topic :: Internet",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries",
        "Typing :: Typed",
    ],
)
