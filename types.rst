Metadata Types
==============


The following atomic types are defined in meta_iron:

============== ==================
Type           Description
============== ==================
string         A UniCode string using the encoding specified in the ``encoding`` attribute.
               If the string is of the form ``@path`` where ``path`` is a file path as defined below, the value
               will be replaced with the contents of the file.  This is useful for long strings that may include
               multiple lines.

URL            A string that is a valid URL, e.g., ``http://legumefederation.org``.

version        A string that is a valid version specifier, e.g., ``v0.1a1``.  Must begin with ``v``.

OID            A string that is a valid Object ID, e.g. ``LegFed000124v2.2``.

path           A string that is a valid path to a file relative to the current directory e.g., ``subdir/README.txt``.
               Absolute paths are not allowed, nor are paths that refer to directories above the current directory.
               Path separators must always be specified with ``/``, regardless of OS convention.

integer        An integer value.   Internal representation is ``BigInt`` and not limited in size.

float          A floating-point value, possibly with exponent e.g., ``1.0E-10``.

boolean        A boolean value.  Valid values on input are any of the following, without regard to capitalization:
               ``true false t f yes no y n 1 0``.  On output only ``true`` or ``false`` are used..
============== ==================

List types is defined on these atomic types by adding ``_list`` to the atomic type names, e.g., ``integer_list``.
Commas will be used as list item separators on ``value`` strings.
There is no quoting mechanism for commas in string lists.