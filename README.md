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
>>> f.view_change()
```

<style type="text/css">
.cfgtools-tree li.m {
    display: block;
    position: relative;
    padding-left: 2.5rem;
}
.cfgtools-tree li.t,
.cfgtools-tree li.i {
    display: block;
    position: relative;
    padding-left: 0;
}
.cfgtools-tree li.i>span {
    border: solid .1em #666;
    border-radius: .2em;
    display: inline-block;
    margin-top: .5em;
    padding: .2em .5em;
    position: relative;
}
.cfgtools-tree li>details>summary>span.open,
.cfgtools-tree li>details[open]>summary>span.closed {
    display: none;
}
.cfgtools-tree li>details[open]>summary>span.open {
    display: inline;
}
.cfgtools-tree li>details>summary {
    display: block;
    cursor: pointer;
}
.cfgtools-tree ul {
    display: table;
    padding-left: 0;
    margin-left: 0;
}
</style>
<ul class="cfgtools-tree">
<li class="t"><details open><summary>{<span class="closed"> ... },</span></summary>
<ul class="t">
<li class="m"><span style="text-decoration:none;color:#cccccc;background-color:#4d2f2f">'foo': 'bar',</span></li>
<li class="m"><span style="text-decoration:none;color:#cccccc;background-color:#2f4d2f">'foo': None,</span></li>
<li class="m"><span>'this': ['is', 'an', 'example'],</span></li>
<li class="m"><span style="text-decoration:none;color:#cccccc;background-color:#2f4d2f">'that': {'is': ['also', 'an', 'example']},</span></li>
<li class="t">}</li>
</ul>
</details></li>
<li class="i"><span>format: None | path: None | encoding: None</span></li>
</ul>

## See Also
### Github repository
* https://github.com/Chitaoji/cfgtools/

### PyPI project
* https://pypi.org/project/cfgtools/

## License
This project falls under the BSD 3-Clause License.

## History
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
