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
from future.builtins import str, list, int
import logging
import os
import numpy as N

from astrophysix.utils.file import FileUtil, FileType
from astrophysix.utils.strings import Stringifiable
from astrophysix.utils.persistency import Hdf5StudyPersistent
from .plot import PlotInfo
from .file import AssociatedFile


log = logging.getLogger("astrophysix.simdm")

#
# HDFITS: Porting the FITS data model to HDF5
# https://doi.org/10.1016/j.ascom.2015.05.001
# https://github.com/telegraphic/fits2hdf
#

# class ImportedDataFileNode(DataFileNode):
#     # _hos_version = 2
#     def __init__(self, name, uid=None, description=None, filename=None, file_md5sum=None):
#         super(ImportedDataFileNode, self).__init__(name, uid=uid, description=description)
#
#    def _fits_to_hdf5(self):
#         import h5py
#         f = h5py.File("test.h5", "w")
#         ff = open("parsz.fits", "rb")
#         l = ff.readlines()
#         len(l)
#         import numpy as N
#         print([len(line) for line in l])
#         s = b"".join(l)
#         a = N.void(s)
#         ds = f.create_dataset("a", data=a)
#         ds.dtype
#         f.close()
#         ff.close()
#         mtime = os.path.getmtime("parsz.fits")

#    def _hdf5_to_fits(self):
#         f = h5py.File("test.h5", "r")
#         ds = f["a"]
#         a = ds[...]
#         f.close()
#         sout = a.tobytes()
#         type(sout)
#         ff = open("parsz_out.fits", "wb")
#         ff.write(sout)
#         ff.close()

#         import time
#         import datetime
#         import os
#         date = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
#         modTime = time.mktime(date.timetuple())
#         os.utime(fileLocation, (modTime, modTime))


class Datafile(Hdf5StudyPersistent, Stringifiable):
    def __init__(self, **kwargs):
        """
        Datafile class (Simulation data model)

        Parameters
        ----------
        name: datafile name (mandatory)
        description: datafile description
        """
        super(Datafile, self).__init__(**kwargs)
        self._name = ""
        self._desc = ""
        self._files = {}  # Datafile associated files dictionary, indexed by FileType.
        self._plot_info = None

        # Datafile name
        if "name" not in kwargs:
            raise AttributeError("{cname:s} 'name' attribute is not defined (mandatory).".format(cname=self.__class__.__name__))
        self.name = kwargs["name"]

        if "description" in kwargs:
            self.description = kwargs["description"]

    def __eq__(self, other):
        """
        Datafile comparison method

        Parameters
        ----------
        other: ``Datafile``
            datafile to compare to:
        """
        if not super(Datafile, self).__eq__(other):
            return False

        if self._name != other.name:
            return False

        if self._desc != other.description:
            return False

        # Lazy
        if self.plot_info != other.plot_info:
            return False

        # Datafile comparison
        for ft in FileType:
            try:
                af = self[ft]
            except KeyError:
                af = None
            try:
                oaf = other[ft]
            except KeyError:
                oaf = None
            if oaf is None and af is None:
                continue
            if oaf != af:
                return False

        return True

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_df_name):
        try:
            self._name = Stringifiable.cast_string(new_df_name, valid_empty=False)
        except TypeError:
            err_msg = "{cname:s} 'name' property is not a valid (non-empty) string.".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

    @property
    def description(self):
        return self._desc

    @description.setter
    def description(self, new_descr):
        try:
            self._desc = Stringifiable.cast_string(new_descr)
        except TypeError:
            err_msg = "{cname:s} 'description' property is not a valid string.".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

    def __getitem__(self, ftype):
        """
        Datafile associated file dictionary getter. Fetch associated file given its FileType.

        Parameters
        ----------
        ftype: ``FileType``
            Associated file type

        Returns
        -------
        f: `AssociatedFile`
            datafile associated file of the selected FileType.
        """
        if not isinstance(ftype, FileType):
            err_msg = "{cname:s} '{ft!s}' key is not a valid {ftcname:s} " \
                      "index.".format(cname=self.__class__.__name__, ft=ftype, ftcname=FileType.__name__)
            log.error(err_msg)
            raise KeyError(err_msg)

        f = self._files.get(ftype, None)
        if f is None:
            err_msg = "No {ft:s} file is associated to the {df!s}.".format(ft=ftype.alias, df=self)
            log.error(err_msg)
            raise KeyError(err_msg)

        return f

    def __delitem__(self, ftype):
        """
        Datafile associated file dictionary deleter. Remove associated file given its FileType.

        Parameters
        ----------
        item: ``FileType``
        """
        if not isinstance(ftype, FileType):
            err_msg = "{cname:s} '{ft!s}' key is not a valid {ftcname:s} " \
                      "index.".format(cname=self.__class__.__name__, ft=ftype, ftcname=FileType.__name__)
            log.error(err_msg)
            raise KeyError(err_msg)

        if ftype not in self._files:
            err_msg = "No {ft:s} file is associated to the {df!s}.".format(ft=ftype.alias, df=self)
            log.error(err_msg)
            raise KeyError(err_msg)

        del self._files[ftype]

    def __setitem__(self, filetype, ass_file):
        """
        Satafile associated file dictionary setter. Set an associated file given its FileType.

        Parameters
        ----------
        filetype: ``FileType``
        ass_file: ``str`` or ``AssociatedFile``
            Associated file path or instance 
        """#``AssociatedFile``  object to save in the file dictionary
        if not isinstance(filetype, FileType):
            err_msg = "{cname:s} '{ft!s}' key is not a valid {ftcname:s} " \
                      "index.".format(cname=self.__class__.__name__, ft=filetype, ftcname=FileType.__name__)
            log.error(err_msg)
            raise KeyError(err_msg)

        for kl in AssociatedFile._all_subclasses():
            if kl.FILE_TYPE == filetype:
                if Stringifiable.is_type_string(ass_file):
                    self._files[filetype] = kl.load_file(ass_file)
                elif isinstance(ass_file, AssociatedFile):
                    if not isinstance(ass_file, kl):
                        err_msg = "{cname:s} associated file type mismatch : expected {kname:s} object but " \
                                  "{afc:s} was provided.".format(cname=self.__class__.__name__, kname=kl.__name__,
                                                                 afc=type(ass_file).__name__)
                        log.error(err_msg)
                        raise ValueError(err_msg)
                    self._files[filetype] = ass_file
                else:
                    err_msg = "Only file paths or {kname:s} objects can be set in {cname:s} as {ft:s} " \
                              "files.".format(cname=self.__class__.__name__, kname=kl.__name__, ft=filetype.alias)
                    log.error(err_msg)
                    raise ValueError(err_msg)
                return

        err_msg = "Cannot attach {ft:s} file to datafile !".format(ft=filetype.alias)
        log.error(err_msg)
        raise NotImplementedError(err_msg)

    @property
    def plot_info(self):
        return self._plot_info

    @plot_info.setter
    def plot_info(self, new_pi):
        if not isinstance(new_pi, PlotInfo):
            err_msg = "{cname:s} 'plot_info' property is not a valid PlotInfo " \
                      "object.".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)
        self._plot_info = new_pi

    def __iter__(self):
        for ft, f in self._files.items():
            yield ft, f

    def _hsp_write(self, h5group, **kwargs):
        """
        Serialize a Datafile object into a HDF5 file.

        Parameters
        ----------
        h5group: ``h5py.Group``
            Main group to write the Datafile into.
        kwargs: ``dict``
            keyword argument dictionary.
        """
        # Call to parent class _hsp_write() : write UUID, etc.
        super(Datafile, self)._hsp_write(h5group, **kwargs)

        # Write name
        self._hsp_write_attribute(h5group, ('name', self._name), **kwargs)

        # Write description, if defined
        self._hsp_write_attribute(h5group, ('description', self._desc), **kwargs)

        # Write plot info, if defined
        self._hsp_write_object(h5group, "PLOT_INFO", self._plot_info, **kwargs)

        # Write associated files into HDF5 file
        if not kwargs.get("dry_run", False) and not kwargs.get("new_file", True):  # Old HDF5 file being modified (not a dry run)
            # Delete files from HDF5 group if not present anymore in the datafile
            for ft in FileType:
                if ft.alias in h5group and ft not in self._files:
                    del h5group[ft.alias]

        for ft, f in self._files.items():
            self._hsp_write_object(h5group, ft.alias, f, **kwargs)

    @classmethod
    def _hsp_read(cls, h5group, version, dependency_objdict=None):
        """
        Read a Datafile object from a HDF5 file (*.h5).

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
        df: ``Datafile``
            Read Datafile instance
        """
        # Handle different versions here

        # Fetch Hdf5StudyPersistent object UUID
        uid = super(Datafile, cls)._hsp_read(h5group, version, dependency_objdict=dependency_objdict)

        # Read datafile name
        name = cls._hsp_read_attribute(h5group, 'name', "datafile name")

        # Create datafile object
        df = cls(uid=uid, name=name)

        # Read datafile description, if defined
        df_descr = cls._hsp_read_attribute(h5group, 'description', "datafile description",
                                           raise_error_if_not_found=False)
        if df_descr is not None:
            df.description = df_descr

        # Read plot info
        if "PLOT_INFO" in h5group:
            df.plot_info = PlotInfo._hsp_read_object(h5group, "PLOT_INFO", "plot information")

        # Read associated files from HDF5
        for ft in FileType:
            if ft.alias not in h5group:
                continue
            df[ft] = AssociatedFile._hsp_read_object(h5group, ft.alias, "{ft:s} associated file".format(ft=ft.alias))

        return df

    def __unicode__(self):
        """
        String representation of the Datafile instance
        """
        s = "[{df_name:s}] datafile".format(df_name=self._name)
        return s

    def display_files(self):
        """
        Show tabulated view of associated files

        Examples
        --------
            >>> df.display_files()
            [My best datafile] datafile. Attached files :
            +-----------+-----------------------------+
            | File type |          Filename           |
            +-----------+-----------------------------+
            | PNG       | CEA.png                     |
            +-----------+-----------------------------+
            | JPEG      | irfu_simple.jpg             |
            +-----------+-----------------------------+
            | FITS      | cassiopea_A_0.5-1.5keV.fits |
            +-----------+-----------------------------+
            | TARGZ     | archive.tar.gz              |
            +-----------+-----------------------------+
            | JSON      | test_header_249.json        |
            +-----------+-----------------------------+
            | ASCII     | abstract.txt                |
            +-----------+-----------------------------+
            | HDF5      | study.h5                    |
            +-----------+-----------------------------+
            | PICKLE    | dict_saved.pkl              |
            +-----------+-----------------------------+
        """
        # Empty file dict
        if len(self._files) == 0:
            print(str(self) + " (no attachment)")
            return

        # Display associated file list in a pretty-formatted table
        strrep = str(self) + ". Attached files :\n"
        ft_fname_tuplist = list([(ft.alias, f.filename) for ft, f in self._files.items()])
        nft = N.max([len(t[0]) for t in ft_fname_tuplist])
        ind_header = "File type"
        nft = len(ind_header) if nft < len(ind_header) else nft
        nstr = N.max([len(t[1]) for t in ft_fname_tuplist])
        item_header = "Filename"
        nstr = len(item_header) if nstr < len(item_header) else nstr
        interline = "+-{nind:s}-+-{nstr:s}-+".format(nind=nft*"-", nstr=nstr*"-")
        strrep += interline + "\n| {ind:^{nind}s} | {s:^{nstr}s} |\n".format(nind=nft, ind=ind_header, nstr=nstr,
                                                                             s=item_header)
        for t in ft_fname_tuplist:
            strrep += interline + "\n"
            strrep += "| {ind:<{nind}s} | {s:<{nstr}s} |\n".format(nind=nft, ind=t[0], nstr=nstr, s=t[1])
        strrep += interline

        print(strrep)


__all__ = ["Datafile"]
