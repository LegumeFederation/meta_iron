Flatten and smooth descriptive metadata
=======================================

``meta_iron`` is a tool that works with hierarchical descriptive metadata by reading and writing tab-separated files.

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
The following issues were deemed to be critical and not addressed by other programs:

============= =================================================================================
Issue         Description of Issue
============= =================================================================================
easy access   Consumers need to generate and parse metadata regardless of
              whether they are human or software, which computer language or editor they
              prefer, whether they are running in the browser or a standalone environment,
              whether served dynamically or are downloaded as static files.  We have
              chosen to use the widely-accepted TSV_ format for access reasons.

hierarchality Metadata is hierarchical in nature, and is reflected in a directory tree.
              Metadata may be may be undefined at some levels of the hierarchy
              and re-defined at others.  Consumers need to be able to
              access metadata from any part of a hierarchy without having to
              download and parse the higher levels.  This implies metadata needs
              to be *flattened* prior to consumption.

typing        Metadata has `types <types.rst>`_, and needs provisions for type checking of
              values.

attributes    Metadata has `attributes <attributes.rst>`_ such as units, descriptions, allowed
              values, bounds, and format parameters. These need to be checked at metadata
              compilation time and have an effect on metadata output.  Other attributes
              may not have an effect on compilation, but still need to be passed to downstream
              programs and user interfaces.

extensible    Developers and consumers should be able to easily add to or overwrite metadata
              if they desire.
============= =================================================================================

Issues meta_iron doesn't address
----------------------------------
``meta_iron`` is designed to be a simple tool and does not address the following issues:

====================== ========================================================================
Issue                  Reasons for Not Addressing in meta_iron
====================== ========================================================================
file-level granularity ``meta_iron`` is designed for directory-level operations and has no
                       concept of files or subdirectories.  This means that "horizontal
                       metadata" on a directory is not part of ``meta_iron``'s domain
                       (e.g., a file of separate latitude and longitude for
                       each file in a directory).  This decision due to the restrictions of
                       the tab-separated file format as it has commonly been used, in
                       particular the uniqueness requirement of column 1 names.

packaging              No concepts of file naming conventions, versioning, checksumming,
                       parent, children, etc.  This is structural metadata and outside
                       the scope of ``meta_iron``.

metadata creation      No support to create and populate input metadata files.  This is highly
                       domain- and project-specific, and has been already addressed by
                       tools such as ISA-Tab_.
====================== ========================================================================

Inputs and Outputs
------------------
Here is the scheme meta_iron uses to address the design goals:

* There is only one type of file for both input and output of metadata, a
  tab-separated file with linux/MacOS linefeeds and extension ``.tsv``.  The first
  column in this file must be the name of the metadata being defined, and the first
  row of this file are the lists of attributes defined.  Names and
  suitable as a variable name (e.g., no white spaces), or the field will be ignored
  and a warning produced.  If names are not unique in that file, a warning will be
  produced and the last instance of the name will be used.

* There is a required ``*root_metadata.tsv`` file that
  defines the dictionary of possible variable names and attributes.
  Any metadata name defined later that is not in this map will result in a warning.
  The asterisk reflects that prefixing the name is both acceptable and
  encouraged

* Every directory with metadata requires a ``*directory_metadata.tsv`` that defines
  the directory type (e.g., transcriptome or assembly) as well as any directory-type-specific
  metadata (e.g., exact genome sizes).  There are usually two columns in this file, name
  and value, but other attributes can be defined if desired.  There must be an unbroken
  chain of directory metadata files to the root metadata file, even if some of those
  directory metadata files are empty.

* meta_iron produces a flattened metadata file in the directory in which it is run
  called ``*metadata.tsv``, where the prefix follows the input ``*node_metadata.tsv`` name.

.. _ISA-Tab: http://www.dcc.ac.uk/resources/metadata-standards/isa-tab
.. _TSV: http://www.iana.org/assignments/media-types/text/tab-separated-values