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
from __future__ import absolute_import, unicode_literals
from future.builtins import str, list, dict
import logging
from astrophysix.utils.persistency import Hdf5StudyPersistent
from astrophysix.utils.strings import Stringifiable

log = logging.getLogger("astrophysix.simdm")


class InputParameter(Hdf5StudyPersistent, Stringifiable):
    """
    Protocol input parameter

    Parameters
    ----------
    key: input parameter indexing key (mandatory)
    name: input parameter name
    description: input parameter description
    """
    def __init__(self, **kwargs):
        super(InputParameter, self).__init__(**kwargs)

        self._key = ""
        self._name = ""
        self._description = ""

        if "key" not in kwargs:
            raise AttributeError("Input parameter 'key' attribute is not defined (mandatory).")
        self.key = kwargs["key"]

        if "name" in kwargs:
            self.name = kwargs["name"]

        if "description" in kwargs:
            self.description = kwargs["description"]

    def __eq__(self, other):
        """
        InputParameter comparison method

        other: ``InputParameter``
            input parameter to compare to
        """
        if not super(InputParameter, self).__eq__(other):
            return False

        if self._name != other.name:
            return False

        if self._key != other.key:
            return False

        if self._description != other.description:
            return False

        return True

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, new_key):
        try:
            self._key = Stringifiable.cast_string(new_key, valid_empty=False)
        except TypeError:
            raise AttributeError("Input parameter 'key' property is not a valid (non empty) string.")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        try:
            self._name = Stringifiable.cast_string(new_name)
        except TypeError:
            raise AttributeError("Input parameter 'name' property is not a valid string.")

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, new_descr):
        try:
            self._description = Stringifiable.cast_string(new_descr)
        except TypeError:
            raise AttributeError("Input parameter 'description' property is not a valid string.")

    def _hsp_write(self, h5group, **kwargs):
        """
        Serialize an InputParameter object into a HDF5 file.

        Parameters
        ----------
        h5group: ``h5py.Group``
            Main group to write the InputParameter into.
        kwargs: ``dict``
            keyword argument dictionary.
        """
        # Call to parent class _hsp_write() : write UUID, etc.
        super(InputParameter, self)._hsp_write(h5group, **kwargs)

        # Write input parameter key
        self._hsp_write_attribute(h5group, ('key', self._key), **kwargs)

        # Write input parameter name, if defined
        self._hsp_write_attribute(h5group, ('name', self._name), **kwargs)

        # Write input parameter description, if defined
        self._hsp_write_attribute(h5group, ('description', self._description), **kwargs)

    @classmethod
    def _hsp_read(cls, h5group, version, dependency_objdict=None):
        """
        Read an InputParameter object from a HDF5 file (*.h5).

        Parameters
        ----------
        h5group: ``h5py.Group``
            Main group to read the object from.
        version: ``int``
            version of the object to read.
        dependency_objdict: ``dict``
            dependency object dictionary. Default None

        Returns
        -------
        exp: ``InputParameter``
            Read InputParameter instance
        """
        # Handle different versions here

        # Fetch Hdf5StudyPersistent object UUID
        uid = super(InputParameter, cls)._hsp_read(h5group, version, dependency_objdict=dependency_objdict)

        # Read input parameter key
        ip_key = cls._hsp_read_attribute(h5group, 'key', "input parameter key")

        # Create input parameter object
        ip = cls(uid=uid, key=ip_key)

        # Read input parameter key, if defined
        ip_name = cls._hsp_read_attribute(h5group, 'name', "input parameter name", raise_error_if_not_found=False)
        if ip_name is not None:
            ip.name = ip_name

        # Read input parameter description, if defined
        ip_descr = cls._hsp_read_attribute(h5group, 'description', "input parameter description",
                                           raise_error_if_not_found=False)
        if ip_descr is not None:
            ip.description = ip_descr

        return ip

    def __unicode__(self):
        """
        String representation of the instance
        """
        s = "[{ipk:s}]".format(ipk=self._key)
        if len(self._name) > 0:
            s += " '{ipname:s}'".format(ipname=self._name)
        s += " input parameter"
        return s


__all__ = ["InputParameter"]
