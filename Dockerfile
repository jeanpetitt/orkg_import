# Use the base Python image
FROM python:3.9-slim
# RUN apt-get update  && apt-get install -y git python3-virtualenv wget 
WORKDIR /workspace

# installation of dependancies
COPY . /workspace
RUN pip install -r tsotsa_orkg/requirements.txt

CMD ["python", "tsotsa_orkg/main.py"]