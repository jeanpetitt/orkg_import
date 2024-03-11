# Use the base Python image
FROM python:3.9-slim
# RUN apt-get update  && apt-get install -y git python3-virtualenv wget 
WORKDIR /workspace

# installation of dependancies
COPY . /workspace
RUN pip install -r tsotsa_orkg/requirements.txt

# Define environments variable for CMD parameters
# ENV PLATFORM="incubating"
# ENV PAPER_ID="R1198107"
# ENV JSON_PATH_CONTRIBUTION="data/contributions/spec_json_template.json"
# ENV COMPARISON_FOLDER_PATH="data/comparisons"

CMD ["python", "tsotsa_orkg/main.py", \
    "--platform","incubating", \
    "--paper_id","R1198107", \
    "--json_path_contribution", "tsotsa_orkg/data/contributions/spec_json_template.json", \
    "--comparison_folder_path","tsotsa_orkg/data/comparisons"\
    ]