#!/usr/bin/env python3

import argparse
import os
import platform
import re
import requests
import subprocess
import tarfile
import zipfile
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from urllib.request import build_opener, HTTPCookieProcessor, install_opener, Request, urlopen


class CMakeInstall:
    def __init__(self, version):
        if version:
            self.version = version
        else:
            self.version = self.get_latest_cmake_version_cmake()

        self.download_timeout_seconds = 10
        self.download_retry_count = 3
        self.download_backoff_factor = 10

        if platform.system() == "Darwin":
            cmake_platform = "macos-universal"
            cmake_archive_ext = ".tar.gz"
            cmake_binary_dir = "CMake.app/Contents/bin"
        elif platform.system() == "Linux":
            cmake_platform = "linux-x86_64"
            cmake_archive_ext = ".tar.gz"
            cmake_binary_dir = "bin"
        elif platform.system() == "Windows":
            cmake_platform = "windows-x86_64"
            cmake_archive_ext = ".zip"
            cmake_binary_dir = "bin"

        cmake_dir = f"cmake-{self.version}-{cmake_platform}"
        self.archive = f"{cmake_dir}{cmake_archive_ext}"
        self.url = f"https://github.com/Kitware/CMake/releases/download/v{self.version}/{self.archive}"
        self.script_path = os.path.dirname(os.path.realpath(__file__))
        self.path = os.path.join(self.script_path, cmake_dir, cmake_binary_dir)


    def get_latest_cmake_version_cmake(self):
        opener = build_opener(HTTPCookieProcessor())
        install_opener(opener)
        req = Request("https://cmake.org/download/", headers={"User-Agent": "Mozilla/72 (X11; Linux i686)"})
        page = urlopen(req).read().decode('utf8', errors='ignore')
        soup = BeautifulSoup(page, "html.parser")
        version_items = soup.find("h3").text.strip().split()
        cmake_version = version_items[2].strip("()")
        return cmake_version


    def get_installed_cmake_version(self, cmake_version_output):
        cmake_version = ""
        match = re.search("\d+\.\d+\.\d+(\-rc\d+)?", cmake_version_output)
        if match:
            cmake_version = match.group(0)
        return cmake_version


    def requested_cmake_is_different(self):
        cmake_version_output = subprocess.run("cmake --version", shell=True, check=True, capture_output=True)
        cmake_version_output = cmake_version_output.stdout.decode("utf-8")
        installed_cmake_version = self.get_installed_cmake_version(cmake_version_output)
        if installed_cmake_version == self.version:
            print(f"Requested CMake {self.version} matches what's already installed", flush=True)
            return False
        else:
            print(f"Requested CMake is {self.version} while {installed_cmake_version} is currently installed", flush=True)
            return True


    def download(self):
        retry_strategy = Retry(
            total=self.download_retry_count,
            backoff_factor=self.download_backoff_factor,
        )
        adapter = HTTPAdapter(max_retries = retry_strategy)
        http = requests.Session()
        http.mount("https://", adapter)
        http.mount("http://", adapter)

        try:
            print(f"Downloading {self.url}", flush=True)
            request = http.get(self.url, timeout=self.download_timeout_seconds, stream=True)
            request.raise_for_status()
        except requests.exceptions.RequestException as error:
            print("Download failed", flush=True)
            print(error, flush=True)
            exit(1)

        with open(self.archive, 'wb') as f:
            f.write(request.content)


    def extract(self):
        print(f"Extracting {self.archive} to {self.script_path}", flush=True)
        if "tar" in self.archive:
            with tarfile.open(f"{self.archive}", "r:gz") as tar:
                tar.extractall(path=self.script_path)
        elif "zip" in self.archive:
            with zipfile.ZipFile(f"{self.archive}", 'r') as zip:
                zip.extractall(path=self.script_path)
        else:
            print("Unsupported archive: {self.archive}", flush=True)
            exit(1)
        subprocess.run(os.path.join(self.path, "cmake --version"), shell=True, check=True)


    def set_path(self):
        if "GITHUB_PATH" in os.environ:
            print(f"Write CMake path, {self.path}, to {os.environ['GITHUB_PATH']}", flush=True)
            with open(os.environ["GITHUB_PATH"], "a") as envfile:
                envfile.write(self.path)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--version",
        help="CMake version in the form 3.18.4 or 3.19.0-rc2 for RCs", required=False
    )
    parser.add_argument("--test",
        action="store_true",
        required=False,
        help="Run unit tests"
    )

    cmake_args = parser.parse_args()

    if cmake_args.test:
        subprocess.run(os.path.join(os.path.dirname(__file__), "install_cmake_tests.py"), shell=True, check=True)

    cmake_install = CMakeInstall(cmake_args.version)
    if cmake_install.requested_cmake_is_different():
        cmake_install.download()
        cmake_install.extract()
        cmake_install.set_path()
    else:
        print("Skipping install", flush=True)

if __name__ == "__main__":
    main()
