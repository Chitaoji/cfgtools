# cfgtools
Provides tools for managing config files.

## Installation
```sh
$ pip install cfgtools
```

## Requirements
```txt
pyyaml
lazyr
```

## Usage
### Save to a config file

```py
>>> from cfgtools import config
>>> config({"a": {"b": "c"}}).save("test.yaml")
```

### Read from a config file
Use `read_config()` to read from a config file in any valid format. The valid formats are `ini`, `json`, `yaml`, `pickle`, etc. The `encoding` of the file is automatically detected if not specified.

```py
>>> from cfgtools import read_config
>>> read_config("test.yaml")
{'a': {'b': 'c'}}
------------------------------------------------------
format: 'yaml' | path: 'test.yaml' | encoding: 'utf-8'
------------------------------------------------------
```

## See Also
### Github repository
* https://github.com/Chitaoji/cfgtools/

### PyPI project
* https://pypi.org/project/cfgtools/

## License
This project falls under the BSD 3-Clause License.

## History
### v0.0.0
* Initial release.