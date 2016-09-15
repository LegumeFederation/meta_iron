Metadata Attributes
===================

Columns other than the first column are for attributes.
``meta_iron`` will pass along as a string value any type of attribute with a valid
attribute identifier, but the following attributes require built-in parsing and handling and
are always defined:

==============  ================================================================================
Attribute       Description
==============  ================================================================================
value           Value or value expression to be associated with ``name``.
                For more discussion of value on input and output see the
                `values document <values.rst>`_.

type            A valid `metadata type <types.rst>`_, e.g. ``integer``.  Default is ``string``.

default         The default value.

label           A short printable label with caps, e.g. ``Genome Size``.  Required for
                definitions with ``execute`` attribute, but not required to be unique.

units           A units string, e.g. ``signatures/Mbp**2``.

min             Minimum value, produces an error if exceeded.

==============  ================================================================================

max             Maximum value, produces an error if exceeded.

precision       Number of digits beyond the decimal point for output of ``float`` types.

width           Width of the field in characters for output.  A warning will result if exceeded.

zeropad         Number of digits to zero-pad.

allowed_values  List of allowed values, useful for class variables.

description     A long description (usually as a sentence) suitable for tooltips.

evaluate        If ``True``, then ``value`` is derived from evaluating a Python expression.  See
                the document on `values <values.rst>`_.  ``evaluate`` attributes are not passed
                along to flattened output, since they only have meaning to ``meta_iron``.  Only
                one of ``evaluate`` and ``execute`` may be true or an error will result.

execute         If non-null then metadata is derived at the ``execute`` command from
                from running an external executable derived from evaluating the list expression defined
                in this attribute and parsing a dictionary of returned results.  The expression
                is evaluated last, after ``value`` may be defined.  All items returned in the
                dictionary will be defined in the current directory's metadata file.  Not exported.
                Obviously this mechanism is not safe for untrusted
                input files, so the ``--execute`` global switch must be used.  Only one of
                ``evaluate`` and ``execute`` may be true or an error will result.

append          If ``True``, will append to rather than override previous definitions of values
                for metadata of sequence type (``string``, ``list``, or ``dictionary``).

encoding        Encoding used for a string value.  Note that this applies only to the ``value``
                attribute and that the ``name`` and other attributes must be encoded with ``UTF-8``.

output          If ``True``, this value will not appear in output files.  Useful for internal-only
                metadata.  Not exported.

final           If ``True``, attempting to redefine this value will produce an error.

prototype       If ``True``, the name is a globbable pattern to be be used by the ``discover``
                command.

defined_by      The name of the ``execute`` command that was responsible for the definition.
                Not exported.

==============  ================================================================================

Each of these attributes corresponds to a column in metadata files.  The order of columns in metadata files
beyond the first column (which must be the name) is not important, and not all attributes need be present.
Attributes not defined here are simply passed along as string values without verification.