import os
from pathlib import Path

from hyd.backend.util.const import LOADER_HTML_INJECTION


def inject_js_loader_to_html(*, dir_path: Path) -> None:
    html_files: list[Path] = []
    _recursive_html_file_search(dir_path=dir_path, html_files=html_files)

    for file in html_files:
        with open(file, "a") as handle:
            handle.write("\n" + LOADER_HTML_INJECTION)


def reinject_js_loader_to_html(*, dir_path: Path) -> None:
    html_files: list[Path] = []
    _recursive_html_file_search(dir_path=dir_path, html_files=html_files)

    for file in html_files:
        with open(file, "r+", encoding="utf-8") as handle:
            handle.seek(0, os.SEEK_END)
            pos = handle.tell()
            while pos > 0 and handle.read(1) != "\n":
                pos -= 1
                handle.seek(pos, os.SEEK_SET)
            if pos > 0:
                handle.seek(pos, os.SEEK_SET)
                handle.truncate()
            handle.write("\n" + LOADER_HTML_INJECTION)


def _recursive_html_file_search(*, dir_path: Path, html_files: list[Path]) -> None:
    for entry in dir_path.iterdir():
        if entry.is_dir():
            _recursive_html_file_search(dir_path=entry, html_files=html_files)
        elif entry.is_file() and entry.suffix == ".html":
            html_files.append(entry)
