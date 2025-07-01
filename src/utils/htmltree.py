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
    nodecls : str, optional
        Class name of the current node, by default "m" ("m" for "main").
    treecls : str, optional
        Class name of the tree, by default "tree".
    style : str | None, optional
        Css style, by default None.
    level_open : int, optional
        Specifies how many levels of the tree are defaultly set open, by
        default 3.

    """

    def __init__(
        self,
        value: str | None = None,
        nodecls: str = "m",
        treecls: str = "tree",
        style: str | None = None,
        level_open: int = 3,
    ) -> None:
        self.__val = value
        self.__nodecls = nodecls
        self.__treecls = treecls
        self.__style = style
        self.__level_open = level_open
        self.__children: list[Self] = []

    def add(self, value: str | Self, nodecls: str | None = None, /) -> None:
        """
        Add a child node.

        Parameters
        ----------
        value : str | Self | list[Self]
            Node value or an instance of the child node.
        nodecls : str | None, optional
            Node class name, by default None.

        Returns
        -------
        Self
            The new node.

        """
        if isinstance(value, str):
            self.__children.append(
                self.__class__(value, "m" if nodecls is None else nodecls)
            )
        else:
            if not isinstance(value, self.__class__):
                raise TypeError(
                    f"object of type {value.__class__.__name__} is not allowed "
                    "to be a child node"
                )
            if nodecls:
                value.setcls(nodecls)
            self.__children.append(value)

    def discard(self, index: int, /) -> None:
        """Discard the n-th child node."""
        self.__children = self.__children[:index] + self.__children[index:]

    def get(self, index: int, /) -> Self:
        """Get the n-th child node."""
        return self.__children[index]

    def setval(self, value: str, /) -> None:
        """Set the node value."""
        self.__val = value

    def getval(self) -> str | None:
        """Get the node value."""
        return self.__val

    def setcls(self, nodecls: str, /) -> None:
        """Set the node class name."""
        self.__nodecls = nodecls

    def getcls(self) -> str | None:
        """Get the node class name."""
        return self.__nodecls

    def set_treecls(self, treecls: str, /) -> None:
        """Set the tree class name."""
        self.__treecls = treecls

    def get_treecls(self) -> str | None:
        """Get the tree class name."""
        return self.__treecls

    def setstyle(self, style: str | None, /) -> None:
        """Set the default css style."""
        self.__style = style

    def getstyle(self) -> str | None:
        """Get the default css style."""
        return self.__style

    def has_child(self) -> bool:
        """Return whether there is a child node."""
        return bool(self.__children)

    def make(self, treecls: str | None = None, style: str | None = None) -> str:
        """
        Make a string representation of the HTML tree.

        Parameters
        ----------
        treecls : str | None, optional
            The class name of the tree, by default None.
        style : str | None, optional
            Css style, by default None.

        Returns
        -------
        str
            String representation.

        """
        if treecls is None:
            treecls = self.__treecls
        if style is None:
            if self.__style is None:
                style = """<style type="text/css">
.{0} li>details>summary>span.open,
.{0} li>details[open]>summary>span.closed {{
    display: none;
}}
.{0} li>details[open]>summary>span.open {{
    display: inline;
}}
.{0} li>details>summary {{
    display: block;
    cursor: pointer;
}}
</style>"""
            else:
                style = self.__style
        return (
            f'{style.format(treecls)}\n<ul class="{treecls}">\n{self.make_node(0)}'
            "\n</ul>"
        )

    def make_node(self, level: int, /) -> str:
        """Make a string representation of the current node."""
        if not self.__children:
            return f'<li class="{self.__nodecls}"><span>{self.__val}</span></li>'
        children_str = "\n".join(x.make_node(level + 1) for x in self.__children)
        if self.__val is None:
            return children_str
        details_open = " open" if level < self.__level_open else ""
        return (
            f'<li class="{self.__nodecls}"><details{details_open}><summary>{self.__val}'
            f'</summary>\n<ul class="{self.__nodecls}">\n{children_str}\n</ul>\n'
            "</details></li>"
        )

    def show(self, treecls: str | None = None, style: str | None = None) -> "HTMLRepr":
        """
        Show the html tree.

        Parameters
        ----------
        treecls : str | None, optional
            The class name of the tree, by default None.
        style : str | None, optional
            Css style, by default None.

        Returns
        -------
        HTMLRepr
            Represents an html object.

        """
        return HTMLRepr(self.make(treecls, style))

    def print(self, treecls: str | None = None, style: str | None = None) -> str:
        """
        Print the string representation of the html tree.

        Parameters
        ----------
        treecls : str | None, optional
            The class name of the tree, by default None.
        style : str | None, optional
            Css style, by default None.

        Returns
        -------
        StrRepr
            Represents a string.

        """
        return StrRepr(self.make(treecls, style))


class HTMLRepr:
    """Represents an html object."""

    def __init__(self, html_str: str, /) -> None:
        self.__html_str = html_str

    def _repr_html_(self) -> str:
        return self.__html_str


class StrRepr:
    """Represents a string."""

    def __init__(self, html_str: str, /) -> None:
        self.__html_str = html_str

    def __repr__(self) -> str:
        return self.__html_str
