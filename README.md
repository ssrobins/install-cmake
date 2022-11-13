# Install CMake
This GitHub Action installs CMake so you can use the latest release or release candidate or set the specific version you have installed. CMake is already installed and regularly updated as part of the provided [runner images](https://github.com/actions/runner-images/tree/main/images) so it's most useful in the following situations:
- You want to be on the latest CMake at all times
- You want to stay on a specific release of CMake at all times
- You want to use release candidates for early access to new features or to help with testing
- You maintain your own runner and you want a way to install CMake

## Usage
Available inputs are descriibed [here](action.yml).

Install the latest version of CMake with one line:
```yaml
- uses: ssrobins/install-cmake@v1
```
Same as above, but with a custom step name:
```yaml
- name: Install CMake
  uses: ssrobins/install-cmake@v1
```
Allow latest CMake install to be a release candidate, if available:
```yaml
- name: Install CMake
  uses: ssrobins/install-cmake@v1
  with:
    release-candidate: true
```
Use `version` to specify a particular version of CMake in the form of `3.24.3` or `3.25.0-rc4` for RCs. NOTE: Currently, only `3.20.0` or higher are supported, but that can be changed if there's a need for it.
```yaml
- name: Install CMake
  uses: ssrobins/install-cmake@v1
  with:
    version: 3.24.3
```
Add `continue-on-error: true` if you don't want a failure of CMake installation to affect the outcome of your GitHub Action:
```yaml
- name: Install CMake
  uses: ssrobins/install-cmake@v1
  continue-on-error: true
```

## Contributing
I want this to be useful to the whole community so if you have an idea, please post an [issue](https://github.com/ssrobins/install-cmake/issues) or a [pull request](https://github.com/ssrobins/install-cmake/pulls). I'll do my try to my best respond in a few days. All I ask for is the following:
- Clearly articulate the goal of a change
- Make sure PR checks pass
- Be nice!

## Under-the-hood
This GitHub Action is a [composite action](https://docs.github.com/en/actions/creating-actions/creating-a-composite-action). Here are all the parts:
- [action.yml](action.yml) defines the inputs and steps to perform the action
- [install_cmake.py](install_cmake.py) is the script that actually does the install
- [install_cmake_tests.py](install_cmake_tests.py) runs the unit tests for the script
- [.github/workflows/main.yml](.github/workflows/main.yml) is the GitHub Action that runs unit tests as well as the action on several environments

The CMake install itself is simply a download and extraction of the tar/zip archives into the GitHub Actions workspace so it's only present in that particular actions run and won't affect any existing CMake installations on the machine. In order for the `cmake` command to use this local install, it outputs the path to the `$GITHUB_PATH` environment file so it will ultimately be added to environment's `PATH` environment variable. More info in the [GitHub documentation](https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#adding-a-system-path).

The determination of the latest release and release candidate is done with a web scraping of https://cmake.org/download/. The download URL is formed from the established pattern  that's been around since `3.20.0`, which is why the current minimum is set to that (for now, at least). So, if either cmake.org or 