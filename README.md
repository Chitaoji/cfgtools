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
Faker
htmlmaster
toml
```

## Usage
### Save to a config file

```py
>>> import cfgtools as cfg
>>> f = cfg.config({"foo": "bar", "this": ["is", "an", "example"]})
>>> f.save("test.cfg", "yaml") # or: f.to_yaml("test.cfg")
```
If not specifeid, the format of the file will be automatically detected according to the file suffix. Valid formats include `ini`, `json`, `yaml`, `pickle`, `toml`, etc. For example:
```py
>>> f.save("test.yaml") # a yaml file is created
>>> f.save("test.pkl") # a pickle file is created
>>> f.save("unspecified.cfg") # by default a json file is created
```

### Read from a config file
```py
>>> cfg.read("test.cfg")
cfgtools.config({'foo': 'bar', 'this': ['is', 'an', 'example']})
```
The encoding and format of the file will be automatically detected if not specified.

### Modify configs
```py
>>> f["foo"] = None
>>> f["that"] = {"is": ["also", "an", "example"]}
>>> f
cfgtools.config({
    'foo': None, 'this': ['is', 'an', 'example'],
    'that': {'is': ['also', 'an', 'example']},
})
```
If user wants to check the changed items, run:
```py
>>> f.view_change()         # auto mode now uses light style
>>> f.view_change("light")  # optimized for light/white backgrounds
>>> f.view_change("dark")   # optimized for dark/black backgrounds
```

## See Also
### Github repository
* https://github.com/Chitaoji/cfgtools/

### PyPI project
* https://pypi.org/project/cfgtools/

## License
This project falls under the BSD 3-Clause License.

## History
### v0.1.0
* Added/updated package metadata for the 0.1.0 release (via `pyproject.toml`) and aligned dependencies.
* Improved HTML rendering for large trees by collapsing/paginating overflow nodes for better readability.
* Enhanced `view_change()` display styles with explicit `light` / `dark` themes and refined auto-mode behavior for consistent output.
* Fixed light-theme style detection issues in VS Code webviews.

### v0.0.9
* Bugfix when reading text files.

### v0.0.8
* Added a simple cli command `cfg [OPTIONS] FILENAME`.
* Renamed `ConfigIOWrapper.safematch()` to `ConfigIOWrapper.adapt()`.

### v0.0.7
* New method for `BasicWrapper`: `*.asstr()`, `*.asint()`, `*.asfloat()`, `*.asbool()`, `*.asnone()`.

### v0.0.6
* Beautified the output of `ConfigIOWrapper.view_change()` through `_repr_mimebundle_()`.

### v0.0.5
* Added support for .toml files.
* New method for `ConfigIOWrapper`: `*.view_change()`, `*.asdict()`, `*.aslist()`.

### v0.0.4
* Fixed a bug in path resolution.

### v0.0.3
* Added reliance on `htmlmaster`.

### v0.0.2
* New method `ConfigIOWrapper.safematch()`.

### v0.0.1
* Initial release.
