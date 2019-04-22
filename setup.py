from setuptools import setup, find_packages  # noqa: H301

NAME = "factom-harmony-connect"
VERSION = "1.0.2"
REQUIRES = [
    "base58 >= 1.0.3",
    "ed25519 >= 1.4",
    "validators >= 0.12",
    "requests >= 2.21",
]

setup(
    name=NAME,
    version=VERSION,
    author="Factom, Inc.",
    author_email="harmony-support@factom.com",
    description="Factom Harmony Connect SDK",
    long_description_content_type="text/markdown",
    url="https://github.com/FactomProject/factom-harmony-connect-python-sdk",
    keywords=["factom", "factom-blockchain", "blockchain", "blockchain-as-a-service", "SDK", "Harmony Connect"],
    install_requires=REQUIRES,
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description="""
GETTING STARTED
===============

This section contains a summary of the steps required to get started
with Python Connect SDK installation.

System Requirements
-------------------

In order to use this Python SDK, you will need the following tool:

-  Python version >= 3.5


Installation
-------------
**Published package**

`pip install factom-harmony-connect`

**Open-source package**

- Clone the repo
- Setup a virtual environment (optional)
- Install dependencies
  - `pip install -r requirements.txt`

To use the SDK, you have to import: `from factom_sdk import FactomClient`

For robust documentation, see the github repository
[HERE](https://github.com/FactomProject/factom-harmony-connect-python-sdk)
""")
