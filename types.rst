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
               to capitalization: ``true false t f yes no y n on off 1 0``.  On output only ``True``
               or ``False`` are used.

version        A string that is a valid version specifier, e.g., ``0.1a1`` as per python's
               `distutils.version.StrictVersion
               <http://epydoc.sourceforge.net/stdlib/distutils.version.StrictVersion-class.html>`_.
               Must *not* begin with ``v``.

identifier     A valid identifier (as determined by `python identifiers
               <https://docs.python.org/3.5/reference/lexical_analysis.html#identifiers>`_.
               E.g., must not contain whitespace or special characters that can be confused
               with operators.

unit           A string that is interpretable by `Pint <https://pint.readthedocs.io/en/0.7.2/>`_
               as a valid unit.

URL            A string that is a valid URL, e.g., ``http://legumefederation.org``.

OID            A string that is a valid Object ID, e.g. ``LegFed000124v2.2``.

file           A string that is a valid path to a file relative to the current directory
               e.g., ``subdir/README.txt``.

directory      A string that is a valid path to a directory relative to the current directory,
               e.g., ``subdir/subsubdir/``.  Trailing slash is optional.

============== ================================================================================

Notes on paths
--------------
Absolute paths are not allowed.  Upward reference with ``..`` *is* allowed by meta_iron,
but may be a bad idea for packaging reasons; consider hosting the file and using a URL instead.
Path separators must always be specified with ``/``, regardless of OS convention.  Paths
that cannot be resolved at compilation time will result in a warning message.

List Types
----------
List types is defined on these atomic types by adding ``_list`` to the atomic type names, e.g.,
``integer_list``. Semicolons (``;``) are used as list item separators on ``value`` strings.
There is no quoting mechanism for semicolons in string lists.