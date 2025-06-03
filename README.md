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
```

## Usage
### Save to a config file

```py
>>> import cfgtools
>>> cfg = cfgtools.test_case.ip_locations(3, 0)
>>> cfg.save("test.cfg", "yaml") # or: cfg.to_yaml("test.cfg")
```
If not specifeid, the format of the file is automatically detected according to the file suffix. Valid formats include `ini`, `json`, `yaml`, `pickle`, etc. For example:
```py
>>> cfg.save("test.yaml") # a yaml file is created
>>> cfg.save("test.pkl") # a pickle file is created
>>> cfg.save("unspecified.cfg") # by default a json file is created
```
### Read from a config file
```py
>>> cfgtools.read("test.cfg")
{
    '38.113.227.125': [
        'Changchester', '4759 William Haven Apt. 194', 'West Corey, CA 90152',
    ],
    '128.18.185.81': ['Ryanborough', 'Unit 7784 Box 0801', 'DPO AP 52775'],
    '85.75.200.206': [
        'Claytonmouth', '139 John Divide Suite 115', 'Rodriguezside, LA 93111',
    ],
}
-----------------------------------------------------
format: 'yaml' | path: 'test.cfg' | encoding: 'utf-8'
-----------------------------------------------------
```
The encoding and format of the file is automatically detected if not specified.

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