import requests
import json
from data import load_data_json_contribution, data_app, prop_ids


class TSOTSA_ORKG:

    def __init__(self):

        self.paper = {}
        self.contribution = {}
        self.ressource = {}
        self.predicate = {}
        self.comparison = {}

        self.api = "https://incubating.orkg.org/api/"  # orkg incubation api
        # self.api = "https://orkg.org/api"
        self.full_api = ""

    # fetch a specific contribution
    def get_contribution(self, contribution_id):
        """ 
            structure of a contribution in json format
        """
        api_contrib = "contributions/"
        self.full_api = self.api + api_contrib + f"{contribution_id}"
        try:
            response = requests.get(self.full_api)

            self.contribution = {
                'status': 200,
                'message': 'success',
                'content': response.content
            }

            # print(self.contribution)

            return self.contribution
        except ValueError as e:
            print(str(e))

    # fetch all contribution

    def get_list_contribution(self, list_contribution_ids=None):
        """ 
            structure of the contributions in json format

        """
        lis_contrib = []
        # get list contributions by enter their ids
        if list_contribution_ids is not None:
            for ids in list_contribution_ids:
                self.full_api = f"{self.api}/contributions/{ids}"

                try:
                    response = requests.get(self.full_api)

                    self.contribution = response.content
                    lis_contrib.append(self.contribution)

                except ValueError as e:
                    print(str(e))
            self.contribution = {
                'status': 200,
                'message': 'success',
                'content': lis_contrib
            }
        # it a list ids is not given, fecth all contribution
        else:
            self.full_api = f"{self.api}/contributions"
            try:
                response = requests.get(self.full_api)
                self.contribution = {
                    'status': 200,
                    'message': 'success',
                    'content': response.content
                }
            except ValueError as e:
                print(e)
        return self.contribution

    # create contribution
    def create_contribution(self, paper_id):
        headers = {
            "Content-Type": "application/vnd.orkg.contribution.v2+json;charset=UTF-8",
            "Accept": "application/vnd.orkg.contribution.v2+json",
            "Authorization": "Bearer" + "og_fcMz__PH-rGZCWJ7FQo0vMBE"
        }

        self.full_api = f"{self.api}/papers/{paper_id}/contributions"
        try:
            for data in load_data_json_contribution(data_json=data_app, property_ids=prop_ids):
                response = requests.post(
                    self.full_api, data=data, headers=headers)

                if response.status_code == 204:
                    print({
                        'status': 201,
                        'message': "contribution created successfully"
                    })
                else:
                    print({
                        'status': response.status_code,
                        'message': response.content
                    })
        except ValueError as e:
            print(e)

    # fetch a specific contribution

    def get_comparison(self, contribution_id):
        """ 
            structure of a contribution in json format

        """
        return self.comparison

    # fetch all contribution

    def get_list_comparison(self):
        """ 
            structure of the contributions in json format

        """
        return self.comparison

    """ 
        creation of the comparison
        1. create comparison with contributions 
        2. compare contribution
        3. create dataframe to display the comparison
    
    """
    #

    def create_comparison(self, title, description, contributions, research_field_id=None):
        headers = {
            "Content-Type": "application/vnd.orkg.contribution.v2+json;charset=UTF-8",
            "Accept": "application/vnd.orkg.contribution.v2+json",
            "Authorization": ""
        }
        self.full_api = f'{self.api}/comparisons'

        try:
            data_template = {
                "title": title if title else print("Title is required"),
                "description": description if description else print("description is required"),
                "research_fields": [research_field_id] if research_field_id else [],
                "authors": [{
                    "id": None,
                    "name": "Jean petit",
                    "identifiers": None,
                    "homepage": None
                }],
                "references": [],
                "contributions": contributions if contributions and len(contributions) >= 2 else print("You should at least give 2 contribution "),
                "observatories": [],
                "organizations": [],
                "is_anonymized": False,
                "extraction_method": "UNKNOWN"

            }
            json_data = json.dumps(data_template)

            print(json_data)

            response = requests.post(
                self.full_api, headers=headers, data=json_data)
            print(response.content)
        except ValueError as e:
            raise ValueError(e)

    def compare_contribution(self, data, comparison_id):

        headers = {
            'Content-Type': 'application/json'
        }
        self.full_api = "https://incubating.orkg.org/simcomp/contribution/compare?contributions=R837784&contributions=R837785&type=PATH"

        response = requests.get(self.full_api, headers=headers)
        response_decoded = json.loads(response.content)

        data["data"]['contributions'] = response_decoded['payload']['comparison']['contributions']
        data['data']['predicates'] = response_decoded['payload']['comparison']['predicates']
        data['data']['data'] = response_decoded['payload']['comparison']['data']
        data['thing_key'] = comparison_id

        json_data = json.dumps(data)

        output_file = "data.json"
        with open(output_file, "w") as file:
            json.dump(data, file)
        print(data)
        return json_data

    def create_dataframe_comparison(self, data, comparison_id):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        url = "https://incubating.orkg.org/simcomp/thing/"
        response = requests.post(
            url, data=self.compare_contribution(data, comparison_id), headers=headers)
        print(response.content)
