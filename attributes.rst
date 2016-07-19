Metadata Attributes
===================


``meta_iron`` will pass along as a string value any type of attribute with a valid
attribute identifier, but certain attributes require special parsing and handling.
Here is the complete list of built-in that meta_iron recognizes:

============== ================================================================================
Attribute      Description
============== ================================================================================
name           A string that matches the regular expression ``[a-zA-Z_][a-zA-Z0-9_]*`` (i.e.
               no white spaces are allowed. The ``name`` attribute is the only required
               attribute and must be in column 1 of the input
               file. If the name is not valid, processing will stop and an error message
               will be issued.  Duplicate names in a file will result in a warning,
               with definitions overlayed and values from the last occurrance being final.

type           A valid `metadata type <types.rst>`_, e.g. ``integer``.

value          A value,

label          A short printable label with caps, e.g. ``Genome Size``.

units          A units string, e.g. ``signatures/Mbp**2``, parsed using the
               `pint <https://pint.readthedocs.io/>`_ package.  Besides the usual SI units,
               this package has been extended to include the following genomics terms and
               abbreviations:
               ``base pairs (bp), chromosome (chr), event (evt), generation (gen), genome (gn),
               individual (indv), Morgans (M),  operational taxonomic units (OTU),
               phylogenetic units (PU), population (pop), recombination (recomb),
               substitution (sub)``.

uncertainty    Uncertainty for numeric values.

min            Minimum value, produces an error if exceeded.

max            Maximum value, produces an error if exceeded.

precision      Number of digits beyond the decimal point for output of ``float`` types.

width          Width of the field in characters for output.

zeropad        Number of digits to zero-pad.

allowed_values List of allowed values, useful for class variables.

description    A long description (usually as a sentence) suitable for tooltips.

evaluate       If ``True``, then evaluate the expression rather than treat it as a literal.  See
               the document on `values <values.rst>`_.  ``evaluate`` attributes are not passed
               along to flattened output, since they only have meaning to ``meta_iron``.

============== ================================================================================

Each of these attributes corresponds to a potential column in metadata files.  The order of columns in metadata files
beyond the first column (which must be the name) is not important, and not al l attributes need be present.
Attributes not defined here are simply passed along as string values without verification.