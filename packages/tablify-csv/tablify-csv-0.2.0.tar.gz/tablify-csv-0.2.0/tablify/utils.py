"""
Miscellaneous utility functions
"""


def save_to_file(contents: str, filepath: str) -> None:
    """Writes `contents` to a file saved in `filepath`."""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(contents)
