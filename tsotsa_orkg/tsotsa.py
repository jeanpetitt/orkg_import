import requests
import json
from load_data import load_data_contribution, prop_ids, load_data_comparison


class _ORKG:

    def __init__(self):

        self.paper = {}
        self.contribution = {}
        self.ressource = {}
        self.predicate = {}
        self.comparison = {}

        self.api = "https://sandbox.orkg.org/api"  # orkg incubation api
        # self.api = "https://orkg.org/api"
        self.full_api = ""

    # fetch a specific contribution
    def get_contribution(self, contribution_id):
        """ 
            structure of a contribution in json format
        """
        self.full_api = f"{self.api}/contributions/{contribution_id}"
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
    def create_contribution(self, paper_id, token, json_template):
        """ 
            token: use to identify the users who make an write operation in orkg
            json_template: content the data to make a contribution
            paper_id: the id of paper which will contain the contribution added
        """
        headers = {
            "Content-Type": "application/vnd.orkg.contribution.v2+json;charset=UTF-8",
            "Accept": "application/vnd.orkg.contribution.v2+json",
            "Authorization": "Bearer" + token
        }

        self.full_api = f"{self.api}/papers/{paper_id}/contributions"
        try:
            with open(json_template, 'r') as f:
                data_app = json.load(f)
                # get all data contribution in the loader of the data
                for data in load_data_contribution(data_json=data_app, property_ids=prop_ids):
                    # make the post request in order to create  the contribution(s) of the paper
                    response = requests.post(
                        self.full_api, data=data, headers=headers)

                    if response.status_code == 201:
                        print({
                            'status': 201,
                            'message': "contribution created successfully",
                            'content': response.content
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

    def create_comparison(self, token, comparison_input):
        headers = {
            "Content-Type": "application/vnd.orkg.comparison.v2+json;charset=UTF-8",
            "Accept": "application/vnd.orkg.comparison.v2+json",
            "Authorization": "Bearer" + token
        }
        self.full_api = f'{self.api}/comparisons'

        try:
            # post the data
            response = requests.post(
                self.full_api, headers=headers, data=load_data_comparison(comparison_input))
            # check if comparison was created successfully
            if response.status_code == 201:
                return {
                    "status": 201,
                    "message": 'comparison created successfully',
                    "content": response.headers
                }
            else:
                return {
                    "status": response.status_code,
                    "message": response.content
                }
        except ValueError as e:
            raise ValueError(e)

    def compare_contribution(self, contributions, comparison_id):
        # def compare_contribution(self, token, comparison_input):
        """ 
            Comparison_input: it is file template that content data to post in order to create comparison like
            title, description, references, contributions.. etc
        """

        # call function that allows us to create a comparison using orkg api
        # comparison = self.create_comparison(
        #     token=token, comparison_input=comparison_input)

        # data format when we use simcomp api got get contribution to compare
        data_format = {
            "thing_type": "COMPARISON",
            "thing_key": "",
            "config": {
                "contributions": [
                    "R837784",
                    "R837785"
                ],
                "predicates": [],
                "type": "PATH",
                "transpose": False
            },
            "data": {
            }
        }

        headers = {
            'Content-Type': 'application/json'
        }
        self.full_api = "https://incubating.orkg.org/simcomp/contribution/compare?"
        try:

            if len(contributions) >= 2:
                i = 0
                contrib = ""
                # format contribution to appropriate form corresponding in simcomp api
                for item in contributions:
                    if i == 0:
                        contrib += f"contributions={item}"
                        i += 1
                    else:
                        contrib += f"&contributions={item}"
                        i += 1
                self.full_api = f"{self.full_api}{contrib}&type=PATH"
                #  get contribution to comapare
                response = requests.get(self.full_api, headers=headers)
                # use json load to decote the byte binary response
                response_decoded = json.loads(response.content)
                # set data
                data_format["data"]['contributions'] = response_decoded['payload']['comparison']['contributions']
                data_format['data']['predicates'] = response_decoded['payload']['comparison']['predicates']
                data_format['data']['data'] = response_decoded['payload']['comparison']['data']
                data_format['thing_key'] = comparison_id
                # dumps de json data
                json_data = json.dumps(data_format)

                # store the data in a file
                output_file = "data.json"
                with open(output_file, "w") as file:
                    json.dump(data_format, file)

                print(data_format)
                return json_data
            else:
                raise ValueError(
                    'Your must provide at least 2 contributions to compare')
        except:
            raise ValueError("error during the process")

    # ceate dataframe comparison in order to populate the comparison with contribution data
    def create_dataframe_comparison(self, data, comparison_id):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        url = "https://incubating.orkg.org/simcomp/thing/"
        response = requests.post(
            url, data=self.compare_contribution(data, comparison_id), headers=headers)
        print(response.content)
