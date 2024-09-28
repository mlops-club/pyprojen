from pyprojen.project import Project
from pyprojen.textfile import TextFile
from pyprojen.util.synth import synth_snapshot


def test__empty_file(test_project: Project):
    """Test that an empty file is created."""
    # GIVEN: The project is already set up by the fixture
    test_file_path = "hello/foo.txt"

    # WHEN: A TextFile is added to the project
    TextFile(scope=test_project, file_path=test_file_path)

    # THEN: Take a snapshot of the project and check the file content
    output: dict = synth_snapshot(test_project)

    assert output[test_file_path] == ""
