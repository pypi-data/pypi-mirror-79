# pylint: skip-file
import io
import os
import tempfile
import unittest

import unimatrix.lib.test

from ..local import LocalDiskBackend


class LocalDiskBackendTestCase(unittest.TestCase):
    backend_class = LocalDiskBackend

    def setUp(self):
        self.backend = self.get_backend()

    def get_backend(self):
        return self.backend_class(**self.get_backend_kwargs())

    def get_backend_kwargs(self):
        return {
            'base_path': tempfile.mkdtemp()
        }

    def test_context_closes_file(self):
        src = 'foo'
        with self.backend.open(src, 'w') as f:
            f.write("Hello world!")
        with self.backend.open(src) as f:
            pass
        self.assertTrue(f.is_closed())

    def test_write_file_with_context(self):
        src = 'foo'
        with self.backend.open(src, 'w') as f:
            f.write("Hello world!")

        with self.backend.open(src) as fd:
            self.assertEqual(fd.read(), "Hello world!")

    def test_write_file_with_fd(self):
        src = 'foo'
        fd = self.backend.open(src, 'w')
        fd.write("Hello world!")
        fd.close()

        with self.backend.open(src) as fd:
            self.assertEqual(fd.read(), "Hello world!")

    def test_reading_non_existing_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            self.backend.open(bytes.hex(os.urandom(16)))

    def test_write_to_reading_file_raises(self):
        src = 'foo'
        with self.backend.open(src, 'w') as f:
            f.write("foo")
        fd = self.backend.open(src)
        with self.assertRaises(io.UnsupportedOperation):
            fd.write("Hello world!")

    def test_read_from_closed_file_raises(self):
        src = 'foo'
        with self.backend.open(src, 'w') as f:
            f.write("foo")
        fd = self.backend.open(src)
        fd.close()
        with self.assertRaises(ValueError):
            fd.read()

    def test_push(self):
        with tempfile.NamedTemporaryFile() as f:
            f.write(b"Hello world!")
            f.flush()

            fn = bytes.hex(os.urandom(16))
            self.backend.push(f.name, fn)

        self.assertTrue(self.backend.exists(fn))
        with self.backend.open(fn) as f:
            self.assertEqual("Hello world!", f.read())

    def test_read_rb_returns_bytes(self):
        src = 'foo'
        with self.backend.open(src, 'w') as f:
            f.write("Hello world!")

        with self.backend.open(src, 'rb') as fd:
            self.assertIsInstance(fd.read(), bytes)

    def test_read_r_returns_string(self):
        src = 'foo'
        with self.backend.open(src, 'w') as f:
            f.write("Hello world!")

        with self.backend.open(src, 'r') as fd:
            self.assertIsInstance(fd.read(), str)

    def test_read_rt_returns_string(self):
        src = 'foo'
        with self.backend.open(src, 'w') as f:
            f.write("Hello world!")

        with self.backend.open(src, 'rt') as fd:
            self.assertIsInstance(fd.read(), str)
