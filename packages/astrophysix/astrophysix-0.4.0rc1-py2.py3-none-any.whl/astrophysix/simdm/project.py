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
from future.builtins import str, list
import logging
import uuid

from astrophysix.utils.persistency import Hdf5StudyPersistent
from .commons import ProjectCategory
from .utils import ObjectList
from astrophysix.utils.strings import Stringifiable
from .experiment import Simulation
from .protocol import SimulationCode, PostProcessingCode


log = logging.getLogger("astrophysix.simdm")


class Project(Hdf5StudyPersistent, Stringifiable):
    """
    Project (Simulation data model)

    Parameters
    ----------
    category: `enum:astrophysix.simdm.commons.ProjectCategory` alias. (mandatory)
    project_title: project title (mandatory)
    alias: Project alias (if defined, 16 max characters is recommended)
    short_description: project short description
    general_description: (long) project description
    data_description: available data description in the project
    directory_path: project directory path
    """
    def __init__(self, *args, **kwargs):
        uid = kwargs.pop("uid", None)
        super(Project, self).__init__(uid=uid)

        self._category = ProjectCategory.StarFormation
        self._title = ""
        self._short_description = ""
        self._general_description = ""
        self._data_description = ""
        self._alias = ""
        self._directory_path = ""

        self._simulations = ObjectList(Simulation, "name")

        if "category" not in kwargs:
            raise AttributeError("Project 'category' attribute is not defined (mandatory).")
        self.category = kwargs["category"]

        if "project_title" not in kwargs:
            raise AttributeError("Project 'project_title' attribute is not defined (mandatory).")
        self.project_title = kwargs["project_title"]

        if "alias" in kwargs:
            self.alias = kwargs["alias"]

        if "short_description" in kwargs:
            self.short_description = kwargs["short_description"]

        if "general_description" in kwargs:
            self.general_description = kwargs["general_description"]

        if "data_description" in kwargs:
            self.data_description = kwargs["data_description"]

        if "directory_path" in kwargs:
            self.directory_path = kwargs["directory_path"]

    def __eq__(self, other):
        """
        Project comparison method

        other: ``Project``
            project to compare to
        """
        if not super(Project, self).__eq__(other):
            return False

        if self._category != other.category:
            return False

        if self._title != other.project_title:
            return False

        if self._alias != other.alias:
            return False

        if self._short_description != other.short_description:
            return False

        if self._general_description != other.general_description:
            return False

        if self._data_description != other.data_description:
            return False

        if self._directory_path != other.directory_path:
            return False

        if self._simulations != other.simulations:
            return False

        return True

    def __ne__(self, other):  # Not an implied relationship between "rich comparison" equality methods in Python 2.X
        return not self.__eq__(other)

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, new_cat):
        try:
            scat = Stringifiable.cast_string(new_cat)
            self._category = ProjectCategory.from_alias(scat)
        except ValueError as  ve:
            log.error(str(ve))
            raise AttributeError(str(ve))
        except TypeError:
            if not isinstance(new_cat, ProjectCategory):
                err_msg = "Project 'category' attribute is not a valid ProjectCategory enum value."
                log.error(err_msg)
                raise AttributeError(err_msg)
            self._category = new_cat

    @property
    def project_title(self):
        return self._title

    @project_title.setter
    def project_title(self, new_title):
        try:
            self._title = Stringifiable.cast_string(new_title, valid_empty=False)
        except TypeError:
            err_msg = "Project 'project_title' property is not a valid (non empty) string."
            log.error(err_msg)
            raise AttributeError(err_msg)

    @property
    def alias(self):
        return self._alias

    @alias.setter
    def alias(self, new_alias):
        try:
            self._alias = Stringifiable.cast_string(new_alias)
            if len(new_alias) > 16:
                log.warning("Project 'alias' attribute is too long (max 16 characters).")
        except TypeError:
            err_msg = "Project 'alias' property is not a valid string"
            log.error(err_msg)
            raise AttributeError(err_msg)

    @property
    def short_description(self):
        return self._short_description

    @short_description.setter
    def short_description(self, new_descr):
        try:
            self._short_description = Stringifiable.cast_string(new_descr)
        except TypeError:
            err_msg = "Project 'short_description' property is not a valid string"
            log.error(err_msg)
            raise AttributeError(err_msg)

    @property
    def general_description(self):
        return self._general_description

    @general_description.setter
    def general_description(self, new_descr):
        try:
            self._general_description = Stringifiable.cast_string(new_descr)
        except TypeError:
            err_msg = "Project 'general_description' property is not a valid string"
            log.error(err_msg)
            raise AttributeError(err_msg)

    @property
    def data_description(self):
        return self._data_description

    @data_description.setter
    def data_description(self, new_descr):
        try:
            self._data_description = Stringifiable.cast_string(new_descr)
        except TypeError:
            err_msg = "Project 'data_description' property is not a valid string"
            log.error(err_msg)
            raise AttributeError(err_msg)

    @property
    def directory_path(self):
        return self._directory_path

    @directory_path.setter
    def directory_path(self, new_path):
        try:
            self._directory_path = Stringifiable.cast_string(new_path)
        except TypeError:
            err_msg = "Project 'directory_path' property is not a valid string"
            log.error(err_msg)
            raise AttributeError(err_msg)

    @property
    def simulations(self):
        return self._simulations

    def _simu_codes(self):
        """Simulation codes iterator"""
        puid_list = []
        for simu in self._simulations:
            p = simu.simulation_code
            if p.uid not in puid_list:
                puid_list.append(p.uid)
                yield p

    def _post_pro_codes(self):
        """Post-processing codes iterator"""
        ppcode_uid_list = []
        for simu in self._simulations:
            for pprun in simu.post_processing_runs:
                p = pprun.postpro_code
                if p.uid not in ppcode_uid_list:
                    ppcode_uid_list.append(p.uid)
                    yield p

    @property
    def _target_objects(self):
        """Target object iterator"""
        # TODO
        to_uid_list = []
        for simu in self._simulations:
            yield None

    def _hsp_write(self, h5group, **kwargs):
        """
        Serialize a Project object into a HDF5 file.

        Parameters
        ----------
        h5group: ``h5py.Group``
            Main group to write the Project into.
        kwargs: ``dict``
            keyword argument dictionary.
        """
        # Call to parent class _hsp_write() : write UUID, etc.
        super(Project, self)._hsp_write(h5group, **kwargs)

        # If necessary, call callback function with project name
        self._hsp_write_callback(str(self), **kwargs)

        # Write project title
        self._hsp_write_attribute(h5group, ('title', self._title), **kwargs)

        # Write project category alias
        self._hsp_write_attribute(h5group, ('category', self._category.alias), **kwargs)

        # Write project Galactica alias, if defined
        self._hsp_write_attribute(h5group, ('galactica_alias', self._alias), **kwargs)

        # Write project directory path, if defined
        self._hsp_write_attribute(h5group, ('project_directory', self._directory_path), **kwargs)

        # Write project short/general/data description
        self._hsp_write_attribute(h5group, ('short_description', self._short_description), **kwargs)
        self._hsp_write_attribute(h5group, ('general_description', self._general_description), **kwargs)
        self._hsp_write_attribute(h5group, ('data_description', self._data_description), **kwargs)

        # Write protocol directory
        if kwargs.get("from_project", False):  # Write protocol list in project subgroup (not in each experiment)
            proto_group = self._hsp_get_or_create_h5group(h5group, "PROTOCOLS", **kwargs)
            self._hsp_write_object_list(proto_group, "SIMU_CODES", self._simu_codes, "simu_code_", **kwargs)
            self._hsp_write_object_list(proto_group, "PPRUN_CODES", self._post_pro_codes, "pprun_code_", **kwargs)

        # Write all target objects
        # if kwargs.get("from_project", False):
        #     self._hsp_write_object_list(h5group, "TARGET_OBJECTS", self._target_objects, "targobj_", **kwargs)

        # Write all simulations
        self._hsp_write_object_list(h5group, "SIMULATIONS", self._simulations, "simu_", **kwargs)

    @classmethod
    def _hsp_read(cls, h5group, version, dependency_objdict=None):
        """
        Read a Project object from a HDF5 file (*.h5).

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
        proj: ``Project``
            Read Project instance
        """
        # Handle different versions here

        # Fetch Hdf5StudyPersistent object UUID
        uid = super(Project, cls)._hsp_read(h5group, version, dependency_objdict=dependency_objdict)

        # Create Project instance with mandatory attributes
        t = cls._hsp_read_attribute(h5group, "title", "project title")
        cat = cls._hsp_read_attribute(h5group, "category", "project category")
        proj = cls(uid=uid, category=cat, project_title=t)

        # ------------------------------------------ Optional attributes --------------------------------------------- #
        # Read Galactica alias
        alias = cls._hsp_read_attribute(h5group, "galactica_alias", "project Galactica alias",
                                        raise_error_if_not_found=False)
        if alias is  not None:
            proj.alias = alias
        # Read project directory
        dpath = cls._hsp_read_attribute(h5group, "project_directory", "project directory",
                                        raise_error_if_not_found=False)
        if dpath is not None:
            proj.directory_path = dpath
        # Read project short/general/data description
        ddescr = cls._hsp_read_attribute(h5group, "data_description", "project data description",
                                         raise_error_if_not_found=False)
        if ddescr is not None:
            proj.data_description = ddescr
        gdescr = cls._hsp_read_attribute(h5group, "general_description", "project general description",
                                         raise_error_if_not_found=False)
        if gdescr is not None:
            proj.general_description = gdescr
        sdescr = cls._hsp_read_attribute(h5group, "short_description", "project short description",
                                         raise_error_if_not_found=False)
        if sdescr is not None:
            proj.short_description = sdescr
        # ------------------------------------------------------------------------------------------------------------ #

        # Build dependency object dictionary indexed by their class name
        dod = {}
        if "PROTOCOLS" in h5group:
            protgroup = h5group["PROTOCOLS"]
            # Build simulation code dictionary indexed by their UUID
            if "SIMU_CODES" in protgroup:
                simu_code_dict = {}
                for simu_code in SimulationCode._hsp_read_object_list(protgroup, "SIMU_CODES", "simu_code_",
                                                                      "simulation code"):
                    simu_code_dict[simu_code.uid] = simu_code

                dod[SimulationCode.__name__] = simu_code_dict

            # Build post-processing code dictionary indexed by their UUID
            if "PPRUN_CODES" in protgroup:
                pprun_code_dict = {}
                for pprun_code in PostProcessingCode._hsp_read_object_list(protgroup, "PPRUN_CODES", "pprun_code_",
                                                                           "post-processing code"):
                    pprun_code_dict[pprun_code.uid] = pprun_code

                dod[PostProcessingCode.__name__] = pprun_code_dict

        # Build simulation list and add each simulation into project
        if "SIMULATIONS" in h5group:
            for simu in Simulation._hsp_read_object_list(h5group, "SIMULATIONS", "simu_", "project simulation",
                                                         dependency_objdict=dod):
                proj.simulations.add(simu)

        return proj

    def __unicode__(self):
        """
        String representation of the instance
        """
        strrep = "[{category:s}]".format(category=self._category.verbose_name)

        # Title and short description
        if len(self._title) > 0:
            strrep += " '{ptitle:s}' project".format(ptitle=self._title)

        return strrep


__all__ = ["Project"]
