#!/usr/bin/env python3

# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import unittest
from install_cmake import CMakeInstall

class TestMethods(unittest.TestCase):
    def test_get_installed_cmake_version(self):
        cmake_install = CMakeInstall(None, None)
        self.assertEqual(cmake_install.get_installed_cmake_version(""), "")
        self.assertEqual(cmake_install.get_installed_cmake_version("blah"), "")
        self.assertEqual(cmake_install.get_installed_cmake_version("3"), "")
        self.assertEqual(cmake_install.get_installed_cmake_version("cmake version 3.18"), "")
        self.assertEqual(cmake_install.get_installed_cmake_version(
            "cmake version 3.18.4"), "3.18.4")
        self.assertEqual(cmake_install.get_installed_cmake_version(
            "cmake version 3.19.0-rc3"), "3.19.0-rc3")
        self.assertEqual(cmake_install.get_installed_cmake_version(
            "cmake version 99.99.99"), "99.99.99")
        self.assertEqual(cmake_install.get_installed_cmake_version(
            "cmake version 99.99.99-rc99"), "99.99.99-rc99")
        self.assertEqual(cmake_install.get_installed_cmake_version(
            "cmake version 3.19.0-rc3\n\n"
            "CMake suite maintained and supported by Kitware (kitware.com/cmake).\n"), "3.19.0-rc3")


if __name__ == '__main__':
    unittest.main()
