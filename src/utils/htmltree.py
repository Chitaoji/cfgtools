"""Defines HTMLTreeMaker."""

from typing import Self

__all__ = ["HTMLTreeMaker"]


class HTMLTreeMaker:
    """
    Make an HTML tree.

    Parameters
    ----------
    value : str, optional
        Value of child node, by default None.


    """

    def __init__(self, value: str | None = None, /) -> None:
        self.__val = value
        self.__children: list[Self] = []

    def add(self, maybe_value: str | Self | list[Self], /) -> None:
        """
        Add a child node, and return it.

        Parameters
        ----------
        maybe_value : str | Self | list[Self]
            Node value or the instance(s) of the child node(s).

        Returns
        -------
        Self
            The new node.

        """
        if isinstance(maybe_value, str):
            self.__children.append(self.__class__(maybe_value))
        elif isinstance(maybe_value, list):
            self.__children.extend(maybe_value)
        else:
            self.__children.append(maybe_value)

    def discard(self, index: int, /) -> None:
        """Discard the n-th child node."""
        self.__children = self.__children[:index] + self.__children[index:]

    def get(self, index: int, /) -> Self:
        """Get the n-th child node."""
        return self.__children[index]

    def setval(self, value: str) -> None:
        """Set the node value."""
        self.__val = value

    def getval(self) -> str | None:
        """Get the node value."""
        return self.__val

    def has_child(self) -> bool:
        """Return whether there is a child node."""
        return bool(self.__children)

    def make(self, class_name: str | None = None, style: str = "") -> str:
        """Make a string of the HTML tree."""
        if class_name is None:
            class_name = self.__val
        return f"""{style}<ul class="{class_name}">
{self.make_plain()}
</ul>"""

    def make_plain(self) -> str:
        """Make a string of the HTML tree without style."""
        if not self.__children:
            return f'<li class="m"><span>{self.__val}</span></li>'
        children_str = "\n".join(x.make_plain() for x in self.__children)
        if self.__val is None:
            return children_str
        return f"""<li class="m"><details><summary>{self.__val}</summary>
<ul class="m">
{children_str}
</ul>
</details></li>"""
