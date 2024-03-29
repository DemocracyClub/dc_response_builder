#!/usr/bin/env python3

from setuptools import setup

setup(
    name="dc_response_builder",
    version="0.0.13",
    description="Builds API responses",
    author="Sym Roe",
    author_email="sym.roe@democracyclub.org.uk",
    setup_requires=["wheel"],
    packages=["response_builder"],
    package_dir={"response_builder": "."},
    package_data={"response_builder": ["v1/*", "v1/**/*"]},
    install_requires=["uk-election-ids==0.7.3", "pydantic[email]>=1.10,<2"],
)
