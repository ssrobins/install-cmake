#!/usr/bin/env python3

# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import unittest
from install_cmake import CMakeInstall, get_cmake_version

class TestMethods(unittest.TestCase):
    def test_suitable_release_found(self):
        cmake_install = CMakeInstall(None, None)
        self.assertFalse(cmake_install.suitable_release_found(""))
        self.assertTrue(cmake_install.suitable_release_found(
            "Latest Release (3.24.3)"))
        self.assertFalse(cmake_install.suitable_release_found(
            "Release Candidate (3.25.0-rc4)"))

    def test_suitable_release_found_rc_flag(self):
        cmake_install = CMakeInstall(None, True)
        self.assertFalse(cmake_install.suitable_release_found(""))
        self.assertTrue(cmake_install.suitable_release_found(
            "Latest Release (3.24.3)"))
        self.assertTrue(cmake_install.suitable_release_found(
            "Release Candidate (3.25.0-rc4)"))

    def test_get_cmake_version(self):
        self.assertEqual(get_cmake_version(""), "")
        self.assertEqual(get_cmake_version("blah"), "")
        self.assertEqual(get_cmake_version("3"), "")
        self.assertEqual(get_cmake_version("cmake version 3.18"), "")
        self.assertEqual(get_cmake_version(
            "cmake version 3.18.4"), "3.18.4")
        self.assertEqual(get_cmake_version(
            "cmake version 3.19.0-rc3"), "3.19.0-rc3")
        self.assertEqual(get_cmake_version(
            "cmake version 99.99.99"), "99.99.99")
        self.assertEqual(get_cmake_version(
            "cmake version 99.99.99-rc99"), "99.99.99-rc99")
        self.assertEqual(get_cmake_version(
            "cmake version 3.19.0-rc3\n\n"
            "CMake suite maintained and supported by Kitware (kitware.com/cmake).\n"), "3.19.0-rc3")


if __name__ == '__main__':
    unittest.main()
