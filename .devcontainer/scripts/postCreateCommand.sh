#!/bin/sh

pip install -U pip poetry mypy
poetry config virtualenvs.in-project true
poetry install
mypy --install-types
