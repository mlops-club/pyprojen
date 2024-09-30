import tempfile
import shutil
from pyprojen.project import Project


class TestProject(Project):
    """Test project setup for pyprojen."""

    def __init__(self, **kwargs):
        self.outdir = tempfile.mkdtemp()
        super().__init__(name="test-project", outdir=self.outdir, **kwargs)

    def cleanup(self):
        shutil.rmtree(self.outdir)