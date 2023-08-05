import inspect
import os
from functools import wraps
from io import BytesIO
from gzip import GzipFile

from py2store.base import KvReader, KvPersister
from py2store.filesys import FileCollection
from py2store.util import lazyprop, fullpath


def func_conjunction(func1, func2):
    """Returns a function that is equivalent to lambda x: func1(x) and func2(x)"""
    # Should assert that the input paramters of func1 and func2 are the same
    assert (
            inspect.signature(func1).parameters
            == inspect.signature(func2).parameters
    )

    @wraps(func2)
    def func(*args, **kwargs):
        return func1(*args, **kwargs) and func2(*args, **kwargs)

    return func


def take_everything(fileinfo):
    return True


class GzipReader(KvReader):
    """A KvReader to read the contents of a gzip file.
    Provides a KV perspective of https://docs.python.org/3/library/zipfile.html

    Note: If you get data zipped by a mac, you might get some junk along with it.
    Namely `__MACOSX` folders `.DS_Store` files. I won't rant about it, since others have.
    But you might find it useful to remove them from view. One choice is to use `py2store.trans.filtered_iter`
    to get a filtered view of the zips contents. In most cases, this should do the job:
    ```
    # applied to store instance or class:
    store = filtered_iter(lambda x: not x.startswith('__MACOSX') and '.DS_Store' not in x)(store)
    ```

    Another option is just to remove these from the zip file once and for all. In unix-like systems:
    ```
    zip -d filename.zip __MACOSX/\*
    zip -d filename.zip \*/.DS_Store
    ```

    Examples:
        # >>> s = GzipReader('/path/to/some_zip_file.zip')
        # >>> len(s)
        # 53432
        # >>> list(s)[:3]  # the first 3 elements (well... their keys)
        # ['odir/', 'odir/app/', 'odir/app/data/']
        # >>> list(s)[-3:]  # the last 3 elements (well... their keys)
        # ['odir/app/data/audio/d/1574287049078391/m/Ctor.json',
        #  'odir/app/data/audio/d/1574287049078391/m/intensity.json',
        #  'odir/app/data/run/status.json']
        # >>> # getting a file (note that by default, you get bytes, so need to decode)
        # >>> s['odir/app/data/run/status.json'].decode()
        # b'{"test_phase_number": 9, "test_phase": "TestActions.IGNORE_TEST", "session_id": 0}'
        # >>> # when you ask for the contents for a key that's a directory,
        # >>> # you get a GzipReader filtered for that prefix:
        # >>> s['odir/app/data/audio/']
        # GzipReader('/path/to/some_zip_file.zip', 'odir/app/data/audio/', {}, <function take_everything at 0x1538999e0>)
        # >>> # Often, you only want files (not directories)
        # >>> # You can filter directories out using the file_info_filt argument
        # >>> s = GzipReader('/path/to/some_zip_file.zip', file_info_filt=GzipReader.FILES_ONLY)
        # >>> len(s)  # compare to the 53432 above, that contained dirs too
        # 53280
        # >>> list(s)[:3]  # first 3 keys are all files now
        # ['odir/app/data/plc/d/1574304926795633/d/1574305026895702',
        #  'odir/app/data/plc/d/1574304926795633/d/1574305276853053',
        #  'odir/app/data/plc/d/1574304926795633/d/1574305159343326']
        # >>>
        # >>> # GzipReader.FILES_ONLY and GzipReader.DIRS_ONLY are just convenience filt functions
        # >>> # Really, you can provide any custom one yourself.
        # >>> # This filter function should take a GzipInfo object, and return True or False.
        # >>> # (https://docs.python.org/3/library/zipfile.html#zipfile.GzipInfo)
        # >>>
        # >>> import re
        # >>> p = re.compile('audio.*\.json$')
        # >>> my_filt_func = lambda fileinfo: bool(p.search(fileinfo.filename))
        # >>> s = GzipReader('/Users/twhalen/Downloads/2019_11_21.zip', file_info_filt=my_filt_func)
        # >>> len(s)
        # 48
        # >>> list(s)[:3]
        # ['odir/app/data/audio/d/1574333557263758/m/Ctor.json',
        #  'odir/app/data/audio/d/1574333557263758/m/intensity.json',
        #  'odir/app/data/audio/d/1574288084739961/m/Ctor.json']
    """

    def __init__(
            self,
            source,
            prefix="",
            open_kws=None,
            # file_info_filt=None
    ):
        """

        Args:
            source: A path to make GzipFile(source)
            prefix: A prefix to filter by.
            open_kws:  To be used when doing a GzipFile(...).open
            file_info_filt: Filter for the FileInfo objects (see https://docs.python.org/3/library/zipfile.html)
                of the paths listed in the zip file
        """
        self.open_kws = open_kws or {}
        # self.file_info_filt = file_info_filt or GzipReader.EVERYTHING
        self.prefix = prefix
        if not isinstance(source, GzipFile):
            if isinstance(source, str):
                source = fullpath(source)
            if isinstance(source, dict):
                source = GzipFile(**source)
            elif isinstance(source, (tuple, list)):
                source = GzipFile(*source)
            elif isinstance(source, bytes):
                source = GzipFile(BytesIO(source))
            else:
                source = GzipFile(source)
        self.source = source

    # @classmethod
    # def for_files_only(
    #         cls, source, prefix="", open_kws=None, file_info_filt=None
    # ):
    #     if file_info_filt is None:
    #         file_info_filt = GzipReader.FILES_ONLY
    #     else:
    #         _file_info_filt = file_info_filt
    #
    #         def file_info_filt(x):
    #             return GzipReader.FILES_ONLY(x) and _file_info_filt(x)
    #
    #     return cls(source, prefix, open_kws, file_info_filt)

    # @lazyprop
    # def info_for_key(self):
    #     return {
    #         x.filename: x
    #         for x in self.source.infolist()
    #         if x.filename.startswith(self.prefix) and self.file_info_filt(x)
    #     }

    def __iter__(self):
        # using source.infolist(), we could also filter for info (like directory/file)
        yield from self.info_for_key.keys()

    def __getitem__(self, k):
        if not self.info_for_key[k].is_dir():
            with self.source.open(k, **self.open_kws) as fp:
                return fp.read()
        else:  # is a directory
            return self.__class__(
                self.source, k, self.open_kws, self.file_info_filt
            )

    def __len__(self):
        return len(self.info_for_key)

    @staticmethod
    def FILES_ONLY(fileinfo):
        return not fileinfo.is_dir()

    @staticmethod
    def DIRS_ONLY(fileinfo):
        return fileinfo.is_dir()

    @staticmethod
    def EVERYTHING(fileinfo):
        return True

    def __repr__(self):
        args_str = ", ".join(
            (
                f"'{self.source.filename}'",
                f"'{self.prefix}'",
                f"{self.open_kws}",
                f"{self.file_info_filt}",
            )
        )
        return f"{self.__class__.__name__}({args_str})"


