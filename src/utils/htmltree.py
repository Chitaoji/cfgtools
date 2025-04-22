"""Defines HTMLTreeMaker."""

from typing import Self

__all__ = ["HTMLTreeMaker"]


class HTMLTreeMaker:
    """
    Make an HTML tree.

    Parameters
    ----------
    title : str, optional
        Title of child node, by default None.


    """

    def __init__(self, title: str | None = None, /) -> None:
        self.title = title
        self.children: dict[str, Self] = {}

    def add_node(self, title: str | None = None, /) -> Self:
        """
        Add a child node, and return it.

        Parameters
        ----------
        title : str, optional
            Title of child node, by default None.

        Returns
        -------
        Self
            The new node.

        """
        if title in self.children:
            raise ValueError(f"node {title!r} already exists")
        self.children[title] = self.__class__(title)

    def del_node(self, title: str | None = None, /) -> None:
        """
        Delete a child node.

        Parameters
        ----------
        title : str, optional
            Title of child node, by default None.

        """
        if title not in self.children:
            raise ValueError(f"node {title!r} not found")
        del self.children[title]

    def make(self, class_name: str | None = None, style: str = "") -> str:
        """Make a string of the HTML tree."""
        if class_name is None:
            class_name = self.title
        return f"""{style}<ul class="{class_name}">
{self.make_plain()}
</ul>"""

    def make_plain(self) -> str:
        """Make a string of the HTML tree without style."""
        if not self.children:
            return f"""<li class="m"><span>{self.title}</span></li>"""
