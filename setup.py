"""
Setup file for Pypi.
"""
import os
from setuptools import setup, find_packages


def read_file(filename: str):
    """
    Helper to read files.
    """
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


version = os.environ.get("GIT_TAG").lstrip("v")
if not version:
    raise ValueError("The GIT_TAG environment variable is not set.")

setup(
    name="quantumcrypto",
    version=version,
    description="A cryptography library.",
    packages=find_packages(),
    install_requires=read_file("requirements.txt").splitlines(),
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown"
)
