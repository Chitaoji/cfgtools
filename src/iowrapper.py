"""
Contains the io wrapper: ConfigIOWrapper.

NOTE: this module is private. All functions and objects are available in the main
`cfgtools` namespace - use that instead.

"""

from pathlib import Path
from typing import TYPE_CHECKING, Iterable, Self

import yaml

if TYPE_CHECKING:
    from ._typing import Config, Data


class ConfigIOWrapper:
    """
    A wrapper for reading and writing config files.

    Parameters
    ----------
    config : Config
        Config object.
    path : str | Path | None, optional
        File path, by default None.
    encoding : str | None, optional
        The name of the encoding used to decode or encode the file,
        by default None.

    """

    def __init__(
        self,
        config: "Config",
        path: str | Path | None = None,
        encoding: str | None = None,
    ) -> None:
        self.config = config
        self.path = path
        self.encoding = encoding

    def __getitem__(self, __key: "Data") -> "Config":
        if isinstance(self.config, (list, dict)):
            return ConfigIOWrapper(self.config[__key], encoding=self.encoding)
        raise TypeError("the config object is not subscriptable")

    def __setitem__(self, __key: "Data", __value: "Config"):
        if isinstance(self.config, (list, dict)):
            self.config[__key] = __value
        else:
            raise TypeError("the config object does not support item assignment")

    def __repr__(self) -> str:
        return repr(self.config)

    def __enter__(self) -> Self:
        if self.path is None:
            raise TypeError(
                "failed to open the wrapper because it's a children node of the "
                "original wrapper - try to open the original wrapper instead"
            )
        return self

    def __exit__(self, *args) -> None:
        self.save()

    def save(self, path: str | Path | None = None) -> None:
        """
        Save the config.

        Parameters
        ----------
        path : str | Path | None, optional
            File path, by default None. If no path is specified, use `self.path`
            instead.

        Raises
        ------
        TypeError
            Raised when both path and `self.path` are None.

        """
        if path is None:
            if self.path is None:
                raise TypeError(
                    "failed to save the config because no path is specified"
                )
            path = self.path
        with open(path, "w", encoding=self.encoding) as f:
            yaml.dump(self.config, f, sort_keys=False)

    def keys(self) -> "Iterable[Data]":
        """Provide a view of the config object's keys if it's a dict."""
        if isinstance(self.config, dict):
            return self.config.keys()
        raise TypeError("the config object is not a dict")

    def values(self) -> "Iterable[Config]":
        """Provide a view of the config object's values if it's a dict."""
        if isinstance(self.config, dict):
            return self.config.values()
        raise TypeError("the config object is not a dict")

    def items(self) -> "Iterable[tuple[Data, Config]]":
        """Provide a view of the config object's items if it's a dict."""
        if isinstance(self.config, dict):
            return self.config.items()
        raise TypeError("the config object is not a dict")

    def append(self, __object: "Config") -> None:
        """Append object to the end of the config object if it's a list."""
        if isinstance(self.config, list):
            return self.config.append(__object)
        raise TypeError("the config object is not a list")

    def extend(self, __object: "Iterable[Config]") -> None:
        """Extend the config object if it's a list."""
        if isinstance(self.config, list):
            return self.config.extend(__object)
        raise TypeError("the config object is not a list")
