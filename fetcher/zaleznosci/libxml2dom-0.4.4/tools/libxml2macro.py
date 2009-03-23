#!/usr/bin/env python

import compiler
import marshal, imp, os, stat, struct

# Originally from Analysis/Writers/Python.

def write_module(module, source_filename, target_filename, syntax_check=1):

    """
    Write the given 'module', associated with the given 'source_filename', to a
    file with the given 'target_filename'. The optional 'syntax_check' flag (set
    by default) ensures that the module is syntactically correct.
    """

    if syntax_check:
        compiler.syntax.check(module)
    compiler.misc.set_filename(source_filename, module)
    generator = compiler.pycodegen.ModuleCodeGenerator(module)
    f = open(target_filename, "wb")
    f.write(get_header(source_filename))
    marshal.dump(generator.getCode(), f)
    f.close()

def get_header(filename):

    "Taken from compiler.pycodegen. Prepare the compiled module header."

    MAGIC = imp.get_magic()
    mtime = os.stat(filename)[stat.ST_MTIME]
    mtime = struct.pack('<i', mtime)
    return MAGIC + mtime

# Processing functions.

def process_nodes(root_node, prefix=None):

    """
    Under the 'root_node', process all suitable expression nodes which employ
    special names using the given 'prefix'.
    """

    for node in root_node.getChildNodes():

        # Find imports and discover if they are really used to define the
        # special prefix.

        if isinstance(node, compiler.ast.Import):
            prefix = process_import(node, root_node) or prefix

        # Identify suitable names and add replacement nodes.

        elif isinstance(node, compiler.ast.CallFunc):
            process_callfunc(node, prefix)
        elif isinstance(node, compiler.ast.Getattr):
            process_getattr(node, prefix, root_node)
        else:
            process_nodes(node, prefix)

def process_import(node, parent):

    """
    Process the Import 'node' searching for the special incantation required to
    set the prefix. Remove compliant nodes from their 'parent' node. If no new
    prefix is found, return None.
    """

    for name, alias in node.names:
        if name == "libxml2macro":

            # Remove this node from its parent.

            parent.nodes.remove(node)
            return alias

    return None

def process_callfunc(node, prefix):

    """
    Process the CallFunc 'node' searching for special names with the given
    'prefix'.
    """

    # Check the prefix.

    if prefix is None:
        return

    # Check the target.

    target = node.node
    if isinstance(target, compiler.ast.Getattr):
        if process_getattr(target, prefix, node):

            # Process all sibling arguments of the new first argument, too.

            process_callfunc_args(node, prefix, start_index=1)

        else:
            process_callfunc_args(node, prefix)

    else:
        process_callfunc_args(node, prefix)

def process_callfunc_args(node, prefix, start_index=0):

    """
    Process the arguments of the given CallFunc 'node' searching for special
    names with the given 'prefix'. The optional 'start_index' is used to
    indicate the first argument to be processed.
    """

    for index in range(start_index, len(node.args)):
        arg = node.args[index]
        if isinstance(arg, compiler.ast.Getattr):
            process_getattr(arg, prefix, node, index=index)

def process_getattr(node, prefix, parent, index=None):

    """
    Process the Getattr 'node' searching for special names with the given
    'prefix', using the given 'parent' to add transformed expressions in place
    of the original ones.

    The optional 'index' is used when arguments of CallFunc nodes are being
    processed and where a replacement of such arguments is occurring.
    """

    # Check the prefix.

    if prefix is None:
        return

    # Detected cases:
    # node.attr plus node.attr.attr
    # (obj.node).attr plus (obj.node).attr.attr
    # Note that the deep cases are dealt with first using a recursive call.

    if getattr_has_prefix(node, prefix) or \
        isinstance(node.expr, compiler.ast.Getattr) and propagated_prefix(process_getattr(node.expr, prefix, node)):

        # Replace CallFunc plus Getattr occurrences:
        # node.attr(args) -> Node_attr(node, args)
        # fn(node.attr) -> fn(Node_attr(node))

        if isinstance(parent, compiler.ast.CallFunc):

            # If this node is not an argument, transform the call.

            if index is None:
                parent.node = compiler.ast.Name("Node_%s" % node.attrname)
                parent.args.insert(0, node.expr)

            else:
                replacement = compiler.ast.CallFunc(
                    compiler.ast.Name("Node_%s" % node.attrname),
                    [node.expr]
                    )
                parent.args[index] = replacement

        # Replace plain Getattr nodes:
        # node.attr -> Node_attr(node)
        # NOTE: Nasty but necessary rewiring of the parent node required.

        else:
            replacement = compiler.ast.CallFunc(
                compiler.ast.Name("Node_%s" % node.attrname),
                [node.expr]
                )
            for key, value in parent.__dict__.items():
                # Detect lists.
                if hasattr(value, "__len__") and node in value:
                    index = value.index(node)
                    value[index] = replacement
                elif value is node:
                    parent.__dict__[key] = replacement

        # Propagate whether the kind of result might need transforming itself.

        return node.attrname

    else:
        process_nodes(node, prefix)
        return None

def propagated_prefix(attrname):

    """
    Return whether the given 'attrname' used in a transformation should be
    considered significant at the parent level.
    """

    return attrname in ("ownerElement", "ownerDocument")

def getattr_has_prefix(node, prefix):

    """
    Determine whether the given Getattr 'node' employs the special 'prefix' in a
    number of ways.
    """

    # Check the expression as a simple name:
    # node.attr

    if isinstance(node.expr, compiler.ast.Name) and node.expr.name.startswith(prefix):
        return 1

    # Check the attribute name of child expressions:
    # (obj.node).attr

    elif isinstance(node.expr, compiler.ast.Getattr) and node.expr.attrname.startswith(prefix):
        return 1
    else:
        return 0

def include_import(module):

    """
    Include an import statement in 'module' to make the macro library available.
    """

    module.node.nodes.insert(0, compiler.ast.From("libxml2dom.macrolib", [("*", None)]))

def process_file(filename):

    """
    Process the module given by the specified 'filename'. The optional special
    'prefix' marks those variables to be processed.
    """

    # Open the module as an AST.

    module = compiler.parseFile(filename)

    # Find references to special variables.

    process_nodes(module)

    # Add necessary imports.

    include_import(module)

    # Write the module.

    write_module(module, filename, os.path.splitext(filename)[0] + ".pyc")
    return module

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print "libxml2macro.py <module-filename>"
        sys.exit(1)
    process_file(sys.argv[1])

# vim: tabstop=4 expandtab shiftwidth=4
