"""
# cfgtools
Provides tools for managing config files.

## See Also
### Github repository
* https://github.com/Chitaoji/cfgtools/

### PyPI project
* https://pypi.org/project/cfgtools/

## License
This project falls under the BSD 3-Clause License.

"""

from . import core, iowrapper, reading
from .__version__ import __version__
from .core import *
from .iowrapper import *
from .reading import *

__all__: list[str] = []
__all__.extend(core.__all__)
__all__.extend(reading.__all__)
__all__.extend(iowrapper.__all__)
