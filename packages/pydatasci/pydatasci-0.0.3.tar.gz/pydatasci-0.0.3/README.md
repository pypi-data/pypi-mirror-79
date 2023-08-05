# pydatasci

Simplify the end-to-end workflow of machine learning.

```
$ rm -r build dist pydatasci.egg-info
# update version number in setup.py
$ python3 setup.py sdist bdist_wheel
$ python3 -m twine upload --repository pypi dist/*
```