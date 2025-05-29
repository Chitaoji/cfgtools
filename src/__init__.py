"""
# cfgtools
Provides tools for managing config files.

## Usage
### Save to a config file

```py
>>> from cfgtools import config
>>> config({"a": {"b": "c"}}).save("test.yaml")
```
If not specifeid, the format of the file is automatically detected according to the file
suffix. Valid formats include `ini`, `json`, `yaml`, `pickle`, etc.

### Read from a config file
```py
>>> from cfgtools import read_config
>>> read_config("test.yaml")
{'a': {'b': 'c'}}
------------------------------------------------------
format: 'yaml' | path: 'test.yaml' | encoding: 'utf-8'
------------------------------------------------------
```
The encoding and format of the file is automatically detected if not specified.

## See Also
### Github repository
* https://github.com/Chitaoji/cfgtools/

### PyPI project
* https://pypi.org/project/cfgtools/

## License
This project falls under the BSD 3-Clause License.

"""

import lazyr

lazyr.VERBOSE = 0
lazyr.register("yaml")
lazyr.register(".test_case")

# pylint: disable=wrong-import-position
from . import core, iowrapper, reader, test_case
from .__version__ import __version__
from .core import *
from .iowrapper import *
from .reader import *

__all__: list[str] = ["test_case"]
__all__.extend(core.__all__)
__all__.extend(reader.__all__)
__all__.extend(iowrapper.__all__)
