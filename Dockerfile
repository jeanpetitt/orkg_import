# Use the base Python image
FROM python:3.9-slim
# RUN apt-get update  && apt-get install -y git python3-virtualenv wget

WORKDIR /workspace

# installation of dependancies
COPY /tsotsa_orkg /workspace
RUN pip install -r requirements.txt


# RUN pip install -r tsotsa/requirements.txt

CMD ["python", "main.py", "--api", "incubating", \
    "--contribution_and_comparison", "true", "--paper_id", "R1198088", \
    "--json_path_contribution", "data/contributions/spec_json_template.json", \
    "--comparison_folder_path", "data/comparisons"]
