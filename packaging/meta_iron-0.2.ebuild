# Copyright 2016 National Center for Genome Resources
# Distributed under the terms of the BSD licence
# $Header: $

EAPI=5

PYTHON_COMPAT=( python3_{4,5} )

inherit distutils-r1

DESCRIPTION="Flatten and smooth descriptive metadata"
HOMEPAGE="https://github.com/LegumeFederation/${P}"
SRC_URI="mirror://pypi/${PN:0:1}/${PN}/${P}.tar.gz"

DEPEND="dev-python/click
	    dev-python/click-plugins
	    dev-python/tabulate
        dev-python/pandas
        dev-python/pint
        dev-python/asteval
		dev-python/pytest
"

LICENSE="BSD"
SLOT="0"
KEYWORDS="~amd64 ~x86 ~amd64-linux ~x86-linux"
IUSE=""
