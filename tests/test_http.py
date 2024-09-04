import tempfile
from typing import ClassVar
from unittest import TestCase

from fastapi.testclient import TestClient

from fs_store import main


class TestHttpRequest(TestCase):

    client: ClassVar[TestClient]

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(main.app)

    def test_upload_file(self):
        # given
        file_name_1 = "test1"
        with tempfile.NamedTemporaryFile() as fp:
            fp.write(b"Hello world!")
            file = {"file": fp}
            # when
            result = self.client.post(f"/files/{file_name_1}", files=file)
            # then
            self.assertEqual(result.status_code, 201)

    def test_list_files(self):
        # given
        file_name_1 = "test1"
        with tempfile.NamedTemporaryFile() as fp:
            fp.write(b"Hello world!")
            file = {"file": fp}
            result = self.client.post(f"/files/{file_name_1}", files=file)
            # when
            result = self.client.get("/files/")
            # then
            self.assertEqual(len(result.json()["files"]), 1)

    def test_delete_file(self):
        # given
        file_name_1 = "test1"
        with tempfile.NamedTemporaryFile() as fp:
            fp.write(b"Hello world!")
            file = {"file": fp}
            result = self.client.post(f"/files/{file_name_1}", files=file)
            # when
            result = self.client.delete(f"/files/{file_name_1}")
            # then
            self.assertEqual(result.status_code, 200)
            result = self.client.get("/files/")
            self.assertEqual(len(result.json()["files"]), 0)

    def test_delete_file_FILE_NOT_FOUND(self):
        # given
        file_name_1 = "test1"
        file_name_2 = "not_found"

        with tempfile.NamedTemporaryFile() as fp:
            fp.write(b"Hello world!")
            file = {"file": fp}
            self.client.post(f"/files/{file_name_1}", files=file)
            # when
            result = self.client.delete(f"/files/{file_name_2}")
        # then
        self.assertEqual(result.json()["detail"], f"{file_name_2} Not Found")
