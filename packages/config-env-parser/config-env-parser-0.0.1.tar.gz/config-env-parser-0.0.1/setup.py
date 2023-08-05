"""
Setup module. This file specifies the setup instructions of this package.
"""
import setuptools

# Read the Readme as long description
with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="config-env-parser",
    version="0.0.1",
    author="Jochen Gietzen",
    author_email="dev@gietzen.org",
    description=(
        "Configuration parser with all variables possible "
        "to overwrite by environment variables"
    ),
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/jockel/config-env-parser.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
