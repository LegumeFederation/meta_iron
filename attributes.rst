Metadata Attributes
===================


``meta_iron`` will pass along as a string value any type of attribute with a valid
attribute identifier, but certain attributes require special parsing and handling.
Here is the complete list of built-in that meta_iron recognizes:

============== ================================================================================
Attribute      Description
============== ================================================================================
name           A string that matches the regular expression ``[a-zA-Z_.][a-zA-Z0-9_.]*`` (i.e.
               no white spaces are allowed. The ``name`` attribute is the only required
               attribute and must be in column 1 of the input
               file. If the name is not valid, processing will stop and an error message
               will be issued.  Duplicate names in a file will result in a warning,
               with definitions overlayed and values from the last occurrance being final.
               If ``name`` begins with a ``.``,  there is an implied wildcard at the
               beginning and all metadata with the ending will have those attribute
               definitions, e.g. the attributes of ``.date`` will apply to ``genome_file.date``
               or any other name that ends in ``.date``.

value          Value or value expression to be associated with ``name``.
               For more discussion of value on input and output see the
               `values document <values.rst>`_.

type           A valid `metadata type <types.rst>`_, e.g. ``integer``.


label          A short printable label with caps, e.g. ``Genome Size``.

units          A units string, e.g. ``signatures/Mbp**2``,

uncertainty    Uncertainty for numeric values.

min            Minimum value, produces an error if exceeded.

max            Maximum value, produces an error if exceeded.

precision      Number of digits beyond the decimal point for output of ``float`` types.

width          Width of the field in characters for output.

zeropad        Number of digits to zero-pad.

allowed_values List of allowed values, useful for class variables.

description    A long description (usually as a sentence) suitable for tooltips.

notes          Information such as provenance or creation date that should be kept but
               not necessarily displayed.

required       If ``True``, then this field must be defined or a fatal error will result.

evaluate       If ``True``, then ``value`` is derived from evaluating a Python expression.  See
               the document on `values <values.rst>`_.  ``evaluate`` attributes are not passed
               along to flattened output, since they only have meaning to ``meta_iron``.  Only
               one of ``evaluate`` and ``execute`` may be true or an error will result.

execute        If ``True`` then and ``executed`` has not been set, then metadata is derived
               from running an external executable derived from evaluating the expression defined
               in this attribute and parsing a dictionary of returned results.  The expression
               is evaluated last, after ``value`` may be defined.  All items returned in the
               dictionary will be defined in the directory metadata file, which gets updated and
               reparsed before the next item is evaluate.  Dictionary items
               which begin with ``self`` will have ``self`` replaced with the name of the current
               field. This provides a flexible mechanism for scriptable
               filling of metadata. For example ``self.date`` when run with a value of `genome_file``
               will result in ``genome_file.data`` becoming defined.
               Values retured by this dictionary supersede any values defined
               in the directory metadata file.  The directory metadata file will be modified
               with values set, so that execution happens once only.  All values defined in
               the returned dictionary will be set, even if they have not been previously set.
               ``execute`` attributes are not passed along to flattened output, since they only
               have meaning to ``meta_iron``.  Obviously this mechanism is not safe for untrusted
               input files, so the ``--execute`` global switch must be used.  Only one of
               ``evaluate`` and ``execute`` may be true or an error will result.

executed       If ``True``, value has been set from the results of an ``execute`` command.
               This mechanism is used to get once-only evaluation.

append         If ``True``, will append to rather than override previous definitions of values
               for metadata of sequence type (``string``, ``list``, or ``dictionary``).

no_export      If ``True``, this value will not appear in output files.  Useful for internal-only
               metadata.

defined_at     This is an internal attribute that shows the directory level at which the
               value was defined.  This value is not directly settable and is not output
               except in diagnostic output of ``meta_iron``.

============== ================================================================================

Each of these attributes corresponds to a potential column in metadata files.  The order of columns in metadata files
beyond the first column (which must be the name) is not important, and not al l attributes need be present.
Attributes not defined here are simply passed along as string values without verification.