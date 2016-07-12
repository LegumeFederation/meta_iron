 flatten and smooth descriptive metadata
 =====

 What is descriptive metadata?
 --------

 Metadata is data about other data, and it comes in two flavors: *structural metadata*
 which characterizes containers and content and *descriptive metadata* which characterizes the
 provenance, statistics, and purpose of the data. Structural metadata is typically
 addressed by packaging mechanisms such as tarballs, checksums, and
 the `BagIt <https://en.wikipedia.org/wiki/BagIt>`_ format. At its simplest,
 descriptive metadata can be thought of a set of key:value pairs
(e.g., ``genome_size: 3.1 Gbp``), but even this simple example shows the
challenge because of domain-specific issues of units and naming. Good
descriptive metadata make life easier for both data publisher and data
consumer by improving data discovery, reproducibility, and reusability.
Some tools that haven been used for descriptive metadata generation and
curation in the 'omics field are the
`ISA-Tab Tools <http://www.dcc.ac.uk/resources/metadata-standards/isa-tab>`_.

There are numerous challenges in dealing gracefully with descriptive metadata.
Here are the ones that ``meta_iron`` was designed to address:

============= =======
easy access   Consumers need to generate and parse metadata regardless of
              whether they are human or software, which computer language or editor they prefer,
              whether they are running in the browser or a standalone environment,
              whether served dynamically or are downloaded as static files.  We have
              chosen to stick with the widely-accepted
              `tab-separated file <http://www.iana.org/assignments/media-types/text/tab-separated-values>`_
              for access reasons.

hierarchality Metadata is hierarchical in nature, and is reflected in a directory tree.
              Metadata may be may be undefined at some levels of the hierachy
              and re-defined at others.  Consumers need to be able to
              access metadata from any part of a hierarchy without having to
              download and parse the higher levels.  This implies metadata needs
              to be *flattened* prior to consumption.

typing       Metadata has `types <types.rst>`_, and needs provisions for type checking of values.

attributes   Metadata has `attributes <attributes.rst>`_ such as units, descriptions,allowed values, and bounds.
             These need to be checked, where possible, and propagated to the user interface, but do not
             need to be searchable.

extensible   Developers and consumers should be able to easily add to or overwrite metadata if
             they desire.
============= =======

``meta_iron`` was intended to be a simple tool, and there are several issues related to metadata
it was *not* designed to address:

====================== =======
file-level granularity ``meta_iron`` is designed for directory-level operations and has no concept
                       of files or subdirectories.  This means that "horizontal metadata" on a directory
                       is not part of ``meta_iron``'s domain (e.g., a file of separate latitude and longitude for
                       each file in a directory).  This decision is in part due to the restrictions of
                       the tab-separated file format as it has commonly been used (uniqueness of column 1 names).

packaging              No concepts of file naming conventions, versioning, checksumming, parent, children, etc.

metadata creation      No concept of domain-specific calculation of metadata and creation of input files.
====================== =======


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

