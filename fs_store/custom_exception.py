class FileNotExistError(Exception):
    def __init__(self, file_name: str):
        message = f"{file_name} Not Found"
        super().__init__(message)
