"""
Contains the io wrapper: ConfigIOWrapper.

NOTE: this module is private. All functions and objects are available in the main
`cfgtools` namespace - use that instead.

"""

from pathlib import Path
from typing import TYPE_CHECKING, Callable, Self

from .css import TREE_CSS_STYLE
from .saver import ConfigSaver
from .tpl import ConfigTemplate, _DictConfigTemplate, _ListConfigTemplate
from .utils.htmltree import HTMLTreeMaker

if TYPE_CHECKING:
    from ._typing import ConfigFileFormat, DataObj

NoneType = type(None)

__all__ = ["FileFormatError"]


SUFFIX_MAPPING = {
    ".yaml": "yaml",
    ".yml": "yaml",
    ".pickle": "pickle",
    ".pkl": "pickle",
    ".json": "json",
    ".ini": "ini",
    ".txt": "text",
    ".bytes": "bytes",
}
FORMAT_MAPPING = {
    "yaml": "yaml",
    "yml": "yaml",
    "pickle": "pickle",
    "pkl": "pickle",
    "json": "json",
    "ini": "ini",
    "text": "text",
    "txt": "text",
    "bytes": "bytes",
}


class ConfigIOWrapper(ConfigTemplate, ConfigSaver):
    """A template for matching config objects."""

    valid_types = (str, int, float, bool, NoneType)
    constructor = object
    sub_constructors = {
        dict: lambda: _DictConfigIOWrapper,
        list: lambda: _ListConfigIOWrapper,
    }

    def __init__(
        self,
        data: "DataObj",
        fileformat: "ConfigFileFormat | None" = None,
        /,
        path: str | Path | None = None,
        encoding: str | None = None,
    ) -> None:
        super().__init__(data)
        self.fileformat = fileformat
        self.overwrite_ok = True
        if path is None:
            self.path = None
        else:
            path = Path(path)
            self.path = path.absolute().relative_to(path.cwd()).as_posix()
        self.encoding = encoding

    def __enter__(self) -> Self:
        if self.path is None:
            raise TypeError("no default file path, please run self.set_path() first")
        if not self.overwrite_ok:
            raise TypeError(
                "overwriting the original path is not allowed, please run "
                "self.unlock() first"
            )
        self.lock()
        return self

    def __exit__(self, *args) -> None:
        self.unlock()
        self.save()

    def _repr_mimebundle_(self, *_, **__) -> dict[str, str]:
        maker = self.to_html()
        maker.setcls("t")
        main_maker = HTMLTreeMaker()
        main_maker.add(maker)
        main_maker.add(
            (
                f"format: {self.fileformat!r} | path: {self.path!r} "
                f"| encoding: {self.encoding!r}"
            ),
            "i",
        )
        return {"text/html": main_maker.make("cfgtools-tree", TREE_CSS_STYLE)}

    def set_path(self, path: str | Path) -> None:
        """Set the path."""
        if not self.overwrite_ok:
            raise TypeError(
                "set_path() is not allowed when the instance is locked, "
                "please run self.unlock() first"
            )
        self.path = path

    def lock(self) -> None:
        """Lock the original path so that it can not be overwritten."""
        self.overwrite_ok = False

    def unlock(self) -> None:
        """Unlock the original path so that it can be overwritten."""
        self.overwrite_ok = True

    def match(self, template: "DataObj", /) -> Self | None:
        """Match the template from the top level."""
        if isinstance(template, ConfigTemplate):
            if isinstance(template, ConfigIOWrapper):
                raise TypeError("expected a config template")
        else:
            template = ConfigTemplate(template)

        if isinstance(t := template.unwrap_top_level(), (dict, list)):
            pass
        elif isinstance(t, type):
            if isinstance(self.__obj, t):
                return self
        elif isinstance(t, Callable):
            if t(self.__obj):
                return self
        elif self.__obj == t:
            return self
        return None

    def save(
        self,
        path: str | Path | None = None,
        fileformat: "ConfigFileFormat | None" = None,
        /,
        encoding: str | None = None,
    ) -> None:
        """
        Save the config.

        Parameters
        ----------
        path : str | Path | None, optional
            File path, by default None. If not specified, use `self.path`
            instead.
        fileformat : ConfigFileFormat | None, optional
            File format to save, by default None. If not specified, the
            file format will be automatically decided.
        encoding : str | None, optional
            The name of the encoding used to decode or encode the file
            (if needed), by default None. If not specified, use
            `self.encoding` instead.

        Raises
        ------
        ValueError
            Raised if both `path` and `self.path` are None.
        FileFormatError
            Raised if the file format is not supported.
        TypeError
            Raised if `self.overwrite_ok` is False.

        """
        if path is None:
            if self.path is None:
                raise ValueError(
                    "no default file path, please specify the path or run "
                    "self.set_path() first"
                )
            if not self.overwrite_ok:
                raise TypeError(
                    "overwriting the original path is not allowed, please run "
                    "self.unlock() first"
                )
            path = self.path
        if fileformat is None:
            if (suffix := Path(path).suffix) in SUFFIX_MAPPING:
                fileformat = SUFFIX_MAPPING[suffix]
            else:
                fileformat = "json" if self.fileformat is None else self.fileformat
        encoding = self.encoding if encoding is None else encoding
        if fileformat in FORMAT_MAPPING:
            super().save(path, FORMAT_MAPPING[fileformat], encoding=encoding)
        else:
            raise FileFormatError(f"unsupported config file format: {fileformat!r}")


class _DictConfigIOWrapper(ConfigIOWrapper, _DictConfigTemplate):
    constructor = ConfigIOWrapper
    sub_constructors = {}

    def match(self, template: "DataObj", /) -> Self | None:
        if matched := super().match(template):
            return matched
        if not isinstance(t := template.unwrap_top_level(), dict):
            return None


class _ListConfigIOWrapper(ConfigIOWrapper, _ListConfigTemplate):
    constructor = ConfigIOWrapper
    sub_constructors = {}


class FileFormatError(Exception):
    """Raised if the file format is not supported."""
