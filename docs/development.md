# Getting Started

# Setup Environment

## Via Python
```shell
pip install -r test_requirements.txt
pdm init
```

## OSX Users
```shell
brew install pdm
pdm init
```

## Everyone Else
[https://pypi.org/project/pdm/](https://pypi.org/project/pdm/)

# Fixes

## Missing Crypto
```shell
pip uninstall crypto pycrypto pycryptodome
pip install pycryptodome
```