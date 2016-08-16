Units
=====

Units are parsed and checked using the
`pint <https://pint.readthedocs.io/>`_ package.
By default this package uses a set of definitions
that includes a wide variety of units,

``meta_iron`` extends the default unit defitions
with an instance-specific set if they exist.The
 units definitionfile should be named
``unit_defs.txt`` and placed in the root
metadata directory.

An example unit definitions file is included
with the examples accessible through the
``install_example_files`` subcommand.  That
set of definitions have been extended
to include the following genomics terms and
abbreviations:

==============================  ============
Unit Name                       Abbreviation
==============================  ============
base_pair                       bp
chromosome                      chr
event                           evt
generation                      gen
genome                          gn
individual                      ind
Morgan                          M
operational_taxonomic_unit      OTU
phylogenetic_unit               PU
population                      pop
recombination                   rec
substitution                    sub
==============================  ===========

Note that you should be using the abbreviated form in unit definitions.