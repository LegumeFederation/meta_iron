Metadata Values
===============

Values are obtained by either overlaid replacement or evaluation using
`asteval <http://newville.github.io/asteval/>`_ if the `evaluate` attribute is set.
Value is the last attribute to be calculated.  Values are calculated in order
of directory tree traversal from root to working directory and
in order of appearance in a file. Multiple entries will result in the last value
being used.  Empty value strings will result in the value being undefined and undefined
metadata values are not output.

Values are encoded as a Unicode strings (all input and output metadata files are required
to use the ``UTF-8`` encoding, but other files may use other encodings)
of type specified by ``type`` that passes optional bounds checking specified by
``min`` and ``max``. If the type conversion or bounds checking fails, an error
will be produced and processing stops.

For overlaid replacement, the value is the one most recently encountered by traversal
from the root. For metadata of type ``path``, values inherited from directories above
the working directory will be replaced with the correct number of up-referenced values
(e.g., the path ``README.txt`` inherited from a directory one level above will become
``../README.txt``).

For evaluated values, the symbol table will be taken from the metadata values that
have been defined up to that point, plus additional internal values: ``date, time,
node, user, metairon_version``.
