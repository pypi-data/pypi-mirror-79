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
from __future__ import unicode_literals  # Python 2 and 3 compatibility
from future.builtins import str, list
import enum
import logging
import numpy as N

from astrophysix.utils import Stringifiable

log = logging.getLogger("astrophysix.simdm")


class DataType(enum.Enum):
    BOOLEAN = ('bool', "Boolean")
    COMPLEX = ('comp', "Complex number")
    DATETIME = ('time', "Datetime")
    REAL = ('real', "Real number")
    INTEGER = ('int', "Integer number")
    RATIONAL = ('rat', "Rational number")
    STRING = ('str', "String")

    def __init__(self, key, name):
        self._key = key
        self._name = name

    @property
    def key(self):
        return self._key

    @property
    def name(self):
        return self._name

    @classmethod
    def from_key(cls, k):
        for dt in cls:
            if dt.key == k:
                return dt
        raise ValueError("No DataType defined with the key '{key:s}'".format(key=k))


class ObjectList(Stringifiable):
    """
    Generic object list container class
    """
    def __init__(self, obj_class, index_prop_name, validity_check=None):
        super(ObjectList, self).__init__()
        self._list = list()
        self._obj_class = obj_class
        self._index_prop_name = index_prop_name
        self._validity_check_method = validity_check
        self._deletion_handlers = []

    def __eq__(self, other):
        """
        Object list comparison method

        other: ``ObjectList``
            other object list to compare to
        """
        # Object classes differ => not equal
        if self._obj_class != other.object_class:
            return False

        # Indexing property differ => not equal
        if self._index_prop_name != other.index_attribute_name:
            return False

        # List lengths differ => not equal
        if len(other) != len(self._list):
            return False

        # Check each object equality (both lists DO have the same length here)
        for iobj, o in enumerate(other):
            if o != self._list[iobj]:
                return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __len__(self):
        return len(self._list)

    @property
    def index_attribute_name(self):
        return self._index_prop_name

    @property
    def object_class(self):
        return self._obj_class

    def _can_add_object(self, obj):
        if not isinstance(obj, self._obj_class):
            err_msg = "Added object is not a valid '{cname:s}' instance.".format(cname=self._obj_class.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

        # Check unicity of object with this given index attribute value within the list
        index_val = getattr(obj, self._index_prop_name, None)
        if index_val is not None and self.__contains__(index_val):
            err_msg = "Cannot add {cname:s} object with index '{iv!s}' in this list, another item with that index " \
                      "value already exists.".format(cname=self._obj_class.__name__, iv=index_val)
            log.error(err_msg)
            raise AttributeError(err_msg)

        # If a validity check method is  provided, apply it
        if self._validity_check_method is not None:
            self._validity_check_method(obj)

    def add_deletion_handler(self, can_delete_meth):
        """
        Add an object deletion handling method to the list of deletion handlers

        Parameters
        ----------
        can_delete_meth: ``Callable``
            object deletion handling method
        """
        # Add deletion handling method to the list of object list deletion handlers
        if can_delete_meth not in self._deletion_handlers:  # Warning here hendling instance __eq__() comparison method will be called
            self._deletion_handlers.append(can_delete_meth)

    def __getitem__(self, index):
        if Stringifiable.is_type_string(index):
            sindex = Stringifiable.cast_string(index)
            for item in self._list:
                index_val = getattr(item, self._index_prop_name, None)
                if index_val is not None and index_val == sindex:
                    return item

            log.warning("Cannot find '{idx!s}' {cln:s} instance in list !".format(idx=sindex,
                                                                                  cln=self._obj_class.__name__))
            return None
        elif type(index) == int:
            if index >= 0 and index < len(self._list):
                return self._list[index]
            err_msg = "Object list index out of range (len={l:d}).".format(l=len(self._list))
            log.error(err_msg)
            raise IndexError(err_msg)
        else:
            err_msg = "'{it:s}' is not a valid search index. Valid types are 'str' and " \
                      "'int'.".format(it=str(index), cln=self._obj_class.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

    def __contains__(self, item):
        if Stringifiable.is_type_string(item):  # Check instance index is in list
            sitem = Stringifiable.cast_string(item)
            for obj in self._list:
                index_val = getattr(obj, self._index_prop_name, None)
                if index_val is not None and index_val == sitem:
                    return True
            return False
        elif isinstance(item, self._obj_class):  # Check instance is in list
            if item in self._list:
                return True
            return False
        else:
            err_msg = "'{it!s}' is not a valid search index. Valid types are 'str' and '{cln:s}' " \
                      "objects.".format(it=item, cln=self._obj_class.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

    def add(self, obj, insert_pos=-1):
        """
        Adds a instance to the list at a given position

        Parameters
        ----------
        obj: instance to insert
        insert_pos: insertion position in the simulation list. Default -1 (last).
        """
        self._can_add_object(obj)

        if insert_pos == -1:
            self._list.append(obj)
        else:
            self._list.insert(insert_pos, obj)

        return obj

    def find_by_uid(self, uid):
        """
        Find an object in the list with a matching UUID

        Parameters
        ----------
        uid: UUID or UUID string representation of the required object

        Returns
        -------
        o: Matching object with corresponding UUID,if any. Otherwise returns None
        """
        suid = str(uid)
        if getattr(self._obj_class, "uid", None) is None:
            err_msg = "{cname} objects do not have a 'uid' property.".format(cname=self._obj_class.__name__)
            log.error(err_msg)
            raise TypeError(err_msg)

        for o in self._list:
            if str(o.uid) == suid:
                return o
        return None

    def __unicode__(self):
        """
        String representation of the instance

        Examples
        --------
            >>> print(str(protocol.algorithms))
            Algorithm list :
            +---+--------------------------------------------+--------------------------------------------------------+
            | # |                   Index                    |                          Item                          |
            +---+--------------------------------------------+--------------------------------------------------------+
            | 0 | Adaptive mesh refinement                   | 'Adaptive mesh refinement' algorithm                   |
            +---+--------------------------------------------+--------------------------------------------------------+
            | 1 | Godunov scheme                             | 'Godunov scheme' algorithm                             |
            +---+--------------------------------------------+--------------------------------------------------------+
            | 2 | Harten-Lax-van Leer-Contact Riemann solver | 'Harten-Lax-van Leer-Contact Riemann solver' algorithm |
            +---+--------------------------------------------+--------------------------------------------------------+
            | 3 | Multigrid Poisson solver                   | 'Multigrid Poisson solver' algorithm                   |
            +---+--------------------------------------------+--------------------------------------------------------+
            | 4 | Particle-mesh solver                       | 'Particle-mesh solver' algorithm                       |
            +---+--------------------------------------------+--------------------------------------------------------+
        """
        # Empty object list
        if len(self._list) == 0:
            return "{obj_cname:s} list : empty".format(obj_cname=self._obj_class.__name__)

        # Display object list in a pretty-formatted table
        strrep = "{obj_cname:s} list :\n".format(obj_cname=self._obj_class.__name__)
        obj_slist = list([str(obj) for obj in self])
        index_slist = list([getattr(obj, self._index_prop_name, "") for obj in self])
        npos = int(N.log10(len(obj_slist))) + 1
        nind = N.max([len(ind) for ind in index_slist])
        ind_header = "Index"
        nind = len(ind_header) if nind < len(ind_header) else nind
        nstr = N.max([len(sobj) for sobj in obj_slist])
        item_header = "Item"
        nstr = len(item_header) if nstr < len(item_header) else nstr
        interline = "+-{npos:s}-+-{nind:s}-+-{nstr:s}-+".format(npos="-"*npos, nind=nind*"-", nstr=nstr*"-")
        strrep += interline + "\n| {d:^{npos}s} | {ind:^{nind}s} | " \
                              "{s:^{nstr}s} |\n".format(npos=npos, d="#", nind=nind, ind=ind_header, nstr=nstr,
                                                        s=item_header)
        for i in range(len(obj_slist)):
            strrep += interline + "\n"
            strrep += "| {i:>{npos}d} | {ind:<{nind}s} | {s:<{nstr}s} |\n".format(npos=npos, i=i, nind=nind,
                                                                                  ind=index_slist[i], nstr=nstr, s=obj_slist[i])
        strrep += interline

        return strrep

    def __iter__(self):
        """Basic object list iterator"""
        return iter(self._list)

    def __call__(self, *args, **kwargs):
        return self.__iter__()

    def __delitem__(self, item):
        """
        Delete instance or instance with a given index property value from object list

        Parameters
        ----------
        item: instance or index property value of the instance to remove from the list
        """
        found_obj = None
        if isinstance(item, self._obj_class):  # item is a corresponding instance of the list object class
            if item in self._list:
                found_obj = item
            else:
                err_msg = "'{o!s}' does not belong to this '{cln:s}' list.".format(o=item, cln=self._obj_class.__name__)
                log.error(err_msg)
                raise KeyError(err_msg)
        elif type(item) == int:
            if item >= 0 and item < len(self._list):
                found_obj = self._list[item]
            else:
                err_msg = "Object list index out of range (len={l:d}).".format(l=len(self._list))
                log.error(err_msg)
                raise IndexError(err_msg)
        elif Stringifiable.is_type_string(item):  # item is a string => search for an object in the list
            sitem = Stringifiable.cast_string(item)
            for obj in self._list:
                index_val = getattr(obj, self._index_prop_name, None)
                if index_val is not None and index_val == sitem:
                    found_obj = obj
                    break

            if found_obj is None:
                # Not found
                err_msg = "Cannot find '{it!s}' {cln:s} instance in list !".format(it=sitem, cln=self._obj_class.__name__)
                log.error(err_msg)
                raise KeyError(err_msg)
        else:
            # Invalid item value
            err_msg = "'{it!s}' is not a valid deletion index. Valid types are 'str' and '{cln:s}' " \
                      "objects.".format(it=item, cln=self._obj_class.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

        # ------------------------------------------ Checks dependencies --------------------------------------------- #
        # Call object deletion handlers, if any is defined
        depend_list = []
        for del_handler in self._deletion_handlers:
            depend_obj = del_handler(found_obj)
            if depend_obj is not None:
                depend_list.append(depend_obj)

        # If deleted object has any dependency, prevent its deletion
        if len(depend_list) > 0:
            err_msg = "'{o!s}' cannot be deleted, the following items depend on it (try to delete them first) : " \
                      "[{dl:s}].".format(o=found_obj, dl=", ".join(depend_list))
            log.warning(err_msg)
            raise AttributeError(err_msg)

        self._list.remove(found_obj)


__all__ = ["ObjectList"]
