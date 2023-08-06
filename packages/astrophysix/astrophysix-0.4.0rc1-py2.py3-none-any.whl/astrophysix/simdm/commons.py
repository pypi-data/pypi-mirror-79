# -*- coding: utf-8 -*-
# This file is part of the 'astrophysix' Python package.
#
# Copyright © Commissariat a l'Energie Atomique et aux Energies Alternatives (CEA)
#
#  FREE SOFTWARE LICENCING
#  -----------------------
# This software is governed by the CeCILL license under French law and abiding by the rules of distribution of free
# software. You can use, modify and/or redistribute the software under the terms of the CeCILL license as circulated by
# CEA, CNRS and INRIA at the following URL: "http://www.cecill.info". As a counterpart to the access to the source code
# and rights to copy, modify and redistribute granted by the license, users are provided only with a limited warranty
# and the software's author, the holder of the economic rights, and the successive licensors have only limited
# liability. In this respect, the user's attention is drawn to the risks associated with loading, using, modifying
# and/or developing or reproducing the software by the user in light of its specific status of free software, that may
# mean that it is complicated to manipulate, and that also therefore means that it is reserved for developers and
# experienced professionals having in-depth computer knowledge. Users are therefore encouraged to load and test the
# software's suitability as regards their requirements in conditions enabling the security of their systems and/or data
# to be ensured and, more generally, to use and operate it in the same conditions as regards security. The fact that
# you are presently reading this means that you have had knowledge of the CeCILL license and that you accept its terms.
#
#
# COMMERCIAL SOFTWARE LICENCING
# -----------------------------
# You can obtain this software from CEA under other licencing terms for commercial purposes. For this you will need to
# negotiate a specific contract with a legal representative of CEA.
#
from __future__ import print_function, unicode_literals, division, absolute_import  # Python 2 and 3 compatibility
from enum import Enum


class ProjectCategory(Enum):
    """
    Project category enum
    """
    SolarMHD = ("SOLAR_MHD", "Solar Magnetohydrodynamics")
    PlanetaryAtmospheres = ("PLANET_ATMO", "Planetary atmospheres")
    StarPlanetInteractions = ("STAR_PLANET_INT", "Star-planet interactions")
    StarFormation = ("STAR_FORM", "Star formation")
    Supernovae = ("SUPERNOVAE", "Supernovae")
    GalaxyFormation = ("GAL_FORMATION", "Galaxy formation")
    GalaxyMergers = ("GAL_MERGERS", "Galaxy mergers")
    Cosmology = ("COSMOLOGY", "Cosmology")

    def __init__(self, alias, verbose):
        self._alias = alias
        self._verbose = verbose

    @property
    def alias(self):
        return self._alias

    @property
    def verbose_name(self):
        return self._verbose

    @classmethod
    def from_alias(cls, alias):
        for cat in cls:
            if cat.alias == alias:
                return cat
        raise ValueError("No ProjectCategory defined with the alias '{a:s}'".format(a=alias))


__all__ = ["ProjectCategory"]
