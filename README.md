# SLCSP
This project solves the slcsp problem for a given data set, finding the second lowest cost silver plan for each zipcode provided.
The output of running this package is to standard out. 

## Installation
This project is written in `python 3`, specifically `python 3.9.6`.  
It does not require installation of dependencies or creation of virtual environment.
To install just clone this repo:
```bash
 git clone https://github.com/rbogle/slcsp.git
```

## Usage
The package can be run as a script from the root of the local clone of this repository doing the following:

```bash
python3 slcsp
```

This will attempt to find the default data files in the local `./data` directory.  
Options exist to point to other locations for the data files:
```bash
python3 slcsp --help

usage: slcsp [-h] [--plans PLANS] [--areas AREAS] [--zips ZIPS]

Find the second lowest cost sliver plan for a provide list of zipcode

optional arguments:
  -h, --help            show this help message and exit
  --plans PLANS, -p PLANS
                        path to file containing rate plans
  --areas AREAS, -a AREAS
                        path to file mapping zipcodes to rate areas
  --zips ZIPS, -z ZIPS  
                        path to file with zipcode to search for slcsp

```



## Contributing
This project uses a few helpers to aid in dev dependency install, testing, formatting

### Install dev dependencies 
Use the [Taskfile]https://github.com/adriancooney/Taskfile) to install deps

```bash
./Taskfile install-dev
```
This will setup dependencies for formatiing and testing

## Testing
You can run the unit tests for the package with `pytest`
```bash
pytest .
```

## Style and Formatting
Both `black` and `flake8` are installed to enable style and formmating checks:

```bash
./Taskfile format
```
or they can be run independently:

```bash
black .
```

```bash
flake8 .
```
