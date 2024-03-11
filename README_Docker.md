# Running Step

## TOKEN

To write in ORKG system you should be login and to do it follow these steps:

- navigate in the tsosa_orkg folder
  
```bash
  cd tsotsa_orkg
```

- Create a .env file
- At the end paste this line inside TOKEN="Your_ORKG_Token"

## Contributions &&  Comparison

### Arguments role

Navigate in the dockerfile File to update the following arguments:

- --comparison: Specify that you want to perform comparsion tasks. It is boolean arguments
- --contribution_and_camparison : Specify that you want to import directly the table in one step. boolean argument
- --contribution: Specify that you want to perform contribtuion tasks. It is boolean arguments
  
- --platform: specify which api you want to use
  - incubating: it is set by default
  - sandbox
  - orkg
  
- --paper_id: specify the paper where you want to add contribution(s)
  
- --json_path_contribution: Json template which help to create a contribution. see an example here [json template example](./tsotsa_orkg/data/contributions/full_json_template.json)

- --comparison_folder_path: Folder that contain json form that help to create a comparison. see an example here [folder comparison form](./tsotsa_orkg/data/comparisons/)

To update the differents arguments you want to use navigate inside [Dockerfile](./Dockerfile.comparison)

### Docker image

The  Docker image is created and started with:

```sh
docker build -f ./Dockerfile -t tsotsa_orkg .
```

```sh
docker run --rm -ti tsotsa_orkg
```
