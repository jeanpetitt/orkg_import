# ORKG Importation

This package aims to make the automatic import of comparison, contribution and paper more easy in ORKG system

## Dependancies

Before running the project in local rest assured that you have python version >= 3.8 install on your device. if it is not the case go on [python donwload](https://www.python.org)

## Contribution

contribution

## Comparison

comparison

## Perform Contribution and Comparison tasks

To run the project in local on your computer device, you have Three options:

### Use Docker to perform different tasks like create comparison, contribution and paper

Actually we have two (02) dockerfiles to perfom contribution and comparison tasks.
For more detail on how you can use docker to perform these tasks, navigate inside [README Docker](./tsotsa_orkg/README.md) and Follow the differents steps.

### Use python script

You can perform the same tasks above by using the python script. But before it let prepare the necessary:

* Create an .env file an copy this line inside TOKEN="your orkg token"

* #### Arguments

  * --comparison: Specify that you want to perform comparsion tasks. It is boolean arguments
  
  * --contribution: Specify that you want to perform contribtuion tasks. It is boolean arguments
  
  * --api: specify which api you want to use
  
        - incubating
        - sandbox
        - orkg
  
  * --paper_id: specify the paper where you want to add contribution(s)
  
  * --json_path_contribution: Json template which help to create a contribution. see an example here [json template example](./tsotsa_orkg/data/contributions/full_json_template.json)

  * --comparison_folder_path: Folder that contain json form that help to create a comparison. see an example here [folder comparison form](./tsotsa_orkg/data/comparisons/)
  
* #### Create contribution with python script using arguments

    ```bash
    python main.py --api incubating --contribution true --paper_id R903121 --json_path_contribution data/contributions/spec_json_template.json
    ```

* #### Create Comparison with python script using arguments

    ```bash
    python main.py --api incubating --comparison true --comparison_folder_path data/comparisons
    ```

### Use python package setup

see more detail in [setup tsotsa_orkg](./README_SETUP.md)

## Authors

* *Fidel Jiomekong*
  
* *Jean Petit BIKIM*
  