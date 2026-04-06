#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

from pathlib import Path
import os
import pytest
import shlex
import shutil
import subprocess

class CMakeFixture(object):
    def __init__(self, rootdir, workspace):
        self.rootdir = rootdir
        self.workspace = workspace
        self.build = os.path.join(workspace, "build")

    def execute(self, command):
        if isinstance(command, list):
            command = " ".join(command)
        return subprocess.run(command, capture_output=True, shell=True, encoding="UTF-8")

    def configure_internal(self, options=[]):
        self.copytree("cmake", "cmake")
        command = [f'cmake -S {shlex.quote(self.workspace)} -B {shlex.quote(self.build)} -DCMAKE_BINARY_DIR={shlex.quote(self.workspace)}']
        return self.execute(command + options)

    def configure(self, build="build", testing_enabled=True, cross_toolchain=True, generator="Unix Makefiles", c_compiler_list=None, cpp_compiler_list=None, extra_options=[]):
        self.build = os.path.join(self.workspace, build)

        # Copy source files to workspace
        self.copytree("tests/project", "")

        options = [
            f'-G "{generator}"',
            f'-DCMAKE_TESTING_ENABLED={testing_enabled}',
            f'-DWITH_CROSS_TOOLCHAIN={cross_toolchain}',
            f'-DCMAKE_HOSTC_COMPILER_LIST="{c_compiler_list}"' if c_compiler_list else '',
            f'-DCMAKE_HOSTCXX_COMPILER_LIST="{cpp_compiler_list}"' if cpp_compiler_list else '',
        ] + extra_options
        return self.configure_internal(options)

    def cmake(self, name=None, verbose=False):
        command = [f'cmake --build {shlex.quote(self.build)}', f'--target {name}' if name else '', f'--verbose' if verbose else '']
        return self.execute(command)

    def ctest(self, args=None):
        pwd = os.getcwd()
        os.chdir(self.build)
        try:
            command = ['ctest', args if args else '']
            output = self.execute(command)
        finally:
            os.chdir(pwd)
        return output

    def gcovr(self):
        return self.execute(f'gcovr --root {shlex.quote(self.workspace)} --exclude ".*external.*"')

    def exists(self, path):
        return os.path.exists(os.path.join(self.build, path))

    def read(self, path):
        with open(os.path.join(self.build, path), "r") as f:
            return f.read()

    def write(self, path, content):
        filePath = os.path.join(self.workspace, path)
        os.makedirs(os.path.dirname(filePath), exist_ok=True)
        with open(filePath, "w") as f:
            if isinstance(content, list):
                f.writelines(content)
            else:
                f.write(content)

    def touch(self, path):
        Path(os.path.join(self.workspace, path)).touch()

    def copy(self, source, destination):
        shutil.copy2(f'{self.rootdir}/{source}', f'{self.workspace}/{destination}')

    def copytree(self, source, destination):
        shutil.copytree(f'{self.rootdir}/{source}', f'{self.workspace}/{destination}', dirs_exist_ok=True)

    def mkdirs(self, path):
        os.makedirs(f'{self.workspace}/{path}', exist_ok=True)

    def rmtree(self, path):
        shutil.rmtree(f'{self.workspace}/{path}', ignore_errors=True)

@pytest.fixture
def testing(request, tmpdir_factory):
    directory = str(tmpdir_factory.mktemp("workspace"))
    def cleanup():
        shutil.rmtree(directory)
    request.addfinalizer(cleanup)
    return CMakeFixture(request.config.rootdir, directory)
