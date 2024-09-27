import os
import glob

def cleanup(outdir: str, files: list[str], exclude: list[str]):
    """
    Clean up orphaned files in the output directory.

    :param outdir: The output directory to clean
    :param files: List of files to keep
    :param exclude: List of glob patterns to exclude from cleanup
    """
    for root, _, filenames in os.walk(outdir):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            relative_path = os.path.relpath(file_path, outdir)
            if relative_path not in files and not any(glob.fnmatch.fnmatch(relative_path, pattern) for pattern in exclude):
                os.remove(file_path)