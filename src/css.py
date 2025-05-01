"""
Contains css styles.

NOTE: this module is private. All functions and objects are available in the main
`cfgtools` namespace - use that instead.

"""

TREE_CSS_STYLE = """<style type="text/css">
.cfgtools-tree,
.cfgtools-tree ul.m,
.cfgtools-tree li.m {
    margin: 0;
    padding: 0;
    position: relative;
}
.cfgtools-tree {
    margin: 0 0 1em;
    text-align: center;
}
.cfgtools-tree,
.cfgtools-tree ul.m {
    display: table;
}
.cfgtools-tree ul.m {
    width: 100%;
}
.cfgtools-tree li.m {
    display: table-cell;
    padding: .5em 0;
    vertical-align: top;
}
.cfgtools-tree ul.s,
.cfgtools-tree li.s {
    text-align: left;
}
.cfgtools-tree li.m:before {
    outline: solid 1px #666;
    content: "";
    left: 0;
    position: absolute;
    right: 0;
    top: 0;
}
.cfgtools-tree li.m:first-child:before {
    left: 50%;
}
.cfgtools-tree li.m:last-child:before {
    right: 50%;
}
.cfgtools-tree li.m>details>summary,
.cfgtools-tree li.m>span {
    border: solid .1em #666;
    border-radius: .2em;
    display: inline-block;
    margin: 0 .2em .5em;
    padding: .2em .5em;
    position: relative;
}
.cfgtools-tree li>details>summary { 
    white-space: nowrap;
}
.cfgtools-tree li.m>details>summary {
    cursor: pointer;
}
.cfgtools-tree li.m>details>summary>span.open,
.cfgtools-tree li.m>details[open]>summary>span.closed {
    display: none;
}
.cfgtools-tree li.m>details[open]>summary>span.open {
    display: inline;
}
.cfgtools-tree ul.m:before,
.cfgtools-tree li.m>details>summary:before,
.cfgtools-tree li.m>span:before {
    outline: solid 1px #666;
    content: "";
    height: .5em;
    left: 50%;
    position: absolute;
}
.cfgtools-tree ul.m:before {
    top: -.5em;
}
.cfgtools-tree li.m>details>summary:before,
.cfgtools-tree li.m>span:before {
    top: -.56em;
    height: .45em;
}
.cfgtools-tree>li.m {
    margin-top: 0;
}
.cfgtools-tree>li.m:before,
.cfgtools-tree>li.m:after,
.cfgtools-tree>li.m>details>summary:before,
.cfgtools-tree>li.m>span:before {
    outline: none;
}
</style>"""
