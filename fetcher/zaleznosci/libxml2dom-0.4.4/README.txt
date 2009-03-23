Introduction
------------

See docs/index.html for the libxml2dom documentation.

Compatibility Warnings
----------------------

From libxml2dom 0.4, nodeValue now returns different results in some cases.
Previously, it was possible to get the textual contents of an element using
the nodeValue property, although this is incompatible with the DOM
specifications. Instead, you should now use the textContent property to get
such data.

Contact, Copyright and Licence Information
------------------------------------------

The current Web page for libxml2dom at the time of release is:

http://www.boddie.org.uk/python/libxml2dom.html

Copyright and licence information can be found in the docs directory - see
docs/COPYING.txt, docs/lgpl-3.0.txt and docs/gpl-3.0.txt for more information.

Dependencies
------------

libxml2     Tested with libxml2 2.6.17.
            Use --with-python=<path to python executable> if building from
            source. Previous releases of libxml2 in the 2.6 series may work,
            but releases before 2.6.16 are not recommended.

            For Windows users, see also the packages for libxml2, available
            from the following site:

            http://users.skynet.be/sbi/libxml-python/

Python      Tested with Python 2.4.
            Python releases from 2.2 onwards should be compatible with
            libxml2dom. The principal requirement from such releases is the
            new-style class support which permits the use of properties in
            the libxml2dom implementation.

Testing
-------

Some of the tests require libxml2macro.py to be run on the test source code
first. Read the docstrings for the various test files before attempting to run
any of them. See also docs/NOTES_libxml2macro.txt for more information. Note
that such tests are retained for historical purposes and/or curiosity since
libxml2macro.py is no longer supported.

Issues
------

The presence of xmlns attributes in serialised documents was called into
question, and the tests/namespace*.py files attempt to show the current
behaviour of libxml2dom.

Use of importNode seems to cause some kind of memory issue, probably related
to nodes being shared across documents. This was observed in libxml2 2.6.0 but
appears to be fixed in libxml2 2.6.16.

Even compared to minidom, importNode may seem very slow (even the
libxml2dom.macrolib implementation, too). A way is needed to get libxml2 to do
the node copying itself.

New in libxml2dom 0.4.4 (Changes since libxml2dom 0.4.3)
--------------------------------------------------------

  * Relicensed under the LGPL version 3 or later (fixing PKG-INFO file).
  * Improved XMPP support for messages, presence and events.
  * Added Ubuntu Feisty (7.04) package support.

New in libxml2dom 0.4.3 (Changes since libxml2dom 0.4.2)
--------------------------------------------------------

  * Enforced well-formedness in parse operations unless otherwise requested.
  * Fixed access to null doctype properties.
  * Added getElementById, firstChild and lastChild to the Node class.
  * Added a __hash__ method to the Node class.
  * Moved document checking into the Node class.
  * Added an iterator for the NamedNodeMap class.
  * Expanded the svg and events modules, including a test of SVG events.
  * Split the debian-stable packages into debian-sarge and debian-etch.

New in libxml2dom 0.4.2 (Changes since libxml2dom 0.4.1)
--------------------------------------------------------

  * Added missing impl attribute to NamedNodeMap, fixing attribute retrieval.
  * Added documentElement to Document.
  * Fixed and expanded the events module.
  * Added lots of functionality to the svg module.

New in libxml2dom 0.4.1 (Changes since libxml2dom 0.4)
------------------------------------------------------

  * Fixed the absence of CDATA node creation and importing.

New in libxml2dom 0.4 (Changes since libxml2dom 0.3.6)
------------------------------------------------------

  * Changed the nodeValue property to return None for various node types, as
    specified in the DOM specification (Level 3).
  * Fixed various "not supported" exceptions and added tests which can raise
    "wrong document" exceptions.
  * Introduced an Implementation class, permitting specialised node creation.
  * Added SVG-specific document support.
  * Made parseURI work for HTML documents.
  * Fixed getElementsByTagName(NS), as reported by Christian Seiler.
  * Fixed previousSibling, nextSibling and parentNode crashes using
    suggestions from Christian Seiler.
  * Reintroduced node comparisons using suggestions from Christian Seiler.
  * Fixed the absence of the CDATA node type.
  * Added the textContent property to nodes.
  * Added a getDOMImplementation function.
  * Added an experimental events module.
  * Added an htmlencoding parameter to the parse functions, as requested by
    Iliyan Peychev.

New in libxml2dom 0.3.6 (Changes since libxml2dom 0.3.5)
--------------------------------------------------------

  * Added cloneNode almost as a synonym for importNode (which, unlike in the
    DOM specification, is present on all nodes).
  * Introduced Debian stable package details - suggested by Robert Siemer.
  * Changed libxml2mod import details to try libxmlmods - suggested by Lucian
    Wischik.

New in libxml2dom 0.3.5 (Changes since libxml2dom 0.3.4)
--------------------------------------------------------

  * Fixed nodeType for HTML document elements - reported by Robert Siemer.
  * Fixed string results from XPath expressions - reported by Robert Siemer.

New in libxml2dom 0.3.4 (Changes since libxml2dom 0.3.3)
--------------------------------------------------------

  * Attempted to introduce generated prefixes for attributes having namespaces
    but whose names are unprefixed.
  * Added support for xmlns attribute retrieval (getAttributeNS) and detection
    (hasAttributeNS).
  * Added the length attribute to NamedNodeMap; renamed the length method on
    NodeList, adding a length attribute.

New in libxml2dom 0.3.3 (Changes since libxml2dom 0.3.2)
--------------------------------------------------------

  * Removed redundant weakref usage.
  * Added explicit copyright and licensing information to source files.

New in libxml2dom 0.3.2 (Changes since libxml2dom 0.3.1)
--------------------------------------------------------

  * Improved the xmlns attribute creation controls.

New in libxml2dom 0.3.1 (Changes since libxml2dom 0.3)
------------------------------------------------------

  * Fixed empty namespace declarations on elements created with namespaceURI
    set to None. Previously, such declarations were missing.
  * Fixed attribute creation and introduced stricter controls over the
    construction of xmlns attributes.

New in libxml2dom 0.3 (Changes since libxml2dom 0.2.4)
------------------------------------------------------

  * Imposed much stricter tests on strings used with the libxml2dom API.
    Strings given as arguments to methods and functions must now only contain
    ASCII characters; any other character data must be provided as Unicode
    objects. This change fixes various issues with XPath expressions, and
    quite probably various other things.
  * Fixed parentNode on Document objects (which caused xml.dom.ext.PrettyPrint
    to crash).
  * Added some support for the doctype attribute and related information.
  * libxml2dom is now licensed under the LGPL - see docs/COPYING.txt for
    details.

New in libxml2dom 0.2.4 (Changes since libxml2dom 0.2.3)
--------------------------------------------------------

  * Fixed Unicode conversions in the Node's xpath method.

New in libxml2dom 0.2.3 (Changes since libxml2dom 0.2.2)
--------------------------------------------------------

  * Fixed the parse function's docstring.
  * Added the owner element to obtained attribute nodes.
  * Fixed Debian package changelog distribution identifiers.

New in libxml2dom 0.2.2 (Changes since libxml2dom 0.2.1)
--------------------------------------------------------

  * Fixed exception raising in parseURI, adding a docstring to explain the
    current limitations around HTML parsing.

New in libxml2dom 0.2.1 (Changes since libxml2dom 0.2)
------------------------------------------------------

  * Moved libxml2macro script to the tools directory.
  * Added getElementsByTagNameNS.
  * Added a normalize implementation.
  * Added HTML parsing support.
  * Added prettyprinting support.
  * Fixed parseURI.
  * Introduced better testing for Unicode objects, especially since things
    like rdflib like to subclass the unicode type, and it might be more
    convenient to detect such subclasses and convert their values
    automatically.
  * Improved some of the API documentation.
  * Introduced better suppression of warnings, network access, and other
    potentially intrusive libxml2 features.
  * Reorganised the documentation, expanding the README.txt file at the
    expense of the HTML documentation, but removing older, less relevant
    information.
  * Added Debian package support.

New in libxml2dom 0.2 (Changes since libxml2dom 0.1.3)
------------------------------------------------------

  * Adopted libxml2macro code within the libxml2dom classes, removing any
    dependencies on the libxml2 module - this makes everything much faster
    and virtually removes any necessity to use libxml2macro.
  * Improved attribute and document node handling.
  * Introduced document reference management.
  * Introduced NodeList wrapper objects.

New in libxml2dom 0.1.3 (Changes since libxml2dom 0.1.2)
--------------------------------------------------------

  * Fixed createElement.
  * Introduced experimental libxml2macro tools, tests and libraries.

New in libxml2dom 0.1.2 (Changes since libxml2dom 0.1.1)
--------------------------------------------------------

  * Fixed getAttributeNode and getAttributeNodeNS.
  * Added comment node creation.
  * Fixed empty namespace usage with elements and attributes.
  * Introduced usage of the libxml2 file and memory parsing features.
  * Introduced suppression of DTD retrieval and validation as the default
    behaviour.
  * Added experimental XPath method support.

New in libxml2dom 0.1.1
-----------------------

  * Fixed text node creation.
  * Fixed setAttributeNS.
  * Added encoding parameters to convenience methods.
  * Added the missing previousSibling property.
  * Added release number to the package.

Release Procedures
------------------

Update the libxml2dom/__init__.py and libxml2dom/macrolib/__init__.py
__version__ attributes.
Change the version number and package filename/directory in the documentation.
Change code examples in the documentation if appropriate.
Update the release notes (see above).
Update the package release notes (in the packages directory).
Check the setup.py file and ensure that all package directories are mentioned.
Check the release information in the PKG-INFO file.
Tag, export.
Archive, upload.
Make packages (see below).
Update PyPI, PythonInfo Wiki, Vaults of Parnassus entries.

Making Packages
---------------

To make Debian-based packages:

  1. Create new package directories under packages if necessary.
  2. Make a symbolic link in the distribution's root directory to keep the
     Debian tools happy; choose one of the following:

     ln -s packages/ubuntu-hoary/python2.4-libxml2dom/debian/
     ln -s packages/debian-sarge/python2.3-libxml2dom/debian/
     ln -s packages/debian-etch/python-libxml2dom/debian/

  3. Run the package builder:

     dpkg-buildpackage -rfakeroot

  4. Locate and tidy up the packages in the parent directory of the
     distribution's root directory.
