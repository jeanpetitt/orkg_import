# Running Step

## Environment variable

To write in ORKG system you should be login and to do it follow these steps:

- navigate in the tsosa_orkg folder

- Create a .env file
- At the end paste these line inside 
```bash
TOKEN="Your_ORKG_Token"
PLATFORM="incubating"
TABLE_JSON_FOLDER_PATH="data/tables_json/test"
```
    

### Environment variables role

* TOKEN : Allow to perform some task in orkg system
* PLATFORM : Specify which platform you want to use (incubation, sandbox and orkg)
* TABLE_JSON_FOLDER_PATH : It is path of directory that contains the json table format. See an example of json table here [json table example](./data/tables_json/test/spec_json_template.json)


### Docker image
The  Docker image is created and started with:

```bash
docker build -f ./Dockerfile -t tsotsa_orkg .
```

```bash
docker run --rm -ti tsotsa_orkg
```
