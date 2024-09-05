# motostat-to-spritmonitor

A project for converting csv files from https://www.motostat.pl to csv files in a format compatible with https://www.spritmonitor.de

## Prerequisite

- UNIX/Linux
- Python3.11
- virtualenv module
- pip module
- git

## Installation

- mkdir -p ~/bin
- git clone https://github.com/Szumak75/motostat-to-spritmonitor.git
- ln -s \`pwd`/motostat-to-spritmonitor/bin/motostat-to-spritmonitor ~/bin
- cd motostat-to-spritmonitor
- python3 -mvenv .venv
- source .venv/bin/activate
- pip install -r requirements.txt
- cd

## Usage

$ cat motostat82522.csv|motostat-to-spritmonitor

In the above example, the file `motostat82522.csv` contains the export of refueling and expenses.

In this case, with the default start options, `motostat-to-spritmonitor` will create two csv files in the /tmp directory:

- `spritmonitor_costs.csv`
- `spritmonitor_fuels.csv`

These files can be imported without further changes in the vehicle profile on the `spritmonitor.de` website.

In the case of vehicles with mileage counted in miles, the `-m` switch should be used when converting csv files.

Motostat.pl always saves mileage in km and converts it for presentation purposes on the website. Spritmonitor saves mileage data without conversion - in the form in which it is entered.

Using the `-m` flag correctly converts mileage from km to miles in the generated files.

The `-o` flag allows you to change the default target directory from `/tmp` to a user-specified one.