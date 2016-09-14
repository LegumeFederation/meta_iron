Metadata Encodings
==================

A distressing amount of scientific programs assume that ``UTF-8`` is the only character encoding that will ever be used,
but real metadata to be used in multiple countries needs support for other encodings.

``meta_iron`` looks for the name of the encoding as the first characters in the root metadata file.  The
encoding specified there (which *must* be in ``UTF-8`` encoding itself) becomes the default for all metadata files
to be opened.  This can be overridden at any level in the directory hierarchy by specifying a different encoding.
This makes it possible to, say, make the root metadata in ``UTF-8`` and lower branches to be in different encodings.

On input, the ``encoding`` attribute overrides default values.  Through use of the ``encoding``
 attribute, individual metadata values can use different encodings from the input metadata file itself.
The ``encoding`` attribute may be set for ``file`` and ``directory`` objects, and is intended to apply to the object
name, contents, and any results of scripts executed on those objects.

The ``encoding`` attribute may be set for ``file`` and ``directory`` objects, but applies to the values itself
(the file or directory name) not to any metadata derived from scripting. ``encoding`` attributes set in input files
 are final, overriding the defaults.


On output, the default encoding of the root metadata file will be written as the first metadata line as for input.
The general practice for  consumer programs will be to open the flattened metadata file with ``UTF-8`` encoding, and if
another encoding is used to re-open it with the proper encoding.
