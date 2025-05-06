"""
Contains css styles.

NOTE: this module is private. All functions and objects are available in the main
`cfgtools` namespace - use that instead.

"""

__all__ = []

TREE_CSS_STYLE = """<style type="text/css">
.cfgtools-tree li.m {
    display: block;
    position: relative;
}
.cfgtools-tree li.m>details>summary {
    display: block;
    cursor: pointer;
}
.cfgtools-tree ul.m {
}
</style>"""
