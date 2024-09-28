import json
import logging
import os
from typing import List

FILE_MANIFEST = ".pyprojen/files.json"


def cleanup(dir: str, new_files: List[str], exclude: List[str]):
    try:
        manifest_files = get_files_from_manifest(dir)
        if manifest_files:
            # Use `FILE_MANIFEST` to remove files that are no longer managed by pyprojen
            remove_files(find_orphaned_files(dir, manifest_files, new_files))
        else:
            # Remove all files managed by pyprojen with legacy logic
            remove_files(find_generated_files(dir, exclude))
    except Exception as e:
        logging.warn(f"warning: failed to clean up generated files: {str(e)}")


def remove_files(files: List[str]):
    for file in files:
        try:
            os.remove(file)
        except Exception as e:
            logging.warn(f"Failed to remove file {file}: {str(e)}")


def find_orphaned_files(dir: str, old_files: List[str], new_files: List[str]) -> List[str]:
    return [os.path.join(dir, f) for f in old_files if f not in new_files]


def find_generated_files(dir: str, exclude: List[str]) -> List[str]:
    # Implement this function to find generated files based on a marker
    # This is a placeholder and should be implemented based on your specific needs
    return []


def get_files_from_manifest(dir: str) -> List[str]:
    try:
        manifest_path = os.path.join(dir, FILE_MANIFEST)
        if os.path.exists(manifest_path):
            with open(manifest_path, "r") as f:
                manifest = json.load(f)
            if "files" in manifest:
                return manifest["files"]
    except Exception as e:
        logging.warn(f"warning: unable to get files to clean from file manifest: {str(e)}")
    return []
