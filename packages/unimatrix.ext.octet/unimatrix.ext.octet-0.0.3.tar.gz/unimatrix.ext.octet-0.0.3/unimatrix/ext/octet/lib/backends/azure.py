"""Declares :class:`StorageBackend` for use with Azure Blob Storage."""
import os

from azure.storage.blob import BlobServiceClient # pylint: disable=E0611

from .base import BaseStorageBackend
from .base import RemoteStorageBackendMixin


class StorageBackend(RemoteStorageBackendMixin, BaseStorageBackend): # pylint: disable=R0801
    """A storage backend that uses Azure Blob Storage."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = BlobServiceClient.from_connection_string(
            os.environ['AZURE_STORAGE_CONNECTION_STRING'])
        self.container_name = os.environ['AZURE_STORAGE_CONTAINER_NAME']

    def get_blob_client(self, path):
        """Returns an Azure blob client for the given path."""
        return self.client.get_blob_client(self.container_name,
            self.storage_path(path))

    def close(self, handler):
        """Flush and close the IO object.

        This method has no effect if the file is already closed.
        """
        dst = self.storage_path(handler.path)
        if handler.is_dirty():
            blob = self.get_blob_client(dst)
            with open(handler.fd.name, 'rb') as f:
                blob.upload_blob(f)

    def exists(self, path):
        """Test whether a path exists.  Returns False for broken symbolic links
        if the storage backend supports them.
        """
        return self.get_blob_client(path).exists()

    def read(self, handler, size=-1):
        """Read at most n characters from handler.

        Read from underlying buffer until we have n characters or we hit EOF.
        If n is negative or omitted, read until EOF.
        """
        if size != -1:
            raise NotImplementedError("Partial reads are not implemented.")

        # It supports offset/length so we can implement seeking.
        blob = self.get_blob_client(handler.path)
        stream = blob.download_blob()
        return stream.content_as_bytes()\
            if handler.is_binary()\
            else stream.content_as_text()

    def push(self, src, path):
        """Copies local absolute path `src` to remote `path`."""
        blob = self.get_blob_client(path)
        with open(src, 'rb') as f:
            blob.upload_blob(f)
