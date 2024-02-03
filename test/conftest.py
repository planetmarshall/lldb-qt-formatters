import os
from subprocess import run
from tempfile import NamedTemporaryFile

import pytest


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "lldb_script: specify script to run in lldb"
    )


@pytest.fixture(scope="session")
def exe(tmp_path_factory):
    repository_root = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
    build_folder = tmp_path_factory.mktemp("build")
    cmake_preset = os.environ.get("CMAKE_PRESET", "linux-gcc-debug")
    cmake_configure = ["cmake", "--preset", cmake_preset, "-S", repository_root, "-B", build_folder]
    cmake_build = ["cmake", "--build", build_folder]
    run(cmake_configure)
    run(cmake_build)

    return build_folder / "bin" / "example"


@pytest.fixture
def lldb(request, exe):
    preamble = [
        "command script import lldb_qt_formatters",
        "breakpoint set --file main.cpp --line 14",
        "run"
    ]
    marker = request.node.get_closest_marker("lldb_script")
    test_script = marker.args[0] if marker is not None else ""

    script = "\n".join(preamble + [test_script.lstrip(" \n")])

    with NamedTemporaryFile("w") as fp:
        fp.write(script)
        fp.flush()

        lldb_command = ["lldb", "--batch", "--source", fp.name, exe]
        result = run(lldb_command, check=True, text=True, capture_output=True)
        yield result.stdout

        # TODO (andrew) work out how to just print the lldb output if the test fails
        print(result.stdout)

