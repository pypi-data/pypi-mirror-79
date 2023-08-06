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
from future.builtins import str, list, dict, int
import logging
import uuid

from astrophysix.utils.strings import Stringifiable
from astrophysix.utils.persistency import Hdf5StudyPersistent
from ..utils import DataType
from ..protocol import InputParameter
from astrophysix import units as U
from enum import Enum


log = logging.getLogger("astrophysix.simdm")


class ParameterVisibility(Enum):
    NOT_DISPLAYED = ("not_displayed", "Not displayed")
    ADVANCED_DISPLAY = ("advanced", "Advanced display")
    BASIC_DISPLAY = ("basic", "Basic display")

    def __init__(self, key, display_name):
        self._key = key
        self._disp_name = display_name

    @property
    def key(self):
        return self._key

    @property
    def display_name(self):
        return self._disp_name

    @classmethod
    def from_key(cls, key):
        for pvis in cls:
            if pvis.key == key:
                return pvis
        raise ValueError("No ParameterVisibility defined with the key '{k:s}'".format(k=key))


class ParameterSetting(Hdf5StudyPersistent, Stringifiable):
    """
    Experiment input parameter setting class

    Parameters
    ----------
    input_param: ``:class:astrophysix.simdm.protocol.input_parameters.InputParameter``
        protocol input parameter (mandatory)
    value: ``float``or ``int`` or ``string`` or ``bool``
        numeric/string/boolean value of the input parameter (mandatory)
    unit: ``string``
        Galactica commons unit key
    visibility: ``ParameterVisibility``
        Param. setting visibility (for display use only). Default ParameterVisibility.BASIC_DISPLAY
    """
    def __init__(self, **kwargs):
        super(ParameterSetting, self).__init__(**kwargs)

        # Protocol associated input parameter
        if "input_param" not in kwargs:
            raise AttributeError("ParameterSetting 'input_param' attribute is not defined (mandatory).")
        inpparam = kwargs["input_param"]
        if not isinstance(inpparam, InputParameter):
            raise AttributeError("Parameter setting 'input_param' attribute is not a valid InputParameter object.")
        self._inpparam = inpparam

        # Input parameters settings
        self._dtype = DataType.REAL
        self._float_value = None
        self._int_value = None
        self._string_value = ""
        self._bool_value = None
        if "value" not in kwargs:
            raise AttributeError("ParameterSetting 'value' attribute is not defined (mandatory).")
        self.value = kwargs["value"]

        self._visibility = ParameterVisibility.BASIC_DISPLAY
        if "visibility" in kwargs:
            self.visibility = kwargs["visibility"]

        self._unit = U.none
        if "unit" in kwargs:
            self.unit = kwargs["unit"]

    def __eq__(self, other):
        """
        ParameterSetting comparison method

        other: ``ParameterSetting``
            parameter setting to compare to
        """
        if not super(ParameterSetting, self).__eq__(other):
            return False

        if self._inpparam != other.input_parameter:
            return False

        if self._dtype != other.value_type or self.value != other.value:
            return False

        if self._visibility != other.visibility:
            return False

        return self._unit == other.unit and self._unit.name == other.unit.name

    @property
    def input_parameter(self):
        return self._inpparam

    @property
    def parameter_key(self):
        return self._inpparam.key

    @property
    def value_type(self):
        return self._dtype

    @property
    def value(self):
        if self._dtype == DataType.REAL:
            return self._float_value
        elif self._dtype == DataType.INTEGER:
            return self._int_value
        elif self._dtype == DataType.BOOLEAN:
            return self._bool_value
        else:  # self._dtype == DataType.STRING:
            return self._string_value

    @value.setter
    def value(self, new_value):
        if isinstance(new_value, bool):  # Boolean value
            self._bool_value = new_value
            self._dtype = DataType.BOOLEAN
            return

        try:
            # Try to cast it as a string
            self._string_value = Stringifiable.cast_string(new_value)
            self._dtype = DataType.STRING

            if self._string_value in ["true", "True"]:  # String that can be casted into a boolean (True) value
                self._bool_value = True
                self._dtype = DataType.BOOLEAN
                return
            elif self._string_value in ["false", "False"]:  # String that can be casted into a boolean (False) value
                self._bool_value = False
                self._dtype = DataType.BOOLEAN
                return

            # Try to cast it into a numeric value
            try:
                self._cast_numeric_value(self._string_value)
            except ValueError:
                # Not a numeric value, keep it a string value
                pass

        except TypeError:  # Not a valid string object
            try:
                self._cast_numeric_value(new_value)
            except TypeError:  # Not a numeric/string value that can be casted into a real number
                raise AttributeError("ParameterSetting 'value' attribute is not a valid string / integer / float / "
                                     "boolean value")

    def _cast_numeric_value(self, v):
        # Cast it into a float
        fvalue = float(v)
        if fvalue > 2 ** 31 or fvalue < -2 ** 31:
            self._float_value = fvalue
            self._dtype = DataType.REAL
        else:
            ivalue = int(fvalue)  # Convert the float into a int
            if ivalue - fvalue == 0.0:
                self._int_value = ivalue
                self._dtype = DataType.INTEGER
            else:
                self._float_value = fvalue
                self._dtype = DataType.REAL

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, new_unit):
        if isinstance(new_unit, U.Unit):
            self._unit = new_unit
        else:
            try:
                s = Stringifiable.cast_string(new_unit, valid_empty=False)
                self._unit = U.Unit.from_name(s)
            except TypeError:  # Not a valid string
                err_msg = "Parameter setting 'unit' property is not a valid (non-empty) string."
                log.error(err_msg)
                raise AttributeError(err_msg)
            except AttributeError as aerr:
                err_msg = "Parameter setting 'unit' property error : {uerr:s}.".format(uerr=str(aerr))
                log.error(err_msg)
                raise AttributeError(err_msg)

    @property
    def visibility(self):
        return self._visibility

    @visibility.setter
    def visibility(self, new_vis):
        try:
            pvis = Stringifiable.cast_string(new_vis)
            self._visibility = ParameterVisibility.from_key(pvis)
        except ValueError as ve:
            err_msg = "Parameter setting 'visibility' property error : {verr:s}.".format(verr=str(ve))
            log.error(err_msg)
            raise AttributeError(err_msg)
        except TypeError:  # Not a valid string
            if not isinstance(new_vis, ParameterVisibility):
                err_msg = "ParameterSetting 'visibility' attribute is not a valid ParameterVisibility enum value."
                log.error(err_msg)
                raise AttributeError(err_msg)
            self._visibility = new_vis

    def _hsp_write(self, h5group, **kwargs):
        """
        Serialize a ParameterSetting object into a HDF5 file.

        Parameters
        ----------
        h5group: ``h5py.Group``
            Main group to write the ParameterSetting into.
        kwargs: ``dict``
            keyword argument dictionary.
        """
        # Call to parent class _hsp_write() : write UUID, etc.
        super(ParameterSetting, self)._hsp_write(h5group, **kwargs)

        # Write input parameter UUID
        self._hsp_write_attribute(h5group, ('inpparam_uid', self._inpparam.uid), **kwargs)

        # Write parameter setting value, if defined
        self._hsp_write_attribute(h5group, ('value', self.value), **kwargs)
        self._hsp_write_attribute(h5group, ('value_type', self._dtype.key), **kwargs)

        # Write parameter setting visibility key
        self._hsp_write_attribute(h5group, ('visibility', self._visibility.key), **kwargs)

        # Write parameter setting unit
        self._hsp_write_attribute(h5group, ('unit', self._unit), **kwargs)

    @classmethod
    def _hsp_read(cls, h5group, version, dependency_objdict=None):
        """
        Read a ParameterSetting object from a HDF5 file (*.h5).

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
        psetting: ``ParameterSetting``
            Read ParameterSetting instance
        """
        # Handle different versions here

        # Fetch Hdf5StudyPersistent object UUID
        uid = super(ParameterSetting, cls)._hsp_read(h5group, version, dependency_objdict=dependency_objdict)

        # Read algorithm type
        param_uid = uuid.UUID(cls._hsp_read_attribute(h5group, 'inpparam_uid', "input parameter UUID"))
        protocol = list(dependency_objdict.values())[0]
        found_param = protocol.input_parameters.find_by_uid(param_uid)
        if found_param is None:
            err_msg = "Unknown input parameter UUID '{puid!s}' in the {proto!s}.".format(puid=param_uid, proto=protocol)
            log.error(err_msg)
            raise IOError(err_msg)

        # Read parameter setting value
        v = cls._hsp_read_attribute(h5group, 'value', "parameter setting value")
        vtype = DataType.from_key(cls._hsp_read_attribute(h5group, "value_type", "parameter setting value datatype"))
        if vtype == DataType.BOOLEAN:
            v = bool(v)

        # Read parameter setting visibility
        vis = cls._hsp_read_attribute(h5group, "visibility", "parameter setting visibility")

        # Read parameter setting unit
        u = cls._hsp_read_unit(h5group, "unit")

        # Create parameter setting object
        psetting = cls(uid=uid, input_param=found_param, value=v, visibility=vis, unit=u)

        return psetting

    def __unicode__(self):
        """
        String representation of the instance
        """
        if self._unit.name != "none":
            us = " {un:s}".format(un=self._unit.name)
        else:
            us = ""
        s = "[{ps_ipnaame:s} = {v!s}{us:s}]".format(ps_ipnaame=self._inpparam.name, v=self.value, us=us)
        s += " parameter setting"
        return s


__all__ = ["ParameterSetting", "ParameterVisibility"]
