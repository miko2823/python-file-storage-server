import tempfile

from typer.testing import CliRunner

from fs_store.cli import app

runner = CliRunner()


def test_upload_file():
    # given
    file_name_1 = "test1"
    # when
    with tempfile.NamedTemporaryFile() as fp:
        fp.write(b"Hello world!")
        result = runner.invoke(app, ["upload-file", file_name_1, fp.name])
        # then
        assert f"{file_name_1} was successfully uploaded!" in result.stdout
        assert result.exit_code == 0


def test_list_files():
    # given
    file_name_1 = "test1"
    file_name_2 = "test2"

    # when
    with tempfile.NamedTemporaryFile() as fp:
        fp.write(b"Hello world!")
        runner.invoke(app, ["upload-file", file_name_1, fp.name])
        runner.invoke(app, ["upload-file", file_name_2, fp.name])
        result = runner.invoke(app, ["list-files"])
        # then
        assert file_name_1 in result.stdout
        assert file_name_2 in result.stdout
        assert result.exit_code == 0


def test_delete_file():
    # given
    file_name_1 = "test1"
    file_name_2 = "test2"

    # when
    with tempfile.NamedTemporaryFile() as fp:
        fp.write(b"Hello world!")
        runner.invoke(app, ["upload-file", file_name_1, fp.name])
        runner.invoke(app, ["upload-file", file_name_2, fp.name])
        delete_result = runner.invoke(app, ["delete-file", file_name_1])

        # then
        assert f"{file_name_1} was successfully deleted!" in delete_result.stdout
        read_result = runner.invoke(app, ["list-files"])
        assert file_name_1 not in read_result.stdout
        assert file_name_2 in read_result.stdout
        assert read_result.exit_code == 0
