Flatten and smooth descriptive metadata
=======================================

meta_iron is a scriptable tool that creates, reads,and writes hierarchical descriptive metadata


What is descriptive metadata?
-----------------------------

Metadata is data about other data, and it comes in two flavors: *structural metadata*
which characterizes containers and content and *descriptive metadata* which characterizes the
provenance, statistics, and purpose of the data. Structural metadata is typically
addressed by packaging mechanisms such as tarballs, checksums, and
the `BagIt <https://en.wikipedia.org/wiki/BagIt>`_ format. Descriptive metadata can be
thought of (at its simplest) as a set of key:value pairs
(e.g., ``genome_size: 3.1 Gbp``), but even this simple example shows the
challenge because of domain-specific issues of units and naming. Good
descriptive metadata make life easier for both data publisher and data
consumer by improving data discovery, reproducibility, and reusability.
There are numerous challenges in dealing gracefully with descriptive metadata.

Issues meta_iron addresses
----------------------------
The following issues were deemed to be critical and not addressed by existing software tools:

============== =================================================================================
Issue          Description of Issue
============== =================================================================================
Accessible     Consumers need to generate and parse metadata regardless of
               whether they are human or software, which computer language or editor they
               prefer, whether they are running in the browser or a standalone environment,
               whether served dynamically or are downloaded as static files.  We have
               chosen to use the widely-accepted TSV_ as an input format for access reasons.
               Output of flattened metadata can be to TSV, JSON, or YAML.

Hierarchical   Metadata is hierarchical in nature, and is reflected in a directory tree.
               Metadata may be may be undefined at some levels of the hierarchy
               and re-defined at others.  Consumers need to be able to
               access metadata from any part of a hierarchy without having to
               download and parse the higher levels.  This implies metadata needs
               to be *flattened* prior to consumption.

Typable        Metadata has `types <types.rst>`_, and needs provisions for type checking of
               values.

Attributes     Metadata has `attributes <attributes.rst>`_ such as units, descriptions, allowed
               values, bounds, and format parameters. The attributes themselves have types and
               bounds that may need to be checked at metadata compilation time.  Other attributes
               may not have an effect on compilation, but still need to be passed to downstream
               programs and user interfaces.

Encodings      Strings in metadata may have different `encodings <encodings.rst>`_.  It shouldn't
               matter if you are writing notes in English or Chinese, the metadata system should
               be able to handle it.

Scriptable     Sometimes metadata is calculated from the data or from other metadata.  Providing
               a means of returning the results of external programs and doing simple
               string and arithmetic operations on those results can save a great deal of
               work elsewhere.

Discoverable   Much metadata works on following a fixed pattern of file names.  When these file
               name patterns are combined with scriptability it lets much of metadata generation
               to be automated and consistent.

Extensible     Developers in other fields should be able to extend metadata types and output
               formats via plugins.

============== =================================================================================

Issues meta_iron doesn't address
----------------------------------
``meta_iron`` is designed to be a simple tool and does not address the following issues:

====================== ========================================================================
Issue                  Reasons for Not Addressing in meta_iron
====================== ========================================================================
Complex Objects        Attributes in ``meta_iron`` are one level deep only.  The is no way of
                       defining attributes of attributes.

Horizontal Metadata    Metadata is sometimes organized vertically with respect to the
                       directory structure (one type of metadatum per directory), and
                       sometimes horizontally (one type of metadatum per file).  For example,
                       a set of files in the same directory with different latitudes and
                       longitudes have horizontal organization.  These latitudes and longitudes
                       *could* be attributes of the files, but could also be encoded in a
                       separate metadata file.  While ``meta_iron`` supports only the first
                       method of organization, the second method has some advantages such as
                       easy conversion to column/vector processing.

Packaging              There is only limited support for file naming, versioning, checksumming,
                       parent, children, etc.  This is structural metadata and outside
                       the main scope of ``meta_iron``.

====================== ========================================================================

Input files
-----------
There is only one type of input file, a tab-separated file with linux/MacOS newlines.
The first characters of this file must be the name of an encoding, itself encoded in ``UTF-8``
followed by a tab.  This becomes the default encoding applied to the rest of the file.

The remainder of the first row are names of attributes used in that file,
separated by tabs.  It is not necessary to have columns defined for attributes that are not
used in that file.

For rows after the first, the contents of the first column of each input file determines the
way that ``meta_iron`` interprets the remainder of the row.  Here are the possibilities
in order of testing:

=============== ===========================================================
Definition Type Interpretation
=============== ===========================================================
Comment         When the line begins with a ``#`` character, it is treated
                as a comment.  The rest of the row will be skipped.
                Comments are not output.

Metadata        The first column is treated as a key in a dictionary.
                You can use any characters you wish, including whitespace or
                ``+`` or ``-``, but these are best avoided because of
                assumptions that downstream programs may make.

Attribute       When the line begins with a ``.`` character, it
                defines an attibute or attributes of attributes.
`
Prototype       If the ``prototype`` attribute is set, the name is treated
                as a pattern for filename discovery.

=============== ===========================================================


* There is a required ``*root_metadata.tsv`` file that defines the root of the directory
  tree in a directory above the current working directory. The asterisk reflects that
  prefixing the name is to be encouraged for uniqueness.  Usually this file contains
  definitions of all attribute and metadata types, and a warning will be produced if
  later files define attribute and metadata types that were not defined in the root
  input file.

* Every directory with metadata requires a ``*directory_metadata.tsv`` that defines
  any directory-type-specific metadata (e.g., exact genome sizes).  There are usually
  just two columns in this file, name and value, but other attributes can be defined if desired.

* meta_iron produces a flattened metadata file in the directory in which it is run
  called ``*metadata.[TYPE}``, where the prefix follows the input ``*directory_metadata.tsv``
  name and where ``[TYPE]`` is the output type (TSV by default).

.. _ISA-Tab: http://www.dcc.ac.uk/resources/metadata-standards/isa-tab
.. _TSV: http://www.iana.org/assignments/media-types/text/tab-separated-values