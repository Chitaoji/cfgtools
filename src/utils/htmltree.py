"""Defines HTMLTreeMaker."""

from typing import Self

__all__ = ["HTMLTreeMaker"]


class HTMLTreeMaker:
    """
    Make an HTML tree.

    Parameters
    ----------
    name : str, optional
        Name of child node, by default None.


    """

    def __init__(self, name: str | None = None, /) -> None:
        self.name = name
        self.children: list[Self] = []

    def add(self, maybe_name: str | Self, /) -> Self:
        """
        Add a child node, and return it.

        Parameters
        ----------
        maybe_name : str | Self
            Name or instance of the child node.

        Returns
        -------
        Self
            The new node.

        """
        if isinstance(maybe_name, str):
            child = self.__class__(maybe_name)
        else:
            child = maybe_name
        self.children.append(child)
        return child

    # def discard(self, name: str, /) -> None:
    #     """Discard a child node."""
    #     if name not in self.children:
    #         raise ValueError(f"node {name!r} not found")
    #     del self.children[name]

    # def get(self, name: str, /) -> Self:
    #     """Get a child node."""
    #     if name not in self.children:
    #         raise ValueError(f"node {name!r} not found")
    #     return self.children[name]

    def set_name(self, name: str) -> Self:
        """Set node name."""
        self.name = name
        return self

    def make(self, class_name: str | None = None, style: str = "") -> str:
        """Make a string of the HTML tree."""
        if class_name is None:
            class_name = self.name
        return f"""{style}<ul class="{class_name}">
{self.make_plain()}
</ul>"""

    def make_plain(self) -> str:
        """Make a string of the HTML tree without style."""
        if not self.children:
            return f'<li class="m"><span>{self.name}</span></li>'
        children_str = "\n".join(x.make_plain() for x in self.children)
        if self.name is None:
            return children_str
        return f"""<li class="m"><details><summary>{self.name}</summary>
<ul class="m">
{children_str}
</ul>
</details></li>"""
