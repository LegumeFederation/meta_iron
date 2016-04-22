# meta_iron
a tool to smoothe and flatten 'omic metadata

Metadata can be viewed as data too small and irregular to warrant
their own data structures, but too critical to embed in file naming
conventions.  Additionally, some metadata may be useful as search
keys. There are numerous challenges in dealing gracefully with
metadata, but here are the ones that meta_iron addresses:

* Consumers need to easily read, write, and parse metadata regardless of:
  	    - whether they are human or software
  	    - which computer language or editor they prefer
  	    - whether they are running in the the browser or standalone
  	    - whether served dynamically via
	      or are downloaded as static files.

* Metadata is hierarchical in nature, and may be undefined at some
  levels and re-defined at others.  Consumers need to be able to
  access metadata from any part of a hierarchy without having to
  (download and) parse the higher levels.  This implies metadata needs
  to be flattened prior to consumption.

* There is meta-metadata in the dictionary of possible variable names
  along with units and definitions. These need to be propaged to the
  UI but not indexed.  For syntactical reasons they can't just be put
  into variable names, because units need special characters and
  definitions need sentences.

* Good metadata make both database maintainer's and the programmer's
  jobs easier by regularizing data discovery without having to
  enforce or encode a complex file-naming convention.  Original file
  names, provenance, and supercession can all be encoded into metadata.

* Consumers should be able to easily add to metadata or change it if
  they want so long as it resides in a private space.  This is the
  normal mode for LegFed developers who aim to put into later use.


Here is the scheme meta_iron uses to address these goals:

* The data hierarchy is reflected in a directory hierarchy.  There
  are no OS-specific tricks such as symlinks or unions.  File names
  are kept as simple as possible.  Versioning 
  
* Every directory in the tree requires a file in YAML format
  called "node_metadata.yaml" that defines the directory type (e.g.,
  transcriptome or assembly) as well as any directory-type-specific
  metadata (e.g., exact genome sizes).  YAML was picked because:
  	   - it is easily read and edited by humans
	   - it has flexible data types
	   - parsers for it exist in most languages, including JavaScript

* meta_iron produces a flattened metadata file for every node in the
  tree called "metadata.yaml".  meta_iron produces this file by
  traversing nodes up the tree until it finds a root_metadata.yaml
  file which defines the root.  It then overloads descendants in order
  into a flat namespace.  It also searches for children (one level
  deep only) and loads their types into a "children" map.

* There is a "metameta" map in the root_metadata.yaml file that
  defines the dictionary of possible variable names.  Any variable
  that is not in this map will throw an exception at metadata
  compiling time.  Each variable potentially has three items in a
  submap:
	-label: a short printable label, e.g. "Genome Size"
	-units: a units string, e.g. "Mbp" or "signatures/Gbp"
	-desc: A short description suitable for tooltips.
	-index: A boolean, that if present and true, results in
	 the value being indexed (e.g., by IRODS metadata or Lucene.

* meta_iron understands a variety of directory types and file types
  and will attempt populate metadata entries by programmatic means
  (i.e., by running gaemr on assembly files).

* meta_iron has naming conventions stored in the metameta map, and will
  enforce these naming conventions.


* meta_iron has versioning convention built-in.  The current version
  convention is to have a "_vX.Y" built into directory names for all
  directories more than one level below the root.
