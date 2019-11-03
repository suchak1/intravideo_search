# ***IntraVideo*** **Search**
[![Build Status](https://travis-ci.org/suchak1/intravideo_search.png?branch=master)](https://travis-ci.org/suchak1/intravideo_search)
[![Linux](https://img.shields.io/badge/os-Linux-1f425f.svg)](https://ubuntu.com/download/desktop)
[![Python 3.7](https://img.shields.io/badge/python-3.7-red.svg)](https://www.python.org/downloads/release/python-370/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.md)
[![version](https://img.shields.io/github/v/tag/suchak1/intravideo_search)](https://github.com/suchak1/intravideo_search/tags)
#### a project for CMSC 22001 -- Software Construction
***
*IntraVideo Search* is a search engine that takes a video source and search terms as inputs and produces short video clips as outputs. Using ML image classification APIs, we can search through a video and retrieve only the parts relevant to the user-specified search terms.

## Getting Started

### Prerequisites

<!---Obtain a free API key.--->

### Installation

To install the necessary packages, simply run:
```
pip install -r requirements.txt
```

### New Packages

To remake the `requirements.txt` file, run:
```
pipreqs ./ --force
```

### Testing

To run all tests, run:
```
pytest
```

To make new tests, follow the template in `test/test_hello_world.py`.

## Deployment


## Result

## Files

```docs/``` - markdown files for software dev

```pics/``` - any screenshots used in markdown files

```src/``` - source code for the project

- ```model.py``` - main driver


- ```view.py``` - GUI

- ```controller.py``` - workhorse

```utils/``` - various scripts to help in dev work

- ```update.py``` - updates all packages that `pip` considers "outdated"

```.travis.yml``` - build pipeline



## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md)
 file for details.

***

[![Made with Python](https://forthebadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

<!---
<<[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)>>
--->
