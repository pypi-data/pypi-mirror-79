"""Declares :class:`BaseStorageBackend`."""
import abc
import os
import tempfile

from ..descriptor import Descriptor


class BaseStorageBackend(metaclass=abc.ABCMeta):
    """The base class for all storage backends.

    Args:
        base_path (str): the base path from where the storage backend
            reads and writes files.

    .. warning::
        The constructor should not be overridden.
    """
    descriptor_class = Descriptor

    @property
    def base_path(self):
        """Return the base path of the storage backend."""
        return self.__base_path

    def __init__(self, base_path):
        self.__base_path = base_path

    def close(self, handler):
        """Flush and close the IO object.

        This method has no effect if the file is already closed.
        """
        raise NotImplementedError("Subclasses must override this method.")

    def push(self, src, path):
        """Copies local absolute path `src` to remote `path`."""
        raise NotImplementedError("Subclasses must override this method.")

    def exists(self, path):
        """Test whether a path exists.  Returns False for broken symbolic links
        if the storage backend supports them.
        """
        raise NotImplementedError("Subclasses must override this method.")

    def get_local_fd(self, handler):
        """Opens a local file descriptor."""
        raise NotImplementedError("Subclasses must override this method.")

    def open(self, path, mode='rt', *args, **kwargs): # pylint: disable=W1113
        """Open the given `path` in the given `mode`."""
        return self.descriptor_class(self, path, mode, *args, **kwargs)

    def read(self, handler, size=-1):
        """Read at most n characters from handler.

        Read from underlying buffer until we have n characters or we hit EOF.
        If n is negative or omitted, read until EOF.
        """
        raise NotImplementedError("Subclasses must override this method.")

    def storage_path(self, *components):
        """Returns the absolute path in the storage of `path`."""
        return os.path.join(self.base_path or '', *components)


class RemoteStorageBackendMixin: # pylint: disable=R0903
    """Overrides :class:`BaseStorageBackend` methods for use with remote
    storage backends.
    """

    def get_local_fd(self, handler): # pylint: disable=R0201
        """Opens a local file descriptor."""
        _, src = tempfile.mkstemp()
        return open(src, handler.mode)
