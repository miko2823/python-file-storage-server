import requests
import typer

from fs_store.custom_exception import FileNotExistError
from fs_store.config import BASE_URL

app = typer.Typer()


@app.callback()
def server_connection_check():
    try:
        requests.get(BASE_URL)
    except Exception:
        print("Server is not running. Please run the server")


@app.command()
def upload_file(name: str, file_path: str):
    try:
        with open(file_path, "rb") as file:
            files = {"file": file}
            response = requests.post(f"{BASE_URL}/files/{name}", files=files)
            if response.status_code == 201:
                print(f"{name} was successfully uploaded!")
            else:
                print(f"Failed to upload. Server responded with: {response.status_code} {response.text}")
    except Exception as e:
        print(str(e))


@app.command()
def delete_file(name: str):
    try:
        response = requests.delete(f"{BASE_URL}/files/{name}")
        if response.status_code == 200:
            print(f"{name} was successfully deleted!")
        else:
            print(f"Failed to delete. Server responded with: {response.status_code} {response.text}")
    except FileNotExistError as e:
        print(str(e))


@app.command()
def list_files():
    try:
        response = requests.get(f"{BASE_URL}/files")
        if response.status_code == 200:
            print(response.json()["files"])
        else:
            print(f"Failed to upload. Server responded with: {response.status_code} {response.text}")
    except Exception as e:
        print(str(e))
