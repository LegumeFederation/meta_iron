Metadata Attributes
===================


Here is the complete list of built-in that meta_iron recognizes:

============== ================================================================================
Attribute      Description
============== ================================================================================
name           A string suitable for use as an identifier (no white spaces, limits on special
               characters. This attribute is required and must be in column 1 of the input
               file. If the name is not valid, processing will stop and an error message
               will be issued.  Duplicate names will result in a warning, with the attributes
               of the last value being used.

type           A valid `metadata type <types.rst>`_, e.g. ``integer``.

value          A value, encoded as a Unicode string with encoding specified by ``encoding``,
               of type specified by ``type`` that passes optional bounds checking specified by
               ``min`` and ``max``. If the type conversion or bounds checking fails, an error
               will be produced and processing stops.

label          A short printable label with caps, e.g. ``Genome Size``.

units          A units string, e.g. ``signatures/Mbp``.

encoding       Unicode encoding for the string and string-derived types.  Default is ``UTF-8``.

min            Minimum value, produces an error if exceeded.

max            Maximum value, produces an error if exceeded.

precision      Number of digits beyond the decimal point for output of ``float`` types.

width          Width of the field in characters for output.

allowed_values List of allowed values, useful for class variables.

description    A long description, as sentences, suitable for tooltips.  If of the form
               ``@filename``, where ``filename`` is a text file in the current directory,
               the description string is replaced by the contents of that file.

============== ================================================================================

Each of these attributes corresponds to a potential column in metadata files.  The order of columns in metadata files
beyond the first column (which must be the name) is not important, and not al l attributes need be present.
Attributes not defined here are simply passed along as string values without verification.