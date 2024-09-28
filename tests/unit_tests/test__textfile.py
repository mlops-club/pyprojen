from pyprojen.project import Project
from pyprojen.textfile import TextFile
from pyprojen.util.synth import synth_snapshot

TEST_FILE_PATH = "hello/foo.txt"


def test__empty_file(test_project: Project):
    """Test that an empty file is created."""
    # GIVEN: The project is already set up by the fixture

    # WHEN: A TextFile is added to the project
    TextFile(scope=test_project, file_path=TEST_FILE_PATH)

    # THEN: Take a snapshot of the project and check the file content
    output: dict = synth_snapshot(test_project)

    assert output[TEST_FILE_PATH] == ""


def test__add_lines(test_project: Project):
    """Test that lines are added to the file."""
    # GIVEN: The project is already set up by the fixture

    # WHEN: A TextFile is added to the project with some lines
    TextFile(scope=test_project, file_path=TEST_FILE_PATH, lines=["line 1", "line 2", "line 3"])

    # THEN: Take a snapshot of the project and check the file content
    output: dict = synth_snapshot(test_project)

    assert output[TEST_FILE_PATH] == "\n".join(["line 1", "line 2", "line 3"])


def test__add_lines_and_append(test_project: Project):
    """Test that lines are added to the file and appended."""
    # GIVEN: The project is already set up by the fixture

    # WHEN: A TextFile is added to the project with some lines
    tf = TextFile(scope=test_project, file_path=TEST_FILE_PATH, lines=["line 1", "line 2"])

    # AND: More lines are appended
    tf.add_line("line 3")
    tf.add_line("line 4")

    # THEN: Take a snapshot of the project and check the file content
    output: dict = synth_snapshot(test_project)

    assert output[TEST_FILE_PATH] == "\n".join(["line 1", "line 2", "line 3", "line 4"])