class GzipFilesReader(FileCollection, KvReader):
    """A local file reader whose keys are the zip filepaths of the rootdir and values are corresponding GzipReaders.
    """

    def __init__(
            self,
            rootdir,
            subpath=".+\.zip",
            pattern_for_field=None,
            max_levels=0,
            prefix="",
            open_kws=None,
            file_info_filt=GzipReader.FILES_ONLY,
    ):
        super().__init__(rootdir, subpath, pattern_for_field, max_levels)
        self.zip_reader_kwargs = dict(
            prefix=prefix, open_kws=open_kws, file_info_filt=file_info_filt
        )

    def __getitem__(self, k):
        return GzipReader(k, **self.zip_reader_kwargs)


# TODO: Add easy connection to ExplicitKeymapReader and other path trans and cache useful for the folder of zips context
class FlatGzipFilesReader(GzipFilesReader):
    """Read the union of the contents of multiple zip files.
    A local file reader whose keys are the zip filepaths of the rootdir and values are corresponding GzipReaders.

    """

    @lazyprop
    def _zip_readers(self):
        rootdir_len = len(self.rootdir)
        return {
            path[rootdir_len:]: super(FlatGzipFilesReader, self).__getitem__(
                path
            )
            for path in super().__iter__()
        }

    def __iter__(self):
        for (
                zip_relpath,
                zip_reader,
        ) in self._zip_readers.items():  # go through the zip paths
            for (
                    path_in_zip
            ) in (
                    zip_reader
            ):  # go through the keys of the GzipReader (the zipped filepaths)
                yield (zip_relpath, path_in_zip)

    def __getitem__(self, k):
        (
            zip_relpath,
            path_in_zip,
        ) = k  # k is a pair of the path to the zip file and the path of a file within it
        return self._zip_readers[zip_relpath][path_in_zip]


GzipFileReader = GzipFilesReader  # back-compatibility alias


class FilesOfGzip(GzipReader):
    def __init__(self, source, prefix="", open_kws=None):
        super().__init__(
            source,
            prefix=prefix,
            open_kws=open_kws,
            file_info_filt=GzipReader.FILES_ONLY,
        )


from py2store.errors import OverWritesNotAllowedError


class OverwriteNotAllowed(FileExistsError, OverWritesNotAllowedError):
    ...


class EmptyGzipError(KeyError, FileNotFoundError):
    ...


class _EmptyGzipReader(KvReader):
    def __init__(self, sourcepath):
        self.sourcepath = sourcepath

    def __iter__(self):
        yield from ()

    def infolist(self):
        return []

    def __getitem__(self, k):
        raise EmptyGzipError(
            "The store is empty: GzipStore(sourcepath={self.sourcepath})"
        )

    def open(self, *args, **kwargs):
        raise EmptyGzipError(
            f"The zip file doesn't exist yet! Nothing was written in it: {self.sourcepath}"
        )
        #
        # class OpenedNotExistingFile:
        #     sourcepath = self.sourcepath
        #
        #     def read(self):
        #         raise EmptyGzipError(
        #             f"The zip file doesn't exist yet! Nothing was written in it: {self.sourcepath}")
        #
        #     def __enter__(self, ):
        #         return self
        #
        #     def __exit__(self, *exc):
        #         return False
        #
        # return OpenedNotExistingFile()


from gzip import (
    _COMPRESS_LEVEL_BEST,
)  # TODO: Do all systems have this? If not, need to choose dflt carefully
from gzip import BadGzipFile

DFLT_COMPRESSION = _COMPRESS_LEVEL_BEST


# TODO: Revise GzipReader and GzipFilesReader architecture and make GzipStore be a subclass of Reader if poss
class GzipStore(KvPersister):
    """
    When you want to read zips, there's the `FilesOfGzip`, `GzipReader`, or `GzipFilesReader` we know and love.

    Sometimes though, you want to write to zips too. For this, we have `GzipStore`.

    Since GzipStore can write to a zip, it's read functionality is not going to assume static data,
    and cache things, as your favorite zip readers did.
    This, and the acrobatics need to disguise the weird zipfile into something more... key-value natural,
    makes for a not so efficient store, out of the box.

    I advise using one of the zip readers if all you need to do is read, or subclassing or
     wrapping GzipStore with caching layers if it is appropriate to you.

    """

    _zipfile_init_kw = dict(
        compression=DFLT_COMPRESSION,
        allowZip64=True,
        compresslevel=None,
        strict_timestamps=True,
    )
    _open_kw = dict(pwd=None, force_zip64=False)
    _writestr_kw = dict(compress_type=None, compresslevel=None)
    zip_writer = None

    @wraps(GzipReader.__init__)
    def __init__(
            self,
            sourcepath,
            compression=DFLT_COMPRESSION,
            allow_overwrites=True,
            pwd=None,
    ):
        self.sourcepath = fullpath(sourcepath)
        self.sourcepath = sourcepath
        self.zip_writer_opened = False
        self.allow_overwrites = allow_overwrites
        self._zipfile_init_kw = dict(
            self._zipfile_init_kw, compression=compression
        )
        self._open_kw = dict(self._open_kw, pwd=pwd)

    @staticmethod
    def files_only_filt(fileinfo):
        return not fileinfo.is_dir()

    @property
    def zip_reader(self):
        if os.path.isfile(self.sourcepath):
            return GzipFile(
                self.sourcepath, mode="r", **self._zipfile_init_kw
            )
        else:
            return _EmptyGzipReader(self.sourcepath)

    def __iter__(self):
        # using source.infolist(), we could also filter for info (like directory/file)
        yield from (
            fi.filename
            for fi in self.zip_reader.infolist()
            if self.files_only_filt(fi)
        )

    def __getitem__(self, k):
        with self.zip_reader.open(k, **dict(self._open_kw, mode="r")) as fp:
            return fp.read()

    def __repr__(self):
        args_str = ", ".join(
            (
                f"'{self.sourcepath}'",
                f"'allow_overwrites={self.allow_overwrites}'",
            )
        )
        return f"{self.__class__.__name__}({args_str})"

    def __contains__(self, k):
        try:
            with self.zip_reader.open(
                    k, **dict(self._open_kw, mode="r")
            ) as fp:
                pass
            return True
        except (
                KeyError,
                BadGzipFile,
        ):  # BadGzipFile is to catch when zip file exists, but is empty.
            return False

    # # TODO: Find better way to avoid duplicate keys!
    # # TODO: What's the right Error to raise
    # def _assert_non_existing_key(self, k):
    #     # if self.zip_writer is not None:
    #     if not self.zip_writer_opened:
    #         try:
    #             self.zip_reader.open(k)
    #             raise OverwriteNotAllowed(f"You're not allowed to overwrite an existing key: {k}")
    #         except KeyError as e:
    #             if isinstance(e, EmptyZipError) or e.args[-1].endswith('archive'):
    #                 pass  #
    #             else:
    #                 raise OverwriteNotAllowed(f"You're not allowed to overwrite an existing key: {k}")

    # TODO: Repeated with zip_writer logic. Consider DRY possibilities.
    def __setitem__(self, k, v):
        if k in self:
            if self.allow_overwrites and not self.zip_writer_opened:
                del self[k]  # remove key so it can be overwritten
            else:
                if self.zip_writer_opened:
                    raise OverwriteNotAllowed(
                        f"When using the context mode, you're not allowed to overwrite an existing key: {k}"
                    )
                else:
                    raise OverwriteNotAllowed(
                        f"You're not allowed to overwrite an existing key: {k}"
                    )

        if self.zip_writer_opened:
            with self.zip_writer.open(
                    k, **dict(self._open_kw, mode="w")
            ) as fp:
                return fp.write(v)
        else:
            with GzipFile(
                    self.sourcepath, mode="a", **self._zipfile_init_kw
            ) as zip_writer:
                with zip_writer.open(k, **dict(self._open_kw, mode="w")) as fp:
                    return fp.write(v)

    def __delitem__(self, k):
        try:
            os.system(f"zip -d {self.sourcepath} {k}")
        except Exception as e:
            raise KeyError(f"{e.__class__}: {e.args}")
        # raise NotImplementedError("zipfile, the backend of GzipStore, doesn't support deletion, so neither will we.")

    def open(self):
        self.zip_writer = GzipFile(
            self.sourcepath, mode="a", **self._zipfile_init_kw
        )
        self.zip_writer_opened = True
        return self

    def close(self):
        if self.zip_writer is not None:
            self.zip_writer.close()
        self.zip_writer_opened = False

    __enter__ = open

    def __exit__(self, *exc):
        self.close()
        return False


# TODO: The way prefix and file_info_filt is handled is not efficient
# TODO: prefix is silly: less general than filename_filt would be, and not even producing relative paths
# (especially when getitem returns subdirs)


# trans alternative:
# from py2store.trans import mk_kv_reader_from_kv_collection, wrap_kvs
#
# GzipFileReader = wrap_kvs(mk_kv_reader_from_kv_collection(FileCollection, name='_GzipFileReader'),
#                          name='GzipFileReader',
#                          obj_of_data=GzipReader)

#
# if __name__ == '__main__':
#     from py2store.test.simple import test_local_file_ops
#
#     test_local_file_ops()


if __name__ == '__main__':
    from py2store.slib.s_gzip import GzipReader, GzipFile
