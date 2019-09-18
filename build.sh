#!/bin/bash
rm -rf dist build
python setup.py bdist_wheel
python setup.py sdist
twine upload dist/tagore* --repository-url https://upload.pypi.org/legacy/
rm -rf dist build tagore.egg-info