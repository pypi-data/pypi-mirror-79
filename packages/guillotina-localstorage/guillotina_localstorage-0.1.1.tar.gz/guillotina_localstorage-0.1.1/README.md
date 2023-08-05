# guillotina_localstorage

[![Build Status](https://travis-ci.org/vinissimus/guillotina_localstorage.svg?branch=master)](https://travis-ci.org/vinissimus/guillotina_localstorage) [![PyPI version](https://badge.fury.io/py/guillotina-localstorage.svg)](https://badge.fury.io/py/guillotina-localstorage) [![Codcov](https://codecov.io/gh/vinissimus/guillotina_localstorage/branch/master/graph/badge.svg)](https://codecov.io/gh/vinissimus/guillotina_localstorage/branch/master) ![](https://img.shields.io/pypi/pyversions/guillotina_localstorage.svg)

Local FS storage support for Guillotina.

## Example

Example config.json entry:

```json
{
    "applications": [
        # ...,
        "guillotina_localstorage"
    ],
    "storage": {"upload_folder": "/tmp"}
}
```

This library uses [aiofiles](https://github.com/Tinche/aiofiles)
