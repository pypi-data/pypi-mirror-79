# hoursofoperation

Utilities for loading and doing calculations with a partner's hours of operations configration.

## Install dependencies
   ```
   pip install -e ".[dev]"
   ```

## For maintainers: How to build

1. Increment `__version__` in `setup.py`.
2. Update the Change Log below.
3. Run the following:
   ```
   rm -i dist/*
   python setup.py sdist bdist_wheel
   ```

4. Add and push a release tag
5. Run the following:
   ```
   twine upload dist/*
   ```

## Change Log
### [0.1.12] - 2020-09-10
#### Changed
- Change hoursOfOperation to use the passed in timezone instead of the local timezone

### [0.1.11] - 2019-02-26
#### Added
- Python 3.7 and some build/deployment issues cleaned.

### [0.1.8] - 2018-10-05
#### Added
- Python 3.6+ support!

### [0.1.7] - 2017-12-07
#### Changed
- Fixed issues in setup.py that were preventing package build

### [0.1.6] - 2017-12-07
#### Added
- Dependendies in setup.py

### [0.1.5] - 2017-12-05
#### Changed
- Minor stylistic updates

[0.1.12]: https://github.com/Brightmd/hoursofoperation/compare/release-0.1.11...release-0.1.12
[0.1.11]: https://github.com/Brightmd/hoursofoperation/compare/release-0.1.8...release-0.1.11
[0.1.8]: https://github.com/Brightmd/hoursofoperation/compare/0.1.7...release-0.1.8
[0.1.7]: https://github.com/Brightmd/hoursofoperation/compare/0.1.6...0.1.7
[0.1.6]: https://github.com/Brightmd/hoursofoperation/compare/0.1.5...0.1.6
[0.1.5]: https://github.com/Brightmd/hoursofoperation/tree/0.1.5
