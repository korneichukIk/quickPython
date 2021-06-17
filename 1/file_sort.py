import os
import getpass
import pathlib

extensions = {
    "video": [
        "mp4",
        "mov",
        "avi",
        "mkv",
        "wmv",
        "3gp",
        "3g2",
        "mpg",
        "mpeg",
        "m4v",
        "h264",
        "flv",
        "rm",
        "swf",
        "vob",
    ],
    "data": [
        "sql",
        "sqlite",
        "sqlite3",
        "csv",
        "dat",
        "db",
        "log",
        "mdb",
        "sav",
        "tar",
        "xml",
    ],
    "audio": [
        "mp3",
        "wav",
        "ogg",
        "flac",
        "aif",
        "mid",
        "midi",
        "mpa",
        "wma",
        "wpl",
        "cda",
    ],
    "image": [
        "jpg",
        "png",
        "bmp",
        "ai",
        "psd",
        "ico",
        "jpeg",
        "ps",
        "svg",
        "tif",
        "tiff",
    ],
    "archive": ["zip", "rar", "7z", "z", "gz", "rpm", "arj", "pkg", "deb"],
    "text": ["pdf", "txt", "doc", "docx", "rtf", "tex", "wpd", "odt"],
    "presentation": ["pptx", "ppt", "pps", "key", "odp"],
    "spreadsheet": ["xlsx", "xls", "xlsm", "ods"],
    "font": ["otf", "ttf", "fon", "fnt"],
    "gif": ["gif"],
}


def get_key_by_value(ext: str) -> str:
    for key, value in extensions.items():
        if ext in value:
            return key

    return "EMPTY"


def create_folders(sorted_folder_path: str) -> None:
    for key in extensions:
        pathlib.Path(sorted_folder_path + "/" + key).mkdir(exist_ok=True)


def sort_files(download_path: str):
    filenames = []
    (_, _, filenames) = next(os.walk(download_path), (None, None, []))
    for filename in filenames:
        file_extension = filename.split(".")[-1]
        file_type = get_key_by_value(file_extension)

        if file_type != "EMPTY":
            os.replace(
                download_path + "/" + filename,
                download_path + "/sorted/" + file_type + "/" + filename,
            )


def remove_empty_folders(sorted_path: str):
    for key in extensions:
        if len(os.listdir(sorted_path + "/" + key)) == 0:
            try:
                pathlib.Path(sorted_path + "/" + key).rmdir()
            except OSError:
                pass


if __name__ == "__main__":
    download_path = "/home/{}/Downloads".format(getpass.getuser())
    sorted_path = download_path + "/sorted"
    pathlib.Path(sorted_path).mkdir(exist_ok=True)

    create_folders(sorted_path)
    sort_files(download_path)
    remove_empty_folders(sorted_path)
