import shutil
import tempfile
from typing import (
    Any,
    Generator,
)

import pytest

from pyprojen.project import Project


@pytest.fixture(scope="function")
def test_project() -> Generator[Project, Any, None]:
    """Create a temporary project for testing."""
    # Setup: Create a TestProject instance with a temporary directory
    outdir = tempfile.mkdtemp()
    project = Project(name="test-project", outdir=outdir)

    # Yield the project for use in the test
    yield project

    # Teardown: Cleanup the temporary directory after the test
    shutil.rmtree(outdir)
