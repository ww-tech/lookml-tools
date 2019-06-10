![](img/lookmltools.png)

# LookML Tools

This repository contains some tools to handle best practices of a set of developers working on LookML files.

There are three tools: 

 - `LookML updater`
 - `LookML linter`
 - `LookML grapher`

 Documentation site: https://ww-tech.github.io/lookml-tools/

## LookML updater
The first tool helps solve a problem of official definitions of `dimensions` and `measures`---such as in a business glossary---getting out of sync from some other system. The solution implemented here is to have a remote master list whose definitions are propagated to LookML. Thus, given some remote definition for a given LookML `dimension`, `dimension_group`, or `measure`, inject it in the LookML.

Full documentation is [here](README_UPDATER.md).


## LookML linter
The second tool helps us check that our LookML conforms to some given coding standards and LookML developer best practices. It runs a series of checks over our LookML files and reports which `files`, or which `dimensions`, `dimension_groups`, or `measures`, fail those checks.

Full documentation is [here](README_LINTER.md).

## LookML grapher
The third tool creates a "network diagram" of the `model - explore - view` relationships and writes to an `PNG` image file. The code will also identify any `orphans` i.e. views not referenced by any models or explores.

Full documentation is [here](README_GRAPHER.md).

## Installation

All three tools above makes use of Fabio's node-based LookML parser (https://github.com/fabio-looker/node-lookml-parser)

```
brew install node   # if on mac
npm install -g lookml-parser
```

You will need to set the path of the `lookml-parser` binary in the config file. For example, for the updater config, your path might be:

```
{
    "parser": "/usr/local/bin/lookml-parser",
    "tmp_file": "parsed_lookml.json",
    "definitions": {
        "type": "CsvDefinitionsProvider",
        "filename": "definitions.csv"
    }
}
```

### pip
You can install the Python codebase of `lookml-tools` via pip:

```
  pip install lookml-tools
```

You may need to install its dependencies:
```
  pip install -r requirements.txt
```

## Unit tests
There is a test suite with close to 100% code coverage

Run with 

```
pip install pytest-cov

python -m pytest --cov=lkmltools/ test/*.py ; coverage html
```

Importantly, as this code relies on an external node utility (`lookml-parser`), one that might not be installed, and one that could be installed but whose behavior might change compared to today,

 - the unit tests are set to check that it is installed (`test/test_prequisites.py`)
 - the unit tests use a cached and checked in parsed lookml file (`test/parsed_minimal_multiline_lookml.json`) and check that parsing the same input file produces the same output as that cached version (see `test/test_lookml_modifier`.`test_get_json_representation`).

 This should provide confidence that this core-functionality parser is working as expected.

## Developer Notes
There are some developer notes for the linter [here](README_DEVELOPER.md).

## Contribute
We would love to have your feedback, suggestions, and especially contributions to the project. Create a pull request!

You can reach me directly at carl.anderson@weightwatchers.com as well as @leapingllamas on Twitter.

## License
Copyright 2019 WW International, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.