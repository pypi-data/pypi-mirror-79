"""Declares :class:`LocalDiskBackend`."""
import shutil
import os

from .base import BaseStorageBackend


class LocalDiskBackend(BaseStorageBackend):
    """A storage backend that uses the local filesystem."""

    def close(self, handler):
        """Flush and close the IO object.

        This method has no effect if the file is already closed.
        """
        handler.fd.close()

    def exists(self, path):
        """Test whether a path exists.  Returns False for broken symbolic links
        if the storage backend supports them.
        """
        return os.path.exists(self.storage_path(path))

    def get_local_fd(self, handler):
        """Opens a local file descriptor."""
        return open(self.storage_path(handler.path), handler.mode)

    def read(self, handler, size=-1):
        """Read at most n characters from handler.

        Read from underlying buffer until we have n characters or we hit EOF.
        If n is negative or omitted, read until EOF.
        """
        return handler.fd.read(size)

    def push(self, src, path):
        """Copies local absolute path `src` to remote `path`."""
        shutil.copy2(src, self.storage_path(path))
