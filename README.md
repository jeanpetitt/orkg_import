# ORKG Importation

This package aims to make the automatic import of comparison, contribution more easy in ORKG system

## Dependancies

Before running the project in local rest assured that you have python version >= 3.8 install on your device. if it is not the case go on [python donwload](https://www.python.org)

## Clone the project in your local device

```bash
git clone https://github.com/jeanpetitt/orkg_import
```

## Perform Contribution and Comparison tasks

To run the project in local on your computer device, you have 02 options:

### Use Docker to perform different tasks like create comparison, contribution...


Navigate inside of the [Dockerfile Readme](/README_Docker.md) For more information

### Use python script

You can perform the same tasks above by using the python script. But before it let prepare the necessary:

#### Create an .env file an copy these lines inside 
```bash
TOKEN="Your_ORKG_Token"
PLATFORM="incubating"
TABLE_JSON_FOLDER_PATH="data/tables_json/test"
```
#### Launch python script

```bash
python main.py 
```

### Use python package setup

see more detail in [setup tsotsa_orkg](./README_SETUP.md)

## Authors

* *Fidel Jiomekong*
  
* *Jean Petit BIKIM*
  