Metadata Values
===============

Values are obtained by either overlaid replacement or appending if the
``append`` attribute is set. ``value`` is the last attribute to be calculated.
Values are calculated from files in order of directory tree traversal from root to working
directory and in order of appearance in a file. Multiple entries will result in
a warning being issued and the last value
being used.  Empty value strings will result in the value becoming undefined, if
previously defined.

Values are encoded as a Unicode strings. All input and output metadata files are required
to use the ``UTF-8`` encoding, but other files may use other encodings.

Input is checked to see if it passes type, bounds, allowed value, and path
existence checking.  Failure of any of these checks produces a fatal error.

For metadata of type ``path``, values inherited from directories above
the working directory will be replaced with the correct number of up-referenced values
(e.g., the path ``README.txt`` inherited from a directory one level above will become
``../README.txt``).


Literal Values
--------------
Values for sequence types must be interpretable as python literals.  This means
that strings must be in quotes.


Evaluated Values
----------------
If the ``evaluate`` attribute is set, the value string will be evaluated using
python syntax as defined by `asteval <http://newville.github.io/asteval/>`.
The symbol table will be taken from the metadata values that
have been defined up to that point, plus additional internal values:

============== =============
Symbol         Value
============== =============
date           The localized date string.

time           The local time in ``HH:MM:SS`` format.

node           Name of the computer on which ``meta_iron`` was run.

root           Relative path to the root directory.

depth          Integer depth of the current working directory from
               the root working directory.

bindir         Additional directory that will be prepended to path
               from environment before executing commands via
               ``execute`` attribute.  Set to ``root+'/bin'`` by
               default if that directory exists, but can be overridden
               by global switch if necessary.

user           Username associated with the ``meta_iron`` process.

meta_iron      Version string from ``meta_iron``.

self           Current metadata item name.

self.attribute Every `attribute <attributes.rst>`_ that is defined, including
               ``self.value`` are available for evaluation.

============== =============

Note that evaluated values must quote literals in either single
or double quotes or else the string will be interpreted as a symbol.

Output values
-------------
Values which are undefined at the level of the current working
directory are not output.


