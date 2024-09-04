# File Storage Server and CLI
This is a simple file server, written in Python. You can also access the server via CLI by installing a build file.

## Server Info
The server provides the following HTTP endpoints.
1. Uploadafile\
POST /files/{name}, Content-Type: multipart/form-data
2. Deleteafile\
DELETE /files/{name}
3. List uploaded files\
GET /files may return a list of files: [file1.txt, file2.txt,]

### How to run the server
Prerequisite: Docker environment

```
$ docker build -t fs_store .
$ docker run -d -p 8000:8000 fs_store
```
If you want to change the host port, change the BASE_URL too at config.py.

## CLI Info
You can access the server via CLI.
1. Uploadafile\
fs-store upload-file {file path}
2. Deleteafile\
fs-store delete-file {filename}
3. List uploaded files\
fs-store list-files

### How to user CLI
Prerequisite: Python environment
```
$ pip install dist/fs_store-0.1.0-py3-none-any.whl
$ fs-store --help
```
## Test
### install Poetry
[Look here for installation](https://python-poetry.org/docs/#installing-with-the-official-installer)

### activate virtual environment
```
$ poetry shell
$ poetry install
```
### run test
```
$ pytest
```
