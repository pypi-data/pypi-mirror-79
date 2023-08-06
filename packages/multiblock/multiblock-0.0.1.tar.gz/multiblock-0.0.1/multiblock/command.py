##
#
# Copyright (C) 2020 Matt Molyneaux
#
# This file is part of Multiblock.
#
# Multiblock is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Multiblock is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Multiblock.  If not, see <https://www.gnu.org/licenses/>.
#
##

"""
Documentation for this module can be found in :doc:`commandline`
"""

import logging

import click

from . import __version__

logger = logging.getLogger("multiblock")


@click.group()
@click.version_option(version=__version__)
@click.option("-v", "--verbose", count=True,
              help="Verbose output, can be used multiple times to increase logging level")
def multiblock(verbose):
    logger.addHandler(logging.StreamHandler())
    if verbose > 1:
        logger.setLevel(logging.DEBUG)
    elif verbose == 1:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARN)
