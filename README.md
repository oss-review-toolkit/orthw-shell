This repository is about (semi-) automating ORT support tasks relating to OSS compliance scans. It is the place to put
scripts, configuration and data files such as re-usable curations.

# The `orthw` script

`orthw` is a shell script that provides a set of commands for working with a specific scan result. Thus, the first step
is to initialize an arbitrary empty directory with a scan result using the `orthw init` command. After that, you
can issue further commands: run `orthw` without any arguments to see all the available options.

To fix issues with a scan result, you will most likely need to set entries in the local and global configuration,
i.e. the file `.ort.yml` and the files within the `configuration repository`, respectively. All `orthw` commands use the
local copy of these files (on your hard drive), which means the changes you make are applied instantly, considerably
shortening the feedback cycle, compared to running a scan remotely (on Jenkins). For example, you can make a
configuration change and then regenerate all reports with the command `orthw report` or you can recreate a specific
report, with a command like `orthw report-html`, which usually takes a few seconds to a minute.

Besides generating `ORT` reports `orthw` provides many other helpful commands, e.g. for investigating license
findings, adding entries to the copyright garbage list, sharing `path excludes` and `license finding curations` across
different projects or `.ort.yml` files as well as formatting, sorting, cleaning-up and generating `.ort.yml` entries.
The following sections explain the use of some of the commands and illustrate suggested `orthw`-based workflows. The
intention is to get you started, rather than provide a comprehensive guide. Please try out the available
commands to explore and learn.

Note: A major design goal of the commands is to provide a granularity just fine enough to allow for separate atomic
commits made-up of the commands outputs.

## Setup

1. Install the prerequisites: `sudo apt install curl jq md5sum xz`
2. Put `orthw` on the system path, e.g. create a symbolic link to `orthw` in the `bin` directory (alternatively copy
   `orthw` to `bin`, but remember to do that again after each update)
3. Copy `orthwconfig-template` to a file `~/.orthwconfig`
4. Clone the OSS repositories `configuration`, `ort`, `scancode-toolkit` and set the parameters in
   `~/.orthwconfig` to point to those local clones and to `support` (this repository)
5. Build `ORT` (`ort` repository cloned in the previous step) via `./gradlew installDist`
4. Verify that `orthw` works by proceeding with the following two sections

Note that the parameters (point 4 above) must be set for the Bash session you use to execute any of the commands below,
otherwise the commands will fail.

## Using the commands

### Run the analyzer

You can choose to run the analyzer in the Docker container that is used on Jenkins or on your local system.

```bash
mkdir dir-for-result && cd dir-for-result
orthw analyze <source-code-dir>            # To run the analyzer without Docker.
orthw analyze-in-docker <source-code-dir>  # To run the analyzer in the Docker container.
```

### Initializing a directory

```bash
mkdir dir-for-scan && cd dir-for-scan
orthw init https://example.com/scans/123456/scan-result.json
cat ort.yml
# Note that `init` extracts the `ort.yml` from the given scan-result, ready to be edited.
# In order to make commits to that ort.yml file it is recommended to replace it with a symbolic
# link to your `ort.yml` within your clone of your source code repository.
```

### Computing a scan report

To compute reports based on your copy of the local and global configuration, run any of the following commands in an
`initialized` directory:

```bash
orthw report          # Compute all reports like static HTML, Web-App or a `FOSS_NOTICE` file.
orthw report-html     # Compute only the static HTML report.
orthw report-*        # Compute any other single report, see also list of available commands.
```

### Basic `.ort.yml` setup

Perform the following steps in this order to produce a good basic `ort.yml` file to which you can make further manual
additions as needed:

#### Apply default formatting

```bash
orthw rc-format
```

#### Sort the entries alphabetically

```bash
orthw rc-sort
```

#### Remove obsolete entries

```bash
orthw rc-clean <source-code-dir>
```

#### Generating scope excludes

```bash
orthw rc-generate-scope-excludes
```

#### Importing and exporting path excludes from other projects

This repository has a database file holding path excludes with high re-use potential, see `path-excludes.yml`. 
The `import` command automatically picks entries potentially applicable to your project, but the entries do not always apply and need to be reviewed. After
finishing your OSS review, you can share your path excludes to help others by using the `export` command.

Tip: Use a diff-tool (like bcompare) for editing the export before committing to avoid errors and to save time.

```bash
orthw rc-import-path-excludes <source-code-dir>
...
orthw rc-export-path-excludes
```

#### Importing and exporting license finding curations

Similar to the previous section also license findings can be `imported` and `exported` via:
```bash
orthw rc-import-curations
...
orthw rc-export-curations
```

### Listing license findings

This section illustrates all commands for listing license findings. In order to reproduce the examples please run the
following init command first:
```bash
orthw init https://example.com/scans/123456/scan-result.json
```

#### All license findings for a package

1. grouped by license text
  ```bash
  # Fast variant as sources are provided (revision needs to match scanned revision):
  orthw licenses Unmanaged:manifest.xml:manifest:91a99da65c0e1558085b01b0de44ddf38e376a48 ~/sources/repo/manifest/
  # Slow variant as sources are downloaded:
  orthw licenses Unmanaged:manifest.xml:manifest:91a99da65c0e1558085b01b0de44ddf38e376a48
  ```
2. not grouped (note the `dot` at the end)
  ```bash
  orthw licenses Unmanaged:manifest.xml:manifest:91a99da65c0e1558085b01b0de44ddf38e376a48 .
  ```

#### Only offending license findings for a package

1. grouped by license text
  ```bash
  # Fast variant as sources are provided (revision needs to match scanned revision):
  orthw offending-licenses Unmanaged:manifest.xml:manifest:91a99da65c0e1558085b01b0de44ddf38e376a48 ~/sources/repo/manifest/
  # Slow variant as sources are downloaded:
  orthw offending-licenses Unmanaged:manifest.xml:manifest:91a99da65c0e1558085b01b0de44ddf38e376a48
  ```
2. not grouped
  ```bash
  orthw offending-licenses Unmanaged:manifest.xml:manifest:91a99da65c0e1558085b01b0de44ddf38e376a48 .
  ```

#### Output format explained

1. There are exactly 6 findings with 2 distinct license texts referred to by `[0]` or `[1]`
2. `[-]` would indicate that the license text could not be resolved
3. `excluded` / `not excluded` is indicated by `(-)` / `(+)`

```
NCSA:
  [0] (+) external/boost/include/boost/chrono/detail/scan_keyword.hpp:6-7
  [0] (+) external/boost/include/boost/chrono/io/time_point_io.hpp:11-12
  [0] (+) external/boost/include/boost/thread/detail/invoke.hpp:19-20
  [0] (+) external/boost/include/boost/thread/detail/invoker.hpp:17-18
  [0] (+) external/boost/include/boost/thread/detail/make_tuple_indices.hpp:15-16

  [0]

    // This file is dual licensed under the MIT and the University of Illinois Open
    // Source Licenses. See LICENSE.TXT for details.

  [1]

    # This file is distributed under the University of Illinois Open Source
    # License. See LICENSE.TXT for details.
```

### Resolving scan timeout issues

There is only one way of addressing scan timeout issues, which is by creating an `IssueResolution`. You should
prefer global over local resolutions in order to minimize effort. The resolution has to make clear via its comment entry why
it is OK not to scan this file. Common reasons are:
* The file does not contain license information (applicable also to binary files)
* The file does have license information, but there are many other files containing the same license
  text which do get successfully scanned
* It's **not distributed** is **not a valid reason**!

The command below generates template entries for the resolutions. Sometimes it makes sense to merge the entries by
adjusting the regex matching the file path to match multiple files.
```bash
orthw rc-generate-timeout-error-resolutions
```

### Copyright statements

The input for the generation of NOTICE files contains a set of `raw copyright statements` per `license`, which are
filtered by the `copyright-garbage.yml` black-list. That black-list allows a company-wide elimination of false copyright
statement detections. After the statements are filtered by that black-list, they get processed further in order to make
the NOTICE file more compact and readable. In order to show the `processed` statements to be put in the notices and the
corresponding `raw` statements, run the following command and view the output files.
```bash
orthw copyrights
Results written to: copyrights.txt, copyrights-debug.txt.
```

#### Adding entries to the copyright garbage list

Open the generated `copyrights.txt` in a text editor and remove all lines except the ones to be black-listed. Afterwards, run the
command below which merges the garbage entries into a `copyright-garbage.yml` file located in the `configuration`
repository. Note that the `merge` command determines all `raw copyright statements` corresponding to the given
`processed copyright statements` and adds them to the black-list.

```bash
orthw export-copyright-garbage
```   

## An `orthw` based workflow for OSS reviews

The steps below work quite efficiently for us in particular for C/C++ projects.

1. Perform the basic `.ort.yml` setup as described in its dedicated section above
2. Go through all analyzer issues and add path excludes for each if applicable
3. Fix offending licenses in C/C++ sources (and dependency sources present in the HERE source tree)
  1. Iterate over the output of `orthw offending licenses` and add path excludes if applicable
  2. Iterate over the output of `orthw offending licenses` and add license finding curations if applicable
  3. Last resort: Add rule violation resolutions for all remaining offending licenses if applicable
  4. If a license issue remains, it needs to be fixed
4. Fix offending licenses in dependencies (managed by a package manager)
  1. Pick any package with a offending license and set the concluded license in `curations.yml` if applicable
  2. Regenerate the report to see the effect via `orthw report-html`
5. Create resolutions for all scan timeout issues as described in its own section
6. Fix the FOSS_NOTICE file
  1. Check if there is any copyright statement which is actually garbage
  2. If so add all such entries to `copyright-garbage.yml` as described in above section
  3. Recompute the FOSS_NOTICE file via `orthw report-notices` to see the effect

Tips:
* Make the `ort.yml` in your `orthw` directory a symlink to a VCS-managed file so that you can commit your changes often
* Do not waste time finding a place for a new entry in the `ort.yml`. Just pick a random place and use the
  `rc-sort` command
