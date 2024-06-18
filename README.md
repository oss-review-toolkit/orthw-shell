# The orthw script

`orthw` is a shell script designed to simplify and speed up common tasks performed when processing [ORT][ort]
scan results. It supports a number of commands, which can be run in the terminal (e.g. Bash).

For example:
- To correct license findings in an open source dependency, you can run `orthw pc-create <package-id>`, which generates
  a [package configuration][ort-package-configurations] file.
- To indicate that certain items are internal to the project (and so license findings should not be reported against them), you can generate scope excludes for your project's  [.ort.yml][ort-yml] file with the command `orthw  rc-generate-scope-excludes` generates [scope excludes][ort-yml-scope-excludes].

## Benefits of `orthw`

`orthw`:
  - Simplifies common ORT scan review tasks such as clearing found licenses.
  - Offers easy to remember CLI commands (but should you forget, run `orthw` with no arguments to see a complete list).
  - Includes commands to format, sort, clean up and generate ORT config files such as [.ort.yml][ort-yml] and [package configuration][ort-package-configurations].
  - Is pre-configured to work with the [ort-config] repository allowing you to re-use the work of other ORT users.

## Installation

### 1. Prerequisites

`orthw` requires the following tools to be installed on the system where you intend to run it:

* [python](https://curl.se)

The next step is to clone the repositories of [ORT][ort], [ort-config], [ScanCode][scancode] and [orthw][orthw].
Run the commands shown below in a dedicated directory such as `~/ort-project`:

```bash
mkdir -p ~/ort-project && \
cd ~/ort-project && \
git clone https://github.com/oss-review-toolkit/ort.git && \
git clone https://github.com/oss-review-toolkit/ort-config.git && \
git clone https://github.com/oss-review-toolkit/orthw.git && \
git clone https://github.com/nexB/scancode-toolkit.git
```

Finally, create an `exports` directory which will be used to store exported license finding curations and path excludes.

```bash
mkdir -p ~/ort-project/exports
```

### 2. Build ORT

Navigate to the directory where you cloned the [ORT][ort] repository and run its [native build][ort-build-native] command:

```bash
cd ~/ort-project/ort && \
./gradlew installDist
```

### 3. Create your `orthw` configuration

- Copy the `orthwconfig-template` file from the orthw repository into your home directory.

```bash
cp ~/ort-project/orthw/orthwconfig-template ~/.orthwconfig
```

- Open `~/.orthwconfig` in a text editor.
- Set `ort_home`, `orthw_home`, `configuration_home` and `scancode_home` to the location of the ORT, orthw, ORT
  configuration and ScanCode repositories which you cloned in above [Prerequisites](#1-prerequisites), respectively.

  If you followed examples in the previous steps and used a `ort-project` directory then
  the contents of `config.yaml` file.

  The file is present in follow OS directories:

  * **Linux**  ~/.config/orthw
  * **Mac OS X** ~/Library/Application Support/orthw
  * **Windows** C:\\Users\\<userid>\\Local\\orthw\\Config

   should in thebe as follows:

```
configuration_home: ~/ort-project/ort-config

ort_home: ~/ort-project/ort

scancode_home: ~/ort-project/scancode-toolkit

exports_home: ~/ort-project/exports

orthw_home: ~/ort-project/orthw
```

### 4. Install `orthw` 



### 5. Test if Everything Works

Verify that `orthw` works by  running `orthw` in a new terminal window: `orthw` should print the full list of available commands and no error messages.

## Usage

Follow the [Getting Started][gs] guide to learn how to use `orthw` to:
- [Initializing a local directory with an ORT scan result][gs-orthw-init]
- [Generating a Web App report to see scan results in a web browser][gs-orthw-report-webapp]
- [Marking files, directories or package manager scopes in your project as not included in released artifacts][gs-orthw-rc-excludes]
- [Checking your project dependencies for security advisories][gs-orthw-check-advisories]
- [Correcting missing or incorrect package metadata][gs-orthw-curations]
- [Marking files or directories in the sources of a dependency as not included in released artifacts][gs-orthw-pc-excludes]
- [Correcting a detected license found in package source code][gs-orthw-pc-create]
- [Listing the licenses found in the sources of a package][gs-orthw-licenses]
- [Listing licenses flagged with a policy violation][gs-orthw-offending-licenses]
- [Conclude the license for a package][gs-orthw-concluded-license-curation]

## Development

PYTHONPATH=$PWD/src
export PYTHONPATH
pip install poetry
python -m poetry
poetry install
python -m orthw

poetry up -> update deps

To check your path is correctly configured

`python -c "import sys; print('\n'.join(sys.path))"`

python -m orthw package-config create Maven:org.eclipse.platform:org.eclipse.osgi:3.18.200 

pip install ptpython

import 

## Contributing to `orthw` and Questions

All contributions are welcome. If you are interested in contributing, please read our
[contributing guide][ort-contributing]. To get quick answers to any of your questions
we recommend that you [join our Slack community][ort-slack].

## License

Copyright (C) 2019-2022 HERE Europe B.V.\
Copyright (C) 2022 EPAM Systems, Inc.

See the [LICENSE](./LICENSE) file in the root of this project for license details.

OSS Review Toolkit (ORT) is a [Linux Foundation project](https://www.linuxfoundation.org) and part of
[ACT](https://automatecompliance.org/).

[chocolatey]: https://chocolatey.org/
[git-bash]: https://git-scm.com/download/win
[gs]: docs/getting-started.md
[gs-orthw-check-advisories]: docs/getting-started.md#orthw-check-advisories
[gs-orthw-copyrights]: docs/getting-started.md#orthw-copyrights
[gs-orthw-concluded-license-curation]: docs/getting-started.md#orthw-concluded-license-curation
[gs-orthw-curations]: docs/getting-started.md#orthw-curations
[gs-orthw-init]: docs/getting-started.md#orthw-init
[gs-orthw-license-choice]: docs/getting-started.md#orthw-license-choice
[gs-orthw-licenses]: docs/getting-started.md#orthw-licenses
[gs-orthw-offending-licenses]: docs/getting-started.md#orthw-offending-licenses
[gs-orthw-pc-create]: docs/getting-started.md#orthw-pc-create
[gs-orthw-pc-excludes]: docs/getting-started.md#orthw-pc-excludes
[gs-orthw-report-webapp]: docs/getting-started.md#orthw-report-webapp
[gs-orthw-rc-excludes]: docs/getting-started.md#orthw-rc-excludes
[homebrew]: https://brew.sh/
[ort]: https://github.com/oss-review-toolkit/ort
[ort-config]: https://github.com/oss-review-toolkit/ort-config
[ort-contributing]: https://github.com/oss-review-toolkit/.github/blob/main/CONTRIBUTING.md
[ort-curations]: https://github.com/oss-review-toolkit/ort/blob/main/docs/config-file-curations-yml.md
[ort-build-native]: https://github.com/oss-review-toolkit/ort#build-natively
[ort-package-configurations]: https://github.com/oss-review-toolkit/ort/blob/main/docs/config-file-package-configuration-yml.md
[ort-slack]: https://join.slack.com/t/ort-talk/shared_invite/zt-1c7yi4sj6-mk7R1fAa6ZdW5MQ6DfAVRg
[ort-yml]: https://github.com/oss-review-toolkit/ort/blob/main/docs/config-file-ort-yml.md
[ort-yml-scope-excludes]: https://github.com/oss-review-toolkit/ort/blob/main/docs/config-file-ort-yml.md#excluding-scopes
[orthw]: https://github.com/oss-review-toolkit/orthw
[scancode]: https://github.com/nexB/scancode-toolkit
[ubuntu-wsl-win-10]: https://ubuntu.com/tutorials/install-ubuntu-on-wsl2-on-windows-10#1-overview
[ubuntu-wsl-win-11]: https://ubuntu.com/tutorials/install-ubuntu-on-wsl2-on-windows-11-with-gui-support#1-overview
