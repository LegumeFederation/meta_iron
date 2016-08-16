Metadata Types
==============
``meta_iron`` recognizes both atomic and list types.

Atomic Types
------------
The following atomic types are defined in ``meta_iron``.  Any attempt to use types other than
these will result in a fatal error.

============== ================================================================================
Type           Description
============== ================================================================================
string         A Unicode string value encoded as UTF-8.

integer        An integer value.   Internal representation is ``BigInt`` and not limited in
               size.

float          A floating-point value, possibly with exponent e.g., ``1.0E-10``.

boolean        A boolean value.  Valid values on input are any of the following, without regard
               to capitalization: ``true false t f yes no y n on off 1 0``.  On output only
               ``True`` or ``False`` are used.

list           A list of values enclosed in ``[]`` and separated by commas.  Unless the
               ``evaluate`` attribute is set, items with string values must be quoted
               by single or double quotation marks.  Commas and non-printable
               characters may also be quoted for evaluation by python. Types are inferred
               and may be mixed in the list. For example, ``["Mark's age", 42]``.

dictionary     A dictionary of values enclosed in ``{}`` with python syntax,
               e.g., ``{'phylum': 'Streptophyta', 'genus': 'Glycine'}``.  Item order is
               preserved on output.

version        A string that is a valid version specifier, e.g., ``0.1a1`` as per python's
               `distutils.version.StrictVersion
               <http://epydoc.sourceforge.net/stdlib/distutils.version.StrictVersion-class.html>`_.
               Must *not* begin with ``v``.

identifier     A valid identifier (as determined by `python identifiers
               <https://docs.python.org/3.5/reference/lexical_analysis.html#identifiers>`_.
               E.g., must not contain whitespace or special characters that can be confused
               with operators.

units          A string that is interpretable by `Pint <https://pint.readthedocs.io/en/0.7.2/>`_
               as a valid unit.

date           An ISO date field.

OID            A string that is a valid Object ID, e.g. ``LegFed000124v2.2``.

file           A string that is a valid path to a file relative to the current directory
               e.g., ``subdir/README.txt``.  Absolute paths are not allowed.

URL            A string that is a valid URL, e.g., ``http://legumefederation.org``.

fileURL        A list consisting of a ``path`` followed by a ``URL``, intended to be
               different transport methods of reaching the same resource, e.g.,
               ''["README.txt", "http://legumefederation.org/somepath/README.txt"]``.
               `fileURL`` types are designed to hold off the decision of which transport
               to be used until packaging time, when the packager will take the faster
               ``file`` component if the file is in the scope of the package, and the
               universal ``URL`` component otherwise.

directory      A string that is a valid path to a directory relative to the current directory,
               e.g., ``subdir/subsubdir/``.  Trailing slash is optional on input but will be
               appended on output.  Absolute paths are not allowed.

============== ================================================================================

Derived _list types
-------------------
There are many situations in which lists are made of elements all of a single type. e.g., a
list of files.  It is desirable to have type and bounds checking on such lists.  For that
reason we have a set of list types denoted by ``TYPE_list`` where ``TYPE`` is one of the
atomic types listed above.  For example, a ``directory_list`` entry might be of the form
``["assembly_v3/", "assembly_v2/", "assembly_v3/"]`.


Notes on paths
--------------
Path separators must always be specified with ``/``, regardless of OS convention.  Paths
that cannot be resolved at compilation time will result in a warning message.
Upward reference with ``..`` *is* allowed by meta_iron, but may be a bad idea for packaging
reasons if the file ends up outside the archive space; consider hosting the file and using the
``fileURL`` list type instead.



