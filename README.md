# The orthw script

The `orthw` shell script can simplify and speed up common tasks for an [ORT][ort] scan of your software project.
For example, you can use:
- `orthw pc-create <package-id>` to generate a [package configuration][ort-package-configurations] file to correct license findings
in an open source dependency.
- `orthw  rc-generate-scope-excludes` to generate [scopes excludes][ort-yml-scope-excludes] in your project's [.ort.yml][ort-yml] file.

Benefits of using the `orthw` script:
- Simplify common ORT scan review tasks such as clearing found licenses.
- Easy to remember CLI commands, and in case you do forget them running `orthw` will show all of them.
- Pre-configured to work with the [ort-config] repository so you can re-use the work of other ORT users.
- Includes commands to format, sort, clean-up and generate ORT config files such as [.ort.yml][ort-yml] and [package configuration][ort-package-configurations].

## Installation

### 1. Prerequisites

The `orthw` requires the following tools to be installed on your system:

* [curl](https://curl.se)
* [jq](https://stedolan.github.io/jq)
* [md5sum](https://linux.die.net/man/1/md5sum)
* [xz](https://linux.die.net/man/1/xz)
* [OpenJDK]()

You can install these tools on your operating system using:
- Ubuntu Linux: 
  - Run: `sudo apt install curl md5sum openjdk-18-jdk xz-utils -y`
- MacOS: 
  - Install [HomeBrew][homebrew] and run: `brew install curl md5sha1sum openjdk xz`
- Windows using Chocolatey and [Git Bash][git-bash]
  - Install [Chocolatey][chocolatey]
  - Run `choco install curl md5 microsoft-openjdk`
  - Alternatively you can also install Microsoft OpenJDK using Powershell _as adminstrator_ and run `winget search Microsoft.OpenJDK`
  - Use [Git Bash][git-bash] as your terminal
- Windows using Windows Subsystem for Linux
  - Install [Ubuntu on WSL for Windows 10][ubuntu-wsl-win-10], or [Ubuntu on WSL for Windows 11][ubuntu-wsl-win-11]
  - Run `sudo apt install curl md5sum openjdk-18-jdk xz-utils -y`

 To verify all tools are correctly installed, open a new terminal and run:

| Command           | Output starts with                 |
|-------------------|------------------------------------|
| `curl --version`  | `curl [VERSION_NUMBER]`            |
| `java -version`   | `openjdk version [VERSION_NUMBER]` |
| `md5sum --version`| `md5sum/sha1sum [VERSION_NUMBER]`  |
| `xz --version`    | `xz (XZ Utils) [VERSION_NUMBER]`   |

Next, you need a copy of the [ORT][ort], [ort-config], [ScanCode][scancode] and the [orthw script][orthw] repositories.

We recommend you clone below-listed repositories in a dedicated directory such as `~/ort-project`:

```bash
mkdir -p ~/ort-project && \
cd ~/ort-project && \
git clone https://github.com/oss-review-toolkit/ort.git && \
git clone https://github.com/oss-review-toolkit/ort-config.git && \
git clone https://github.com/oss-review-toolkit/orthw.git && \
git clone https://github.com/nexB/scancode-toolkit.git
```

Finally, create a `exports` directory which will be used to store exported license finding curations, path excludes and vcs mappings.

```bash
mkdir -p ~/ort-project/exports
```

### 2. Build ORT

Navigate to the directory where you cloned [ORT][ort] repository and run its [native build][ort-build-native] command:

```bash
cd ~/ort-project/ort && \
./gradlew installDist
```

### 3. Make `orthw` Script Executable Everywhere

To make `orthw` executable everywhere, add a `PATH` export to your terminal configuration file.

- Open using text editor either the `~/.bashrc` or `~/.zshrc` file.
- Add a path export pointing to the `orthw` script e.g. `export PATH=" ~/ort-project/orthw/orthw$PATH"`

### 4. Create your `orthw` configuration

- Copy the `orthwconfig-template` file from the orthw repository into your home directory.

```bash
cp ~/ort-project/orthw/orthwconfig-template ~/.orthwconfig
```

- Open using a text editor the `~/.orthwconfig` file.
- Set `ort_home`, `orthw_home`, `configuration_home` and `scancode_home` to respectively the location
  of the ORT, orthw, ORT configuration and ScanCode repositories which you cloned in above [Prerequisites](#1-prerequisites).

  If you followed examples in the previous steps and used a `ort-project` directory then
  the contents of `~/.orthwconfig` file should be as follows:

```
configuration_home=~/ort-project/ort-config

ort_home=~/ort-project/ort

scancode_home=~/ort-project/scancode-toolkit

exports_home=~/ort-project/exports

orthw_home=~/ort-project/orthw
```

### 5. Test if Everything Works

Verify that `orthw` works by opening a new terminal and run `orthw`. 
It should print the full list of available commands and no error messages.

# Usage

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

# Want to Help or have Questions?

All contributions are welcome. If you are interested in contributing, please read our
[contributing guide][ort-contributing], and to get quick answers to any of your questions
we recommend you [join our Slack community][ort-slack].

# License

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
