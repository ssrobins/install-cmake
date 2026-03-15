#!/usr/bin/env python3

# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import unittest
from unittest.mock import patch
from install_cmake import CMakeInstall, get_cmake_version, get_cmake_platform

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
        self.assertEqual(get_cmake_version(
            "'3.24.3'"), "3.24.3")
        self.assertEqual(get_cmake_version(
            '"3.24.3"'), "3.24.3")

    def test_get_cmake_platform_darwin(self):
        with patch("platform.system", return_value="Darwin"):
            result = get_cmake_platform()
        self.assertEqual(result, ("macos-universal", ".tar.gz", "CMake.app/Contents/bin"))

    def test_get_cmake_platform_linux_x86_64(self):
        with patch("platform.system", return_value="Linux"), \
             patch("platform.machine", return_value="x86_64"):
            result = get_cmake_platform()
        self.assertEqual(result, ("linux-x86_64", ".tar.gz", "bin"))

    def test_get_cmake_platform_linux_aarch64(self):
        with patch("platform.system", return_value="Linux"), \
             patch("platform.machine", return_value="aarch64"):
            result = get_cmake_platform()
        self.assertEqual(result, ("linux-aarch64", ".tar.gz", "bin"))

    def test_get_cmake_platform_windows_x86_64(self):
        with patch("platform.system", return_value="Windows"), \
             patch("platform.machine", return_value="AMD64"):
            result = get_cmake_platform()
        self.assertEqual(result, ("windows-x86_64", ".zip", "bin"))

    def test_get_cmake_platform_windows_arm64(self):
        with patch("platform.system", return_value="Windows"), \
             patch("platform.machine", return_value="ARM64"):
            result = get_cmake_platform()
        self.assertEqual(result, ("windows-arm64", ".zip", "bin"))

    def test_cmake_install_windows_arm_requires_324(self):
        with patch("platform.system", return_value="Windows"), \
             patch("platform.machine", return_value="ARM64"):
            with self.assertRaises(SystemExit):
                CMakeInstall("3.23.0", None)

    def test_cmake_install_windows_arm_allows_324(self):
        with patch("platform.system", return_value="Windows"), \
             patch("platform.machine", return_value="ARM64"):
            cmake_install = CMakeInstall("3.24.0", None)
        self.assertEqual(cmake_install.version, "3.24.0")

    def test_get_cmake_platform_unsupported_arch(self):
        with patch("platform.system", return_value="Linux"), \
             patch("platform.machine", return_value="riscv64"):
            self.assertRaises(RuntimeError, get_cmake_platform)

    def test_get_cmake_platform_unsupported_system(self):
        with patch("platform.system", return_value="FreeBSD"):
            self.assertRaises(RuntimeError, get_cmake_platform)


if __name__ == '__main__':
    unittest.main()
