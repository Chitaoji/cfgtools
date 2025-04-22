"""
# cfgtools
Provides tools for managing config files.

## Usage
### Save to a config file

```py
>>> from cfgtools import config
>>> config({"a": {"b": "c"}}).save("test.yaml")
```

### Read from a config file
Use `read_config()` to read from a config file in any valid format. The valid formats
are `ini`, `json`, `yaml`, `pickle`, etc. The `encoding` of the file is automatically
detected if not specified.

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

"""

import lazyr

lazyr.VERBOSE = 0
lazyr.register("yaml")

# pylint: disable=wrong-import-position
from . import core, iowrapper, reading
from .__version__ import __version__
from .core import *
from .iowrapper import *
from .reading import *

__all__: list[str] = []
__all__.extend(core.__all__)
__all__.extend(reading.__all__)
__all__.extend(iowrapper.__all__)
