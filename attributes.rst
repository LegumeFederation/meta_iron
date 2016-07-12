Here is the complete list of attributes that meta_iron recognizes:

============== ===========
Attribute      Description
============== ===========
name           A string suitable for use as an identifier (as determined by python ``.isidentifier())``.
               This attribute is required and must be in column 1 of the input file.  If the name is not valid,
               a warning will be produced and the entry will be ignored.

type           A valid `metadata type <types.rst>`_, e.g. ``integer``.

value          A value, encoded as a string with encoding specified by ``encoding``, of type specified by ``type``
               that passes optional bounds checking specified by ``min`` and ``max``.  If the type conversion or
               bounds checking fails, a warning will be produced and the entry will be ignored.

label          A short printable label with caps, e.g. ``Genome Size``.

units          A units string, e.g. ``signatures/Mbp``.

index          A boolean, that if present and true, results in the value being indexed by the site indexer
              (e.g., IRODS metadata or Lucene).

format         Format for string values, default is ``txt`` for text, but could be ``md`` for markdown,
               ``rst`` for restructured text, or ``html`` for HTML.

encoding       Unicode encoding for the string and string-derived types.  Default is ``UTF-8``.

min            Minimum value, produces an error if exceeded.

max            Maximum value, produces an error if exceeded.

precision      Number of digits beyond the decimal point for ``float`` types.

width          Width of the field in characters for output.

allowed_values List of allowed values, useful for class variables.

description    A long description, as sentences, suitable for tooltips.  If of the form ``@filename``, where
               ``filename`` is a text file in the current directory, the description string is replaced by that file.

============== ===========

Each of these attributes corresponds to a column in metadata files.  The order of columns in metadata files is not important, and not all attributes need be present.  Attributes not defined here are simply passed along as string values without verification.
