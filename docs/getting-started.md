# Getting Started

This tutorial gives a brief introduction to how one can use the `orthw` script on a [ORT][ort] scan
of the [code repository][mime-types-github] of the [mime-types][mime-types-npm] 2.1.26 NPM package.

The steps assume you already have followed the [installation instructions][orthw-installation] for `orthw`.

It will guide you through the following workflow steps for `orthw` to :

- [Initializing a local directory with an ORT scan result](#orthw-init)
- [Generating a Web App report to see scan results in a web browser](#orthw-report-webapp)
- [Marking files, directories or package manager scopes in your project as not included in released artifacts](#orthw-rc-excludes)
- [Checking your project dependencies for security advisories](#orthw-check-advisories)
- [Correcting missing or incorrect package metadata](#orthw-curations)
- [Marking files or directories in the sources of a dependency as not included in released artifacts](#orthw-pc-excludes)
- [Correcting a detected license found in package source code](#orthw-pc-create)
- [Listing the licenses found in the sources of a package](#orthw-licenses)
- [Listing licenses flagged with a policy violation](#orthw-offending-licenses)
- [Conclude the license for a package](#orthw-concluded-license-curation)

## Initializing a Local Directory with an ORT Scan Result <a name="orthw-init"></a>

For this tutorial we are going to use [examples/npm-mime-types-2.1.26-scan-result.json][npm-mime-types-2.1.26-scan-result] found within [orthw] repository. This scan result file was created using the policy rules, [curations][ort-curations] and [package configurations][ort-package-configurations] from the [ort-config] repository commit [04c6b0d][ort-config-04c6b0d].

To switch your local clone of the [ort-config] repository to this commit run:

```
cd ~/ort-project/ort-config && \
git checkout 04c6b0d
```

The first step to use `orthw`, is to _initialize_ a directory using the `orthw init` command.

```bash
mkdir -p ~/ort-scans/mime-types-orthw && cd ~/ort-scans/mime-types-orthw
orthw init file:///Users/ort-user/ort-project/orthw/examples/npm-mime-types-2.1.26-scan-result.json
```
or alternatively, you pass it a URL for example the ORT scan result in the job artifacts from a CI/CD run:

```bash
mkdir -p ~/ort-scans/mime-types-orthw && cd ~/ort-scans/mime-types-orthw
orthw init https://raw.githubusercontent.com/oss-review-toolkit/orthw/examples/npm-mime-types-2.1.26-scan-result.json
```

Once `orthw init` command successfully finishes the contents of  `~/ort-scans/mime-types-orthw` should have a hidden directory named `.orthw` containing the scan results and the `ort.yml` file.

The [ort.yml][ort-yml] file will either contain the contents of the [.ort.yml][ort-yml] file as found in the root of the project, or `--- {}` if no `.ort.yml` was found.

```
.
├── .orthw
│   ├── scan-result.json
│   ├── scan-results
│   └── target-url.txt
└── ort.yml
```

## Generating a Web App Report to see Scan Results in a Web Browser <a name="orthw-report-webapp"></a>

One of the reports [ORT][ort] can generate is the Web App report - a single HTML file containing a JavaScript-based
web application designed to make it easier to navigate, filter and analyze scan results.

To generate the Web App using `orthw` run:

```bash
cd ~/ort-scans/mime-types-orthw
orthw report-webapp
```
Afterwards `~/ort-scans/mime-types-orthw` directory should contain a file named `webapp.html`.
Open using a web browser `webapp.html` and the Web App report should read _Completed scan with 375 unresolved policy violations_.

### Report Sections

The Web App is divided in three sections:
- _Summary_: Overview of what was scanned and resulting rule violations, vulnerabilities and found licenses
- _Table_: Found packages displayed as a table of which you can hide/show columns and filter its rows
- _Tree_: Found packages displayed as a browsable and searchable dependency tree

### Package Details

Click any '+' sign in front of a package id, such as _NPM::ansi-regex:3.0.0_ to see additional information such as:
- _Package details_: description, homepage, code repositories, binary and source artifact
- _Licenses_: declared licenses (from package metadata), detected licenses (found in source code), and concluded licenses (human overwrites)
- _Paths_: dependency trail from root project to opened package id
- _Scan Results_: copyright and licenses findings for files included in the source repository or artifact of opened package id
- _Scope Excludes_: reasons why opened package id was marked as not included in released artifacts

### About Modal

In the top-right corner of the Web App report you can find the _About_ button which, if clicked, shows you:
- _Excludes_: contents of the [.ort.yml][ort-yml] file for the project. Not shown if no `.ort.yml` was found
- _Labels_: labels were passed to the ORT _analyzer_ using one or more `-L` parameters. Not shown if no labels were set
- _About_: details on the ORT project and render timestamp for the report

## Marking Files, Directories or Package Manager Scopes in your Project as not Included in Released Artifacts <a name="orthw-rc-excludes"></a>

Not every file in the code repository of a software project is included in its release artifacts things such as build scripts, documentation or tests are often only used internally and are not released. You may want the treat these project internal files differently when reviewing license findings, e.g. a GPL-2.0-only licensed build script may be OK but GPL-2.0-only source code file which is included in the release artifacts may be not OK.

In ORT you can add defined [excludes][ort-yml-excludes] in a file named [.ort.yml][ort-yml] in the root of a software project to be scanned to define which OSS is distributed to third parties and which code is only used internally, e.g. for building, documenting or testing the code.

Many package managers support grouping of dependencies by their use. Such groups are called scopes in ORT. For example, Maven provides the scopes compile, provided, and test, while NPM scopes are dependencies and devDependencies.

### Marking Scopes in a Project as Excluded

1. Use `orthw rc-generate-scope-excludes` to generate so-called [scope excludes][ort-yml-scope-excludes] entries for scopes used only for development or testing:

```bash
cd ~/ort-scans/mime-types-orthw
orthw rc-generate-scope-excludes
```

2. Open `~/ort-scans/mime-types-orthw` in a text editor. It should contain the following:

```
---
excludes:
  scopes:
  - pattern: "devDependencies"
    reason: "DEV_DEPENDENCY_OF"
    comment: "Packages for development only."
```

   The scope `devDependencies` can be excluded as per the [npm docs][npm-docs-devdependencies] it contains _"Packages that are only needed for local development and testing."_.

4. [Generate the Web App report](#orthw-report-webapp) to see the impact of applying a [scope exclude][ort-yml-scope-excludes]:

```bash
cd ~/ort-scans/mime-types-orthw
orthw rc-generate-scope-excludes
```

5. Open `~/ort-scans/mime-types-orthw/webapp.html` using a web browser.
6. The Web App report should show _Completed scan successfully_ under _Summary_.

   Previously the _Completed scan with 375 unresolved policy violations_, however the example [policy rules][ort-config-04c6b0d-rules-kts] contain an `-isExcluded()` in the `require` for most policy rules.
   An `-isExcluded()` in the `require` block means that a rule requires a package not to be excluded before it is executed. As all packages corresponding to the 375 unresolved policy violations have been marked as excluded by the scope exclude for `devDependencies` in the `ort.yml`, there are no more open policy violations left.

### Marking Files and Directories in a Project as Excluded

Besides scope excludes, you can also mark files and directories as excluded in the [.ort.yml][ort-yml] file using [path excludes][ort-yml-path-excludes]. At the moment you can not yet generate [path excludes][ort-yml-path-excludes] using `orthw` so you have to add them by hand.

If you look at [code for mime types version 2.1.26][mime-types-2.1.26] you will see it contains a directory named `test` which is not included in the release artifact [mime-types-2.1.26.tgz] so we can excluded it by adding a [path exclude][ort-yml-path-excludes] into the [.ort.yml][ort-yml] file:

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

- Symlink the `ort.yml` created by `orthw` to the `.ort.yml` in the project code repository so you can commit your changes easily and often
- Do not bother manually sorting path or scope excludes entries in the `ort.yml` file, simply add them and use `orthw rc-sort` to sort the file

### Example .ort.yml files

- [The .ort.yml of harp.gl][ort-yml-harp.gl], a 3D web map rendering engine written in TypeScript
- [The .ort.yml of MoveTK][ort-yml-movetk], a c++ library for computational movement analysis 
- [The .ort.yml of XYZ Hub][ort-yml-xyz-hub], a RESTful web service for the access and management of geospatial data written in Java

## Checking your Project Dependencies for Security Advisories <a name="orthw-check-advisories"></a>

ORT supports querying multiple security advisory providers to help you safely use open source software in your project.

The `~/.orthwconfig` file is preconfigured to use [OSV][osv] as the default advisory provider but you are free to add one or more other services such as [OSS Index][oss-index] or your local instance of [VulnerableCode][vulnerablecode].

Run the below command to check your project dependencies for known security vulnerabilities:

```bash
cd ~/ort-scans/mime-types-orthw
orthw check-advisories
```

[Generate the Web App report](#orthw-report-webapp) using `orthw report-webapp` and it should show several security vulnerabilities and increase in policy violations under _Summary_.

## Correcting Invalid or Missing Package Metadata <a name="orthw-curations"></a>

Using [curations][ort-curations] you can correct invalid or missing package metadata including the declared license and code repository information.

In the WebApp report look up `NPM::acorn:7.1.1` by filtering the _Package_ column under _Table_. You will find the declared license is MIT but the detected are Apache-2.0, BSD-2-Clause, BSD-3-Clause, LicenseRef-scancode-facebook-patent-rights-2 and MIT, so which licenses apply?

### Determining whether Right Sources where Scanned

Click the '+' sign on the left of `NPM::acorn:7.1.1` and expand the _Scan Results_ section which contains copyright and license findings. Look at copyright and license findings and you will find entries for the directories `acorn-loose` and `acorn-walk` containing `LICENSE` and `package.json` files. 
This is an indication of _overscanning_ - more than the actual sources of the package were scanned due to incorrect package metadata. In this case code repository seems to contain multiple packages so sources of multiple packages were scanned.

To confirm this assumption, do the following:

1. Navigate to the _Details_ section under `NPM::acorn:7.1.1`.
2. Download and extract [acorn-7.1.1.tgz].
3. Open the [acorn] repository in a web browser and find the code for version `7.1.1`. 
4. Compare [version 7.1.1 in the repository][acorn-7.1.1] with the extracted contents of [acorn-7.1.1.tgz].
5. You will find the contents of [acorn-7.1.1.tgz] come from the `acorn` directory within [acorn repository][acorn-7.1.1]. 

An alternative way to confirm [acorn repository][acorn-7.1.1] contains multiple npm packages is to simply search for the package names on [npmjs.com][npmjs]. Both the [acorn-loose][npm-acorn-loose] and [npm-acorn-walk][npm-acorn-walk] packages can be found on [npmjs.com][npmjs]. 

The cause of the _overscanning_ can be found in the [repository field of acorn's package.json][acorn-7.1.1-package-vcs] which is missing a [directory][npm-docs-repository] field to specify the directory in which the package lives:

```
"repository": {
    "type": "git",
    "url": "https://github.com/acornjs/acorn.git"
    "directory": "acorn" // Missing in actual acorn sources
},
```

One can not fix the sources of already released package artifacts so to resolve the missing _directory_ in the metadata of `NPM::acorn:7.1.1` you can use a [VCS path curation][ort-curations]:

1. Create or open using a text editor `curations/NPM/_/acorn.yml` in your local clone of the [ort-config] repository.
2. Add the below to the file, this instructs ORT that sources for any version of `NPM::acron` can be found in the `acorn` directory within the [acorn] code repository:

```
- id: "NPM::acorn"
  curations:
    comment: "Package resides in its own directory within repo."
    vcs:
      path: "acorn"
```

*Important*: Any time you add a [VCS curation][ort-curations] to [ort-config] you will need do a re-scan of your project. Once the re-scan has completed you should see a reduced number of detected licenses.

### Tips for Working with curations

- Fix incorrect package metadata upstream if the issue exists for latest version. Contributing back helps the community and you; once package maintainers are aware of the issue they might fix the same issue for all the packages they maintain.
- Contribute when possible curations you make to the [ort-config] repository so any [ORT][ort] user can benefit

## Marking Files or Directories in the Sources of a Dependency as not Included in Released Artifacts <a name="orthw-pc-excludes"></a>

Using [package configuration][ort-package-configurations] you can mark files and directories as not included in released artifacts - use it to make clear that license findings in documentation or tests in a package sources do not apply to the release (binary) artifact which is a dependency in your project.

[Generate the Web App report](#orthw-report-webapp) and look up `NPM::acorn-jsx:5.2.0` by filtering the _Package_ column under _Table_. You will find the declared license is MIT but the detected are BSD-2-Clause and MIT so which licenses apply?

### Determining what is Included in a Package

Click the '+' sign on the left of `NPM::acorn-jsx:5.2.0` and expand the _Scan Results_ section which contains copyright and license findings. Look at copyright and license findings and you will find a single BSD-2-Clause match in `test/tests-jsx.js`. It's likely that the `test` directory is not included in the release artifact of the package.

To confirm this assumption, do the following:
1. Navigate to the _Details_ section under `NPM::acorn-jsx:5.2.0`.
2. Download and extract [acorn-jsx-5.2.0.tgz].
3. Open the [acorn-jsx] repository in a web browser and find the code for version `5.2.0`. 
4. Compare [version 5.2.0 in the repository][acorn-jsx-5.2.0] with the extracted contents of [acorn-jsx-5.2.0.tgz].
5. You will find [acorn-jsx-5.2.0.tgz] does not contain anything from the `test` directory so one can conclude BSD-2-Clause does not apply to [acorn-jsx-5.2.0.tgz].

### Marking a Files or Directories for a Dependency as Excluded

You first thought might be to conclude the license for `NPM::acorn-jsx:5.2.0` as MIT. However, a better solution is to mark up the `test` directory as not included in the released artifact using [package configuration][ort-package-configurations] with a _path exclude_. Conclude only licenses if they were incorrectly identified e.g. a found BSD-3-Clause is actually a BSD-2-Clause.

1. Run the below command to generate a [package configuration][ort-package-configurations]:

```
orthw pc-create NPM::acorn-jsx:5.2.0
```

2. Upon completion, it should report the creation of `vcs.yml` in your local clone of the [ort-config] repository e.g. `[ort-config]/package-configurations/NPM/_/acorn-jsx/5.2.0/vcs.yml`
3. Open using a text editor the newly created `vcs.yml`, it should contain the following:

```
---
id: "NPM::acorn-jsx:5.2.0"
vcs:
  type: "Git"
  url: "https://github.com/acornjs/acorn-jsx.git"
  revision: "c30617bd8d3763ee96fc76abfc0a9bb00e036d68"
```

3. Add a `path_excludes` entry the `test` directory

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

## Correcting a Detected License found in Package Source Code <a name="orthw-pc-create"></a>

Using [package configuration][ort-package-configurations] you can overwrite scanner findings to correct identified licenses in a dependency for a specific file(s).

[Generate the Web App report](#orthw-report-webapp) and look up `NPM::eslint-scope:5.0.0` by filtering the _Package_ column under _Table_. You will find the detected licenses containing a NOASSERTION. 

All licenses in ORT follow the [SPDX][spdx] license specification and a NOASSERTION in detected licenses means the scanner detected something that looks like a license but was unable to determine which one.

How do we resolve the NOASSERTION to an actual license?

### Determining the Applicable License for a NOASSERTION

1. Click the '+' sign on the left of `NPM::eslint-scope:5.0.0` under _Table_ and expand the _Scan Results_ section which contains copyright and license findings. 
2. Filter the _Value_ column, selecting only the NOASSERTION and you will find out the scanner flagged line 54 in `README.md`.
3. Navigate to the _Details_ section under `NPM::eslint-scope:5.0.0`.
4. Open the [eslint-scope] repository in a web browser and find the code for version `5.0.0`. 
5. In [version 5.0.0 of the repository][eslint-scope-5.0.0] find the `README` file.
6. Using the [blame view][github-blame-view] in GitHub to located [line 54][eslint-scope-5.0.0-readme-54].
7. You will find the [line 54][eslint-scope-5.0.0-readme-54] states 'ESLint Scope is licensed under a permissive BSD 2-clause license.'.  The NOASSERTION likely triggered on the 'licensed under'.

### Correcting a NOASSERTION match

1. Run the below command to generate a [package configuration][ort-package-configurations]:

```
orthw pc-create NPM::eslint-scope:5.0.0
```

2. Upon completion, it should report the creation of `vcs.yml` in your local clone of the [ort-config] repository e.g. `[ort-config]/package-configurations/NPM/_/eslint-scope/5.0.0/vcs.yml`
3. Open using a text editor the newly created `vcs.yml`, it should contain the following:

```
---
id: "NPM::eslint-scope:5.0.0"
vcs:
  type: "Git"
  url: "https://github.com/eslint/eslint-scope.git"
  revision: "dbddf14d5771b21b5da704213e4508c660ca1c64"
```

3. Add a `license_finding_curations` entry for the NOASSERTION

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

4. When creating _license finding curations_ entries it's recommended to also create _path excludes_:

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

5. [Generate the Web App report](#orthw-report-webapp) using `orthw report-webapp`.
6. Open `~/ort-scans/mime-types-orthw/webapp.html` using a web browser.
6. The Web App report should now show for `NPM::eslint-scope:5.0.0`:
   - _Licenses_:
      - _Detected_: BSD-2-Clause
      - _Detected Excluded_: BSD-3-Clause, LicenseRef-scancode-public-domain, MIT
   - _Scan Results_:
      - A light grey icon in front the `Makefile.js` file and `test` directory rows 

## Listing the Licenses found in the Sources of a Package <a name="orthw-licenses"></a>

If you want to see matched texts for a detected license then use the `orthw licenses` command.
For example, to see the license matches for `NPM::mime-types:2.1.26`, run:

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

If you want to see licenses flagged for a policy violation then use the `offending-licenses` command.
For example, to see the flagged licenses  for `NPM::acorn:7.1.1`, run:

```
orthw offending-licenses NPM::acorn:7.1.1
```

## Conclude the License for a Package <a name="orthw-concluded-license-curation"></a>

Using [concluded license curation][ort-curations] you can set the concluded license for packages.

Before you set the concluded license of a package it's recommend to the below workflow:

### License Clearance Workflow

1. Ensure only the sources for package are scanned:
   - Use a _VCS URL_ curation to set the correct code repository location.
   - Use a _VCS path_ curation to set the directory within the code repository that contains the sources for a package.
2. Mark files and directories as not included in released artifacts:
   - Use a [package configuration][ort-package-configurations] with `path_excludes` to make clear that license findings in documentation, build scripts, or tests in a package sources do not apply to the release (binary) artifact which is a dependency in your project.
3. Correct license scanner findings:
    - Use a [package configuration][ort-package-configurations] with `license_finding_curation` to overwrite scanner findings to correct identified licenses for a specific file(s).
4.  Package includes license choices or a too large number of findings to be excluded or curated:
    - Use a [concluded license curation][ort-curations] to set the concluded license for a package.
    - Omit the version number within id of the curation if you are sure the concluded license applies
      to all versions of the package.

In the WebApp report look up `NPM::spdx-license-ids:3.0.5` by filtering the _Package_ column under _Table_. You will find hundreds of detected licenses. This is not surprising once you read the description of the package which states "a list of SPDX license identifiers".

One could use a [package configuration][ort-package-configurations] with hundreds concluded license `license_finding_curation` entries to set the applicable licenses for `NPM::spdx-license-ids:3.0.5`
Following the _License Clearance Workflow_ above the best solution here is to conclude the license for  `NPM::spdx-license-ids` as SPDX license list has and will always be licensed under CC-1.0.

1. Create or open using a text editor `curations/NPM/_/spdx-license-ids.yml` in your local clone of the [ort-config] repository.
2. Add the below to the file, this instructs ORT to conclude the license for any version of `NPM::spdx-license-ids`:

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
6. Open `~/ort-scans/mime-types-orthw/webapp.html` using a web browser.
7. The Web App report should now show less policy violations under _Summary_ and for `NPM::spdx-license-ids:3.0.5`:
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
