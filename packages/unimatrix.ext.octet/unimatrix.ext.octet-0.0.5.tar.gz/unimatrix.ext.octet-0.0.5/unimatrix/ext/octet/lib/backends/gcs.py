"""Declares :class:`GoogleCloudStorageBackend`."""
import os

from google.cloud import storage

from .base import BaseStorageBackend
from .base import RemoteStorageBackendMixin


class StorageBackend(RemoteStorageBackendMixin, BaseStorageBackend):
    """A storage backend that uses Google Cloud Storage (GCS)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = storage.Client()
        self.bucket = self.client.get_bucket(os.environ['GOOGLE_GCS_BUCKET'])

    def close(self, handler):
        """Flush and close the IO object.

        This method has no effect if the file is already closed.
        """
        dst = self.storage_path(handler.path)
        if handler.is_dirty():
            blob = self.bucket.blob(dst)
            blob.upload_from_filename(handler.fd.name)

    def exists(self, path):
        """Test whether a path exists.  Returns False for broken symbolic links
        if the storage backend supports them.
        """
        return storage.Blob(bucket=self.bucket, name=self.storage_path(path))\
            .exists(self.client)

    def read(self, handler, size=-1):
        """Read at most n characters from handler.

        Read from underlying buffer until we have n characters or we hit EOF.
        If n is negative or omitted, read until EOF.
        """
        if size != -1:
            raise NotImplementedError("Partial reads are not implemented.")

        # TODO: This is not going to play well with seeking and friends (pylint: disable=W0511).
        blob = self.bucket.blob(self.storage_path(handler.path))
        blob.download_to_filename(handler.fd.name)
        return handler.fd.read(size)

    def push(self, src, path):
        """Copies local absolute path `src` to remote `path`."""
        blob = self.bucket.blob(self.storage_path(path))
        blob.upload_from_filename(src)
