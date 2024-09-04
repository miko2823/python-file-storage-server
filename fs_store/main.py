import os

from fastapi import FastAPI, File, UploadFile, HTTPException
from pathlib import Path

from fs_store.custom_exception import FileNotExistError


app = FastAPI()
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/")
async def health_check():
    return True


@app.get("/files/", status_code=200)
async def get_files():
    try:
        files = os.listdir(UPLOAD_DIR)
        return {"files": files}
    except Exception as e:
        HTTPException(status_code=500, detail=str(e))


@app.post("/files/{name}", status_code=201)
async def upload_file(name: str, file: UploadFile = File(...)):
    try:
        file_location = UPLOAD_DIR / name
        with file_location.open("wb") as f:
            f.write(await file.read())

    except Exception as e:
        HTTPException(status_code=500, detail=str(e))


@app.delete("/files/{name}", status_code=200)
async def delete_file(name: str):
    try:
        file_location = UPLOAD_DIR / name
        if not file_location.exists():
            print(file_location, file_location.exists())
            raise FileNotExistError(name)
        file_location.unlink()

    except FileNotExistError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        HTTPException(status_code=500, detail=str(e))
