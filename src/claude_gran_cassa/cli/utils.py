from pathlib import Path
import re


def get_versioned_filename(base_path: Path) -> Path:
    """Create a versioned filename to prevent overwrites"""
    if not base_path.exists():
        return base_path

    stem = base_path.stem
    suffix = base_path.suffix
    parent = base_path.parent

    match = re.match(r"(.*?)_v(\d+)$", stem)
    if match:
        stem = match.group(1)
        version = int(match.group(2)) + 1
    else:
        version = 1

    return parent / f"{stem}_v{version}{suffix}"
