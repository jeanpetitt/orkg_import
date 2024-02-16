# Running Step

## TOKEN

To write in ORKG system you should be login and to do it follow these steps:

- Create a .env file
- At the end paste this line inside TOKEN="Your_ORKG_Token"

## Contributions &&  Comparison

### Navigate in the dockerfile folder

```bash
cd tsotsa_orkg
```

### Arguments

- --comparison: Specify that you want to perform comparsion tasks. It is boolean arguments
  
- --contribution: Specify that you want to perform contribtuion tasks. It is boolean arguments
  
- --api: specify which api you want to use
        - incubating
        - sandbox
        - orkg
  
- --paper_id: specify the paper where you want to add contribution(s)
  
- --json_path_contribution: Json template which help to create a contribution. see an example here [json template example](./tsotsa_orkg/data/contributions/full_json_template.json)

- --comparison_folder_path: Folder that contain json form that help to create a comparison. see an example here [folder comparison form](./tsotsa_orkg/data/comparisons/)

To update the differents arguments you want to use navigate inside [Dockerfile comparison](./Dockerfile.comparison) or [Dockerfile contribution](./Dockerfile.contribution)

### Docker image

The contribution Docker is created and started with:

```sh
docker build -f ./Dockerfile.contribution -t tsotsa_contribution .
```

```sh
docker run --rm -ti tsotsa_contribution
```

The comparison Docker is created and started with:

```sh
    docker build -f ./Dockerfile.comparison -t tsotsa_comparison .
```

```sh
    docker run --rm -ti tsotsa_comparison
```
