# Getting Started

This tutorial is an introduction to the `orthw` script. It shows how to run the script on an [ORT][ort] scan
of the [code repository][mime-types] for the NPM package [mime-types][mime-types-npm] 2.1.26.

The tutorial covers the following steps, which represent a typical `orthw` workflow:

- [Initializing a local directory with an ORT scan result](#orthw-init)
- [Generating a Web App report to see scan results in a web browser](#orthw-report-webapp)
- [Marking files, directories or package manager scopes in your project as not included in released artifacts](#orthw-rc-excludes)
- [Checking your project dependencies for security advisories](#orthw-check-advisories)
- [Correcting missing or incorrect package metadata](#orthw-curations)
- [Marking files or directories in dependency sources as not included in released artifacts](#orthw-pc-excludes)
- [Correcting a detected license found in package source code](#orthw-pc-create)
- [Listing the licenses found in the sources of a package](#orthw-licenses)
- [Listing licenses flagged with a policy violation](#orthw-offending-licenses)
- [Concluding the license for a package](#orthw-concluded-license-curation)

Before you begin working through the tutorial, please complete the [installation instructions][orthw-installation] for `orthw`.

## Initializing a Local Directory with an ORT Scan Result <a name="orthw-init"></a>

This tutorial uses the scan result file
[examples/npm-mime-types-2.1.26-scan-result.json][npm-mime-types-2.1.26-scan-result]
from the [orthw] repository. The file was created by [ORT][ort] applying policy rules, [curations][ort-curations] and [package
configurations](ort-package-configurations) from the [ort-config] repository, commit [04c6b0d][ort-config-04c6b0d].

Run the following command in the terminal to switch your local clone of the [ort-config] repository to this commit:

```
cd ~/ort-project/ort-config && \
git checkout 04c6b0d
```

An essential first step before you can leverage the functionality of `orthw` is to create and initialize a local
directory for a specific scan by running the command `orthw init` in the terminal.

```bash
mkdir -p ~/ort-scans/mime-types-orthw && cd ~/ort-scans/mime-types-orthw
orthw init file:///<path-to-ort-user-directory>/ort-project/orthw/examples/npm-mime-types-2.1.26-scan-result.json
```
Note that the second command (`orthw init`) can be given a CI/CD job artifact URL, instead of a path to a local file:

```bash
orthw init https://raw.githubusercontent.com/oss-review-toolkit/orthw/main/examples/npm-mime-types-2.1.26-scan-result.json
```

Once `orthw init` has successfully finished, `~/ort-scans/mime-types-orthw` should have in it the `ort.yml` file and a
hidden directory named `.orthw` containing the scan results (in a sub-directory).

This [ort.yml][ort-yml] file will either be the same as the [.ort.yml][ort-yml] in the
project repository, or, if there is no `.ort.yml` in the repository, its contents are set to `--- {}`.

Note that the file to which we refer here as the project's `ort.yml` file can have a name specific to the artifact or
release or flavor, provided that it ends with ".ort.yml", for example it can be named "my-artifact.ort.yml". This means that multiple
`*.ort.yml` files can exist in a repository, each specific to a release or flavor of the software.
```
.
├── .orthw
│   ├── scan-result.json
│   ├── scan-results
│   └── target-url.txt
└── ort.yml
```

## Generating a Web App Report to See Scan Results in a Web Browser <a name="orthw-report-webapp"></a>

One of the reports [ORT][ort] can generate is the Web App report. It is a single HTML file containing a JavaScript
web application designed to help you navigate, filter and analyze scan results.

To generate the Web App using `orthw` run:

```bash
cd ~/ort-scans/mime-types-orthw
orthw report-webapp
```
As a result, `~/ort-scans/mime-types-orthw` should now contain a file named `webapp.html`.
When you load the file in a web browser, it opens on the section named "Summary", where the fourth
bullet point from the top shows text in red and reads  _Completed scan with 375 unresolved policy violations_.

### Report Sections

The Web App is divided in three sections or tabs:
- _Summary_: offers an overview of the packages that were scanned along with the detected rule violations, vulnerabilities and licenses
- _Table_: shows a table of packages found during the scan -- you can hide/show columns and filter the table rows
- _Tree_:  presents a browsable and searchable dependency tree of the packages found during the scan

Note that "Rule Violations" under _Summary_ (if shown) as well as _Table_ and _Tree_ mark expandable items with a '+' to the
left of the item name. By clicking on the '+', you can see further detail.

### Package Details

Click the '+' sign to the left of a package id, for example to the left of _NPM::acorn:7.1.1_, to see information such as:
- _Details_: package description, homepage, code repositories, binary and source artifact
- _Licenses_: declared licenses (from package metadata), detected licenses (found in source code), and concluded licenses (human overwrites)
- _Paths_: dependency trail from the root project to the selected package id
- _Scan Results_: copyright and license findings for files included in the source repository or artifact of the selected package id
- _Scope Excludes_: (if present) reasons why the selected package was marked as not included in released artifacts

Note that when rule violations (_Rule Violations_) are displayed below _Summary_, the package-specific information includes _How to Fix_ in
addition to the items shown above. _How to Fix_ shows instructions to help you correct a rule violation.

### About Modal

At the right end of the top line in the Web App report -- the line that shows _Summary_, _Table and _Tree_ -- you will find an icon for the _About_ dialog. Click on it to see:
- _Excludes_: contents of the [.ort.yml][ort-yml] file for the project -- not shown if no `.ort.yml` was found or is empty
- _Labels_: labels that were passed to the ORT _analyzer_, using one or more `-L` parameters -- shown only if labels were set
- _About_: details on the ORT project and the timestamp showing when the report was created

## Marking Files, Directories or Package Manager Scopes in Your Project as not Included in Released Artifacts <a name="orthw-rc-excludes"></a>

It is possible that not every file in the code repository of a software project is included in the release artifacts. For example, build
scripts, documentation or test scripts are often only used for development and are not part of public
release artifacts. Consequently, it makes sense to mark such files in the scan results to avoid reporting policy violations for license findings that have no relevance to the released software.

ORT allows you to mark files as "excluded", by listing them as [excludes][ort-yml-excludes] in
[.ort.yml][ort-yml] (in the software project's repository).

Many package managers support grouping of dependencies according to their use. Such groups are called `scopes` in
ORT. For example, Maven provides the scopes `compile`, `provided`, and `test`, while NPM scopes are `dependencies` and
`devDependencies`.

### Marking Scopes in a Project as Excluded

`orthw` supports package exclusion by scope through the command `rc-generate-scope-excludes`. The command generates
[scope excludes][ort-yml-scope-excludes] as a list of `ort.yml` entries indicating parts of the software that are
used only for development or testing.

1.  To use `orthw` to create scope excludes, run the following commands in the terminal:

```bash
cd ~/ort-scans/mime-types-orthw
orthw rc-generate-scope-excludes
```

2. Open `~/ort-scans/mime-types-orthw/ort.yml` in a text editor. It should contain the following lines:

```
---
excludes:
  scopes:
  - pattern: "devDependencies"
    reason: "DEV_DEPENDENCY_OF"
    comment: "Packages for development only."
```

   The scope `devDependencies` can be excluded as described in the [npm docs][npm-docs-devdependencies] it contains "Packages that are only needed for local development and testing".

4. [Generate the Web App report](#orthw-report-webapp) to see the impact of a [scope exclude][ort-yml-scope-excludes]:

```bash
cd ~/ort-scans/mime-types-orthw
orthw report-webapp
```

5. Open `~/ort-scans/mime-types-orthw/webapp.html` using a web browser.
6. The Web App report's _Summary_ now shows _Completed scan successfully_ and does not list any rule violations.

   Previously, the _Summary_ showed the text _Completed scan with 375 unresolved policy violations_. All of those rule
   violations referred to packages used only in development. By excluding the scope "devDependencies", you have reconfigured the
   [policy rules][ort-config-04c6b0d-rules-kts] used by [ORT][ort] which apply only to non-excluded packages.

### Marking Files and Directories in a Project as Excluded

Besides excluding scopes, you can mark files and directories as excluded in the [.ort.yml][ort-yml] file using [path
excludes][ort-yml-path-excludes].

`orthw` is not able to generate [path excludes][ort-yml-path-excludes], so they must be added manually to
[.ort.yml][ort-yml].

Consider, for example, the [repository for mime types version 2.1.26][mime-types-2.1.26], which contains a directory
named `test`. This directory is not included in the release artifact [mime-types-2.1.26.tgz] and therefore any scanning
findings for the `test` directory in [ORT][ort]'s scan results are non-applicable to [mime-types-2.1.26.tgz].

We can exclude it by adding the following [path exclude][ort-yml-path-excludes] in the [.ort.yml][ort-yml] file:

```
---
excludes:
  paths:
  - pattern: "test/**"
    reason: "TEST_OF"
    comment: "Directory used for testing only."
  scopes:
  - pattern: "devDependencies"
    reason: "DEV_DEPENDENCY_OF"
    comment: "Packages for development only."
```

### Tips for Working with the `.ort.yml` File

- Symlink the `ort.yml` created by `orthw` to the `.ort.yml` in the project code repository, so you can commit your
  changes easily and often
- Do not sort path or scope exclude entries in `ort.yml` manually, but simply add them and use the command `orthw rc-sort`

### Example .ort.yml files

- [The .ort.yml of harp.gl][ort-yml-harp.gl], a 3D web map rendering engine written in TypeScript
- [The .ort.yml of MoveTK][ort-yml-movetk], a c++ library for computational movement analysis
- [The .ort.yml of XYZ Hub][ort-yml-xyz-hub], a RESTful web service for the access and management of geospatial data written in Java

## Checking Project Dependencies for Security Advisories <a name="orthw-check-advisories"></a>

ORT supports querying multiple security advisory providers to help you use open source software in your project safely.

The `~/.orthwconfig` file is preconfigured to use [OSV][osv] as the default advisory provider, but you are free to add other services such as [OSS Index][oss-index] or a local instance of [VulnerableCode][vulnerablecode].

Run the following commands to check your project dependencies for known security vulnerabilities:

```bash
cd ~/ort-scans/mime-types-orthw
orthw check-advisories
```

[Generate the Web App report](#orthw-report-webapp) using `orthw report-webapp` -- the report should now show several security vulnerabilities and an increased number of policy violations under _Summary_.

## Correcting Invalid or Missing Package Metadata <a name="orthw-curations"></a>

You can use [curations][ort-curations] to add or correct missing or invalid package metadata, including the declared
license and code repository information.

In the Web App report, look up `NPM::acorn:7.1.1` by filtering the _Package_ column under _Table_. Notice that the
declared license is MIT, but ORT detected Apache-2.0, BSD-2-Clause, BSD-3-Clause,
LicenseRef-scancode-facebook-patent-rights-2 and MIT, so which licenses apply?

### Determining whether Right Sources Were Scanned

Click the '+' sign to the left of `NPM::acorn:7.1.1` and expand _Scan Results_ to see the copyright and license
findings. You should see entries for the directories `acorn-loose` and `acorn-walk` containing `LICENSE` and
`package.json` files. This is an indication of _overscanning_ -- the scan covering files beyond the sources for the
package due to incorrect package metadata. In this case, the code repository seems to contain multiple packages and the
scan covered them indiscriminately.

To verify if this assumption is correct:

1. Navigate to the _Details_ section under `NPM::acorn:7.1.1`.
2. Download and extract [acorn-7.1.1.tgz].
3. Open the [acorn] repository in a web browser and locate the code for version `7.1.1`.
4. Compare [version 7.1.1 in the repository][acorn-7.1.1] with the extracted contents of [acorn-7.1.1.tgz].
5. You will find the contents of [acorn-7.1.1.tgz] come from the `acorn` directory within [acorn repository][acorn-7.1.1].

An alternative way to confirm that the [acorn repository][acorn-7.1.1] contains multiple npm packages is to simply
search for the package names on [npmjs.com][npmjs]. Both the [acorn-loose][npm-acorn-loose] and
[npm-acorn-walk][npm-acorn-walk] packages can be found on [npmjs.com][npmjs].

The cause of the _overscanning_ can be found in the [repository field of acorn's package.json][acorn-7.1.1-package-vcs],
which is missing a [directory][npm-docs-repository] field to specify the directory in which the package lives:

```
"repository": {
    "type": "git",
    "url": "https://github.com/acornjs/acorn.git"
    "directory": "acorn" // Missing in actual acorn sources
},
```

Although it is not possible to fix the sources of previously released package artifacts, you can use a [VCS path
curation][ort-curations] to add metadata that specifies the missing source code _directory_ for `NPM::acorn:7.1.1`. To
do so:

1. In your local clone of the [ort-config] repository, create `curations/NPM/_/acorn.yml` or, if it already exists, open
   the file in a text editor.
2. Add the lines below to the file to instruct ORT that sources for any version of `NPM::acron` can be found in the
   `acorn` directory within the [acorn] code repository:

```
- id: "NPM::acorn"
  curations:
    comment: "Package resides in its own directory within repo."
    vcs:
      path: "acorn"
```

*Important*: Any time you add a [VCS curation][ort-curations] to [ort-config] you will need to re-scan your
project. Once the re-scan has completed, you should see a reduced number of detected licenses in the Web App report.

### Tips for Working with Curations

- Fix incorrect package metadata upstream if the issue exists in the latest version. Contributing back helps both the
  community and you; once package maintainers are aware of an issue, they can fix it for all the packages
  they maintain.
- When possible, contribute the curations you make to the [ort-config] repository so that any [ORT][ort] user can benefit.

## Marking Files or Directories in Dependency Sources as not Included in Released Artifacts <a name="orthw-pc-excludes"></a>

A [package configuration][ort-package-configurations] allows you to mark files and directories as not included in
release artifacts - this makes it clear that license findings in documentation or tests in the package sources do not
apply to the release (binary) artifact that is a dependency in your project.

[Generate the Web App report](#orthw-report-webapp) and look up `NPM::acorn-jsx:5.2.0` by filtering the _Package_ column
under _Table_. You will find that the declared license is MIT, but the detected licenses are BSD-2-Clause and
MIT. The question arises which of these licenses apply.

### Determining What is Included in a Package

Click the '+' sign on the left of `NPM::acorn-jsx:5.2.0` and expand the _Scan Results_ to see copyright and license
findings. Among them, you should find a single BSD-2-Clause match in `test/tests-jsx.js`. It is likely that the `test`
directory is not included in the release artifact of the package.

To verify this:
1. Navigate to _Details_ under `NPM::acorn-jsx:5.2.0`.
2. Download and extract [acorn-jsx-5.2.0.tgz].
3. Open the [acorn-jsx] repository in a web browser and locate the code for version `5.2.0`.
4. Compare [version 5.2.0 in the repository][acorn-jsx-5.2.0] with the extracted contents of [acorn-jsx-5.2.0.tgz].
5. You should find that [acorn-jsx-5.2.0.tgz] does not contain anything from the `test` directory, which indicates that
   the BSD-2-Clause does not apply to [acorn-jsx-5.2.0.tgz].

### Marking Files or Directories for a Dependency as Excluded

One solution could be to conclude the license for `NPM::acorn-jsx:5.2.0` as MIT. However, it is better to mark the
`test` directory as not included in the released artifact through a [package configuration][ort-package-configurations]
with a _path exclude_. As a general rule, conclude licenses only if they were incorrectly identified, for example if ORT
has detected the BSD-3-Clause license, but it is BSD-2-Clause that actually applies.

1. Run the command below to generate a [package configuration][ort-package-configurations]:

```
orthw pc-create NPM::acorn-jsx:5.2.0
```

2. The command should exit reporting the creation of the file `vcs.yml` in your local clone of the [ort-config]
   repository e.g. `[ort-config]/package-configurations/NPM/_/acorn-jsx/5.2.0/vcs.yml`
3. When you open the newly created `vcs.yml` in a text editor, it should contain:

```
---
id: "NPM::acorn-jsx:5.2.0"
vcs:
  type: "Git"
  url: "https://github.com/acornjs/acorn-jsx.git"
  revision: "c30617bd8d3763ee96fc76abfc0a9bb00e036d68"
```

3. Add a `path_excludes` entry for the `test` directory:

```
---
id: "NPM::acorn-jsx:5.2.0"
vcs:
  type: "Git"
  url: "https://github.com/acornjs/acorn-jsx.git"
  revision: "c30617bd8d3763ee96fc76abfc0a9bb00e036d68"
path_excludes:
- pattern: "test/**"
  reason: "TEST_OF"
```

   The available options for the `reason` field are defined in [PathExcludeReason.kt][ort-path-exclude-reason].

4. [Generate the Web App report](#orthw-report-webapp) using `orthw report-webapp`.
5. Open `~/ort-scans/mime-types-orthw/webapp.html` using a web browser.
6. The Web App report should now show for `NPM::acorn-jsx:5.2.0`:
   - _Detected licenses_: MIT
   - _Detected Excluded_: BSD-2-Clause
   - _Scan Results_: A light grey icon in front the `test` directory rows

## Correcting a Detected License Found in Package Source Code <a name="orthw-pc-create"></a>

Sometimes, the ORT scanner incorrectly identifies licenses in a file or multiple files in a dependency. You can
overwrite such findings by using a [package configuration][ort-package-configurations].

[Generate the Web App report](#orthw-report-webapp) and look up `NPM::eslint-scope:5.0.0` by filtering the _Package_
column under _Table_. You should find that the detected licenses contain NOASSERTION.

All licenses in ORT follow the [SPDX][spdx] license specification and a NOASSERTION in detected licenses means the scanner found something that looks like a license, but was unable to determine which one.

How do we resolve the NOASSERTION to an actual license?

### Determining the Applicable License for a NOASSERTION

1. Click the '+' sign on the left of `NPM::eslint-scope:5.0.0` under _Table_ and expand the _Scan Results_ to see the copyright and license findings.
2. Filter the _Value_ column, selecting only the NOASSERTION and you will find out that the scanner flagged line 54 in `README.md`.
3. Navigate to the _Details_ section under `NPM::eslint-scope:5.0.0`.
4. Open the [eslint-scope] repository in a web browser and find the code for version `5.0.0`.
5. In [version 5.0.0 of the repository][eslint-scope-5.0.0], find the `README` file.
6. Use the [blame view][github-blame-view] in GitHub to locate [line 54][eslint-scope-5.0.0-readme-54].
7. You will find that [line 54][eslint-scope-5.0.0-readme-54] states 'ESLint Scope is licensed under a permissive BSD
   2-clause license.' The NOASSERTION was most likely triggered by the words 'licensed under'.

### Correcting a NOASSERTION match

1. Run the command below to generate a [package configuration][ort-package-configurations]:

```
orthw pc-create NPM::eslint-scope:5.0.0
```

2. When the command completes, it should report the creation of `vcs.yml` in your local clone of the [ort-config] repository, e.g. `[ort-config]/package-configurations/NPM/_/eslint-scope/5.0.0/vcs.yml`
3. Open this new file in a text editor. It should contain the following lines:

```
---
id: "NPM::eslint-scope:5.0.0"
vcs:
  type: "Git"
  url: "https://github.com/eslint/eslint-scope.git"
  revision: "dbddf14d5771b21b5da704213e4508c660ca1c64"
```

3. Add a `license_finding_curations` entry for the NOASSERTION to `vcs.yml`:

```
---
id: "NPM::eslint-scope:5.0.0"
vcs:
  type: "Git"
  url: "https://github.com/eslint/eslint-scope.git"
  revision: "dbddf14d5771b21b5da704213e4508c660ca1c64"
license_finding_curations:
  - path: "README.md"
    start_lines: "54"
    line_count: 1
    detected_license: "NOASSERTION"
    reason: "INCORRECT"
    comment: "Match on 'licensed under'."
    concluded_license: "BSD-2-Clause"
```

The available options for the `reason` field are defined in [LicenseFindingCurationReason.kt][ort-license-finding-curation-reason].

4. When you create _license finding curation_ entries, we recommended that you also create _path excludes_:

```
---
id: "NPM::eslint-scope:5.0.0"
vcs:
  type: "Git"
  url: "https://github.com/eslint/eslint-scope.git"
  revision: "dbddf14d5771b21b5da704213e4508c660ca1c64"
path_excludes:
- pattern: "Makefile.js"
  reason: "BUILD_TOOL_OF"
- pattern: "tests/**"
  reason: "TEST_OF"
license_finding_curations:
  - path: "README.md"
    start_lines: "54"
    line_count: 1
    detected_license: "NOASSERTION"
    reason: "INCORRECT"
    comment: "Match on `licensed under`."
    concluded_license: "BSD-2-Clause"
```

5. [Generate the Web App report](#orthw-report-webapp) with the command `orthw report-webapp`.
6. Open `~/ort-scans/mime-types-orthw/webapp.html` in a web browser.
7. For the package `NPM::eslint-scope:5.0.0`, the Web App report should now show:
   - _Licenses_:
      - _Detected_: BSD-2-Clause
      - _Detected Excluded_: BSD-3-Clause, LicenseRef-scancode-public-domain, MIT
   - _Scan Results_:
      - A light grey icon in front the `Makefile.js` file and `test` directory rows

## Listing the Licenses Found in the Sources of a Package <a name="orthw-licenses"></a>

`orthw` allows you to see the actual license text for any detected license. For example, to see the license matches for
`NPM::mime-types:2.1.26`, run:

```
orthw licenses NPM::mime-types:2.1.26

Downloading sources for NPM::mime-types:2.1.26.
Downloading sources for package 'NPM::mime-types:2.1.26'...
  scan results:
    [0] type=Git, url=https://github.com/jshttp/mime-types.git, path=, revision=73f9933bfa5247337b459240ec67ea6045cdec84

  MIT [0]:
    [0] (+) LICENSE:1-23
    [1] (+) README.md:101-103
    [2] (+) index.js:5-5
    [3] (+) package.json:10-10

    [0]

      (The MIT License)

      Copyright (c) 2014 Jonathan Ong <me@jongleberry.com>
      Copyright (c) 2015 Douglas Christopher Wilson <doug@somethingdoug.com>

      Permission is hereby granted, free of charge, to any person obtaining
      a copy of this software and associated documentation files (the
      'Software'), to deal in the Software without restriction, including
      without limitation the rights to use, copy, modify, merge, publish,
      distribute, sublicense, and/or sell copies of the Software, and to
      permit persons to whom the Software is furnished to do so, subject to
      the following conditions:

      The above copyright notice and this permission notice shall be
      included in all copies or substantial portions of the Software.

      THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
      EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
      MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
      IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
      CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
      TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
      SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

    [1]

      ## License

      [MIT](LICENSE)

    [2]

      * MIT Licensed

    [3]

      "license": "MIT",
```

## Listing Licenses Flagged with a Policy Violation <a name="orthw-offending-licenses"></a>

To see licenses flagged for a policy violation, use the `orthw` command `offending-licenses`.
For example, to see the flagged licenses for `NPM::acorn:7.1.1`, run:

```
orthw offending-licenses NPM::acorn:7.1.1
```

## Concluding the License for a Package <a name="orthw-concluded-license-curation"></a>

To set the concluded license for a package, create a [concluded license curation][ort-curations] by following the workflow
below (recommended).

### License Clearance Workflow

1. Ensure only the actual sources for the package are scanned:
   - Use a [VCS URL curation][ort-curations] to set the correct code repository location.
   - If appropriate, use a [VCS path curation][ort-curations] to set the directory within the code repository that contains the sources for a package.
2. Mark files and directories as not included in released artifacts as necessary:
   - Use a [package configuration][ort-package-configurations] with `path_excludes` to make clear that license findings
     in documentation, build scripts, or tests in the package sources do not apply to the release (binary) artifact, which is a dependency in your project.
3. Correct license scanner findings:
    - Use a [package configuration][ort-package-configurations] with `license_finding_curation` to overwrite scanner
      findings and correct identified licenses for a specific file or files.
4.  If the package includes license choices or there are too many findings to be excluded or curated:
    - Use a [concluded license curation][ort-curations] to set the concluded license for the package.
    - Omit the version number within the id of the curation if you are sure the concluded license applies
      to all versions of the package.

In the Web App report, locate `NPM::spdx-license-ids:3.0.5` by filtering the _Package_ column under _Table_. You will
find hundreds of detected licenses. This is not surprising, given that the description of the package states: "a list of SPDX license identifiers".

You could use a [package configuration][ort-package-configurations] with hundreds of concluded license
`license_finding_curation` entries to set the applicable licenses for `NPM::spdx-license-ids:3.0.5`. However,
the _License Clearance Workflow_ above suggests a simpler solution, which is to conclude the license for
`NPM::spdx-license-ids` as an SPDX license list, which is always licensed under CC-1.0.

1. In your local clone of the [ort-config] repository, create and/or open in a text editor the file `curations/NPM/_/spdx-license-ids.yml`.
2. Add the lines shown below to instruct ORT to conclude the license for any version of `NPM::spdx-license-ids`:

```
- id: "NPM::spdx-license-ids"
  curations:
    comment: |
      The package contains a JSON file with official SPDX identifiers for various open source licenses as defined on https://spdx.dev/licenses/. The list of identifiers itself is licensed under CC0-1.0, see
      https://github.com/spdx/license-list-XML/blob/1387bf927b3499bb5230313b9a43556987b07180/package.json
      and also the mention of `SPDX-License-Identifier: CC0-1.0` in
      https://github.com/spdx/license-list-XML/blob/1387bf927b3499bb5230313b9a43556987b07180/schema/ListedLicense.xsd.
    concluded_license: "CC0-1.0"
```

5. [Generate the Web App report](#orthw-report-webapp) using `orthw report-webapp`.
6. Open `~/ort-scans/mime-types-orthw/webapp.html` in a web browser.
7. The Web App report should now show fewer policy violations under _Summary_ and for `NPM::spdx-license-ids:3.0.5`:
   - _Licenses_:
      - _Detected_: 0BSD, AFL-1.1 .... gSOAP-1.3b, mpich2, zlib-acknowledgement
      - _Concluded_: CC-1.0
   - _Scan Results_:
      - No changes

[acorn]: https://github.com/acornjs/acorn
[acorn-7.1.1]: https://github.com/acornjs/acorn/tree/7.1.1
[acorn-7.1.1-package-vcs]: https://github.com/acornjs/acorn/blob/7.1.1/acorn/package.json#L26-L29
[acorn-7.1.1.tgz]: https://registry.npmjs.org/acorn/-/acorn-7.1.1.tgz
[acorn-jsx]: https://github.com/acornjs/acorn-jsx.git
[acorn-jsx-5.2.0]: https://github.com/acornjs/acorn-jsx/tree/5.2.0
[acorn-jsx-5.2.0.tgz]: https://registry.npmjs.org/acorn-jsx/-/acorn-jsx-5.2.0.tgz
[eslint-scope]: https://github.com/eslint/eslint-scope.git
[eslint-scope-5.0.0]: https://github.com/eslint/eslint-scope/tree/v5.0.0
[eslint-scope-5.0.0-readme-54]: https://github.com/eslint/eslint-scope/blame/v5.0.0/README.md#L54
[github-blame-view]: https://docs.github.com/en/repositories/working-with-files/using-files/viewing-a-file#viewing-the-line-by-line-revision-history-for-a-file
[ort]: https://github.com/oss-review-toolkit/ort
[ort-config]: https://github.com/oss-review-toolkit/ort-config
[ort-config-04c6b0d]: https://github.com/oss-review-toolkit/ort-config/tree/04c6b0d
[ort-config-04c6b0d-rules-kts]: https://github.com/oss-review-toolkit/ort-config/blob/04c6b0d/evaluator-rules/src/main/resources/example.rules.kts
[ort-curations]: https://github.com/oss-review-toolkit/ort/blob/main/docs/config-file-curations-yml.md
[ort-package-configurations]: https://github.com/oss-review-toolkit/ort/blob/main/docs/config-file-package-configuration-yml.md
[ort-path-exclude-reason]: https://github.com/oss-review-toolkit/ort/blob/main/model/src/main/kotlin/config/PathExcludeReason.kt
[ort-license-finding-curation-reason]: https://github.com/oss-review-toolkit/ort/blob/main/model/src/main/kotlin/config/LicenseFindingCurationReason.kt
[ort-yml]: https://github.com/oss-review-toolkit/ort/blob/main/docs/config-file-ort-yml.md
[ort-yml-excludes]: https://github.com/oss-review-toolkit/ort/blob/main/docs/config-file-ort-yml.md#excludes
[ort-yml-harp.gl]: https://github.com/heremaps/harp.gl/blob/4aa6f2d27e5367367e03f824f9407524e147836f/.ort.yml
[ort-yml-movetk]: https://github.com/movetk/movetk/blob/dd0c4700fe52c864ce5f311b2602b83e2cad174c/.ort.yml
[ort-yml-path-excludes]: https://github.com/oss-review-toolkit/ort/blob/main/docs/config-file-ort-yml.md#excluding-paths
[ort-yml-scope-excludes]: https://github.com/oss-review-toolkit/ort/blob/main/docs/config-file-ort-yml.md#excluding-scopes
[ort-yml-xyz-hub]: https://github.com/heremaps/xyz-hub/blob/4a4281af71119ab258a2bcb141141c99bce0519c/.ort.yml
[orthw]: https://github.com/oss-review-toolkit/orthw
[orthw-installation]: ../README.md#installation
[oss-index]: https://ossindex.sonatype.org/
[osv]: https://osv.dev/
[mime-types]: https://github.com/jshttp/mime-types.git
[mime-types-2.1.26]: https://github.com/jshttp/mime-types/tree/2.1.26
[mime-types-2.1.26.tgz]: https://registry.npmjs.org/mime-types/-/mime-types-2.1.26.tgz
[mime-types-npm]: https://www.npmjs.com/package/mime-types
[npm-acorn-loose]: https://www.npmjs.com/package/acorn-loose
[npm-acorn-walk]: https://www.npmjs.com/package/acorn-walk
[npm-docs-devdependencies]: https://docs.npmjs.com/specifying-dependencies-and-devdependencies-in-a-package-json-file
[npm-docs-repository]: https://docs.npmjs.com/cli/v8/configuring-npm/package-json#repository
[npm-mime-types-2.1.26-scan-result]: ../examples/npm-mime-types-2.1.26-scan-result.json
[npmjs]: https://npmjs.com
[spdx]: https://spdx.dev
[vulnerablecode]: https://github.com/nexB/vulnerablecode
