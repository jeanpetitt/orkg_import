import requests
import json
import os
from load_data import load_data_comparison


class _ORKG:

    def __init__(self):

        self.paper = {}
        self.contribution = {}
        self.comparison = {}

        self.api = "https://incubating.orkg.org/api"
        self.full_api = ""

    # getter
    def get_api(self):
        return self.api

    def get_contribution(self):
        return self.contribution

    def get_comparison(self):
        return self.comparison

    def get_paper(self):
        return self.paper

    # setter
    def set_api(self, api):
        self.api = api

    def get_specific_paper(self, paper_id):
        self.full_api = f"{self.api}/papers/{paper_id}"
        try:
            response = requests.get(self.full_api)
            if response.status_code == 200:
                self.paper = {
                    'status': 200,
                    'message': 'success',
                    'content': response.content
                }
            else:
                self.paper = {
                    'status': response.status_code,
                    'message': 'Failed',
                    'content': response.content
                }
            return self.paper
        except ValueError as e:
            return e

    def create_paper(self, token):
        headers = {
            "Content-Type": "application/vnd.orkg.paper.v2+json;charset=UTF-8",
            "Accept": "application/vnd.orkg.paper.v2+json",
            "Authorization": "Bearer" + token
        }

        data = {
            "title": "Nutritional of compositional food dish",
            "content": {},
            "observatories": ["R498126"],
            "research_fields": ["R12"]
        }

    def edit_paper(self, token, paper_id):
        headers = {
            "Content-Type": "application/vnd.orkg.paper.v2+json;charset=UTF-8",
            "Accept": "application/vnd.orkg.paper.v2+json",
            "Authorization": "Bearer" + token
        }
        paper = self.get_specific_paper(paper_id)
        # use json load to decote the byte binary response
        paper_json_decode = json.loads(paper['content'])

        authors = []
        for item in paper_json_decode['authors']:
            if item['identifiers'] == {}:
                item['identifiers'] = None
                authors.append(item)
            else:
                authors.append(item)
        data = {
            "authors": authors,
            "identifiers": paper_json_decode['identifiers'],
            "observatories": ["1afefdd0-5c09-4c9c-b718-2b35316b56f3"],
            "organizations": [],
            "publication_info": {
                "published_in": paper_json_decode['publication_info']['published_in']['label'],
                "published_month": paper_json_decode['publication_info']['published_month'],
                "published_year": paper_json_decode['publication_info']['published_year'],
                "url": paper_json_decode['publication_info']['url']
            },
            "research_fields":  [field['id'] for field in paper_json_decode['research_fields']],
            "title": paper_json_decode['title'],
        }
        json_data = json.dumps(data)
        print(json_data)
        self.full_api = f"{self.api}/papers/{paper_id}"
        try:
            response = requests.put(
                self.full_api, data=json_data, headers=headers)

            if response.status_code == 204:
                self.paper = {
                    "status": 204,
                    "message": "Success",
                    "content": response.headers['Location']
                }
                return self.paper
            else:
                self.paper = {
                    "status": 204,
                    "message": "Success",
                    "content": response.content
                }
                return self.paper
        except ValueError as e:
            return e

    def _load_data_contribution(self, data_json):
        contribution = []
        # contribution template
        data_template = {

            "literals": {
            },

            "contribution": {
                "label": "Contribution 1",
                "statements": {
                    "P107024": [{
                        "id": "#temp1",
                        # "statements": "null"
                    }],
                    "P107024": [{
                        "id": "#temp1"
                    }]
                }
            }
        }

        for item in data_json['table']:
            i = 1
            # add name food as a contribution
            contribution_label = item['contribution_label']
            data_template["contribution"]['label'] = contribution_label

            # add values to property
            for props in item['properties']:
                if isinstance(props['value'], float):
                    data_type = 'xsd:decimal'
                elif isinstance(props['value'], bool):
                    data_type = 'xsd:boolean'
                elif isinstance(props['value'], int):
                    data_type = 'xsd:integer'
                elif isinstance(props['value'], str):
                    data_type = 'xsd:string'
                data_template["literals"][f'#temp{i}'] = {
                    'label': props['value'],
                    'data_type': data_type
                }

                # add property to contribution
                data_template["contribution"]["statements"][f"{props['property_id']}"] = [{
                    "id": f"#temp{i}"
                }]
                i += 1
            # json serialize
            json_data = json.dumps(data_template)
            contribution.append(json_data)
            output_file = "data_contrib.json"
            with open(output_file, "w") as file:
                json.dump(data_template, file)

        return contribution

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

        contribution = []

        self.full_api = f"{self.api}/papers/{paper_id}/contributions"
        try:
            with open(json_template, 'r') as f:
                data_app = json.load(f)
                # get all data contribution in the loader of the data
                for data in self._load_data_contribution(data_json=data_app):
                    # make the post request in order to create  the contribution(s) of the paper
                    response = requests.post(
                        self.full_api, data=data, headers=headers)

                    if response.status_code == 201:
                        print({
                            'status': 201,
                            'message': "contribution created successfully",
                            'content': response.headers['Location']
                        })

                        contribution.append(
                            response.headers['Location'].split("/")[-1])
                    else:
                        print({
                            'status code': response.status_code,
                            'message': response.content
                        })
            return contribution
        except ValueError as e:
            print(e)

    """ 
        creation of the comparison
        1. create comparison with contributions 
        2. compare contribution
        3. create dataframe to display the comparison
    
    """

    def _laod_comparison_form(self, token, comparison_file, paper_id, template_contribution):
        contribution = self.create_contribution(
            paper_id=paper_id, token=token, json_template=template_contribution)

        print(contribution)
        with open(comparison_file, 'r') as f:
            comparison_input = json.load(f)
            data_template = {
                "title": comparison_input['title'],
                "description": comparison_input['description'],
                "research_fields": comparison_input['research_fields'],
                "authors": comparison_input['authors'],
                "references": [],
                "contributions": contribution,
                "observatories": comparison_input['observatories'],
                "organizations": comparison_input['organizations'],
                "is_anonymized": comparison_input['is_anonymized'],
                "extraction_method": comparison_input['extraction_method']

            }

        with open(comparison_file, 'w') as file:
            json.dump(data_template, file)

        data_template = json.dumps(data_template)
        return data_template

    def _create_comparison(self, token, comparison_file, paper_id, template_contribution):

        headers = {
            "Content-Type": "application/vnd.orkg.comparison.v2+json;charset=UTF-8",
            "Accept": "application/vnd.orkg.comparison.v2+json",
            "Authorization": "Bearer" + token
        }
        self.full_api = f'{self.api}/comparisons'
        try:
            # post the data
            response = requests.post(
                self.full_api, headers=headers, data=self._laod_comparison_form(
                    token=token, comparison_file=comparison_file,
                    paper_id=paper_id, template_contribution=template_contribution
                )
            )
            # check if comparison was created successfully
            if response.status_code == 201:
                return {
                    "status": 201,
                    "message": 'comparison created successfully',
                    # location url/ split.("/")[-1] in order to get id
                    "comparison_id": response.headers['Location'].split('/')[-1],
                    "content": response.headers['Location']
                }
            else:
                print({
                    "status": response.status_code,
                    "message": response.content
                })
        except ValueError as e:
            raise ValueError(e)

    def _compare_contribution(self, token, comparison_file, paper_id, template_contribution):
        """ 
            Comparison_input: it is file template that content data to post in order to create comparison like
            title, description, references, contributions.. etc
        """

        self.comparison = self._create_comparison(
            token=token, comparison_file=comparison_file,
            paper_id=paper_id,
            template_contribution=template_contribution
        )
        datas = ''
        with open(comparison_file, 'r') as f:

            datas = json.load(f)

        print(self.comparison)

        print("======= STEP 1: generate comparison")
        print("comparison_id generated: ", self.comparison['comparison_id'])
        print("Contributions: ", datas['contributions'])

        # data format when we use simcomp api got get contribution to compare
        data_format = {
            "thing_type": "COMPARISON",
            "thing_key": self.comparison['comparison_id'],
            "config": {
                "contributions": datas['contributions'],
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

            if len(datas['contributions']) >= 2:
                i = 0
                contrib = ""
                # format contribution to appropriate form corresponding in simcomp api
                for item in datas['contributions']:
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
                # dumps de json data
                json_data = json.dumps(data_format)

                # store the data in a file
                output_file = "test/data.json"
                with open(output_file, "w") as file:
                    json.dump(data_format, file)

                return json_data
            else:
                raise ValueError(
                    'Your must provide at least 2 contributions to compare')
        except:
            raise ValueError("error during the process")

    def _create_dataframe_comparison(self, token, comparison_folder_path, paper_id, template_contribution):
        list_file_comps = os.listdir(comparison_folder_path)
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            # "Authorization": "Bearer" + token
        }
        i = 1
        for file in list_file_comps:
            print("\n============== COMPARISON ", i, "===================")
            if file.endswith("json"):

                data = self._compare_contribution(
                    token=token, comparison_file=f"{comparison_folder_path}/{file}",
                    paper_id=paper_id, template_contribution=template_contribution
                )
                print(
                    "======= STEP 2: Compare Contribution ============")

                print(
                    "======= STEP 3: Create dataFrame ============")
                try:

                    self.full_api = "https://incubating.orkg.org/simcomp/thing/"
                    response = requests.post(
                        self.full_api, data=data, headers=headers)
                    if response.status_code == 201:
                        i += 1
                        print({
                            "status": 201,
                            "message": "Success",
                            "content": response.content
                        })

                    else:
                        print({
                            "status": response.status_code,
                            "content": response.content
                        })
                except ValueError as e:
                    return ValueError(e)

    def create_comparison(self, token, comparison_file_input):
        headers = {
            "Content-Type": "application/vnd.orkg.comparison.v2+json;charset=UTF-8",
            "Accept": "application/vnd.orkg.comparison.v2+json",
            "Authorization": "Bearer" + token
        }

        self.full_api = f'{self.api}/comparisons'
        data = load_data_comparison(comparison_file_input)

        try:
            # post the data
            response = requests.post(
                self.full_api, headers=headers, data=data)
            # check if comparison was created successfully
            if response.status_code == 201:
                return {
                    "status": 201,
                    "message": 'comparison created successfully',
                    # location url/ split.("/")[-1] in order to get id
                    "comparison_id": response.headers['Location'].split('/')[-1],
                    "content": response.headers['Location']
                }
            else:
                print({
                    "status": response.status_code,
                    "message": response.content
                })
        except ValueError as e:
            raise ValueError(e)

    def compare_contribution(self, token, comparison_file_input):
        """ 
            Comparison_input: it is file template that content data to post in order to create comparison like
            title, description, references, contributions.. etc
        """
        datas = ''
        with open(comparison_file_input, 'r') as f:

            datas = json.load(f)

        # call function that allows us to create a comparison using orkg api
        comparison = self.create_comparison(
            token=token, comparison_file_input=comparison_file_input)
        print("======= STEP 1: generate comparison")
        print("comparison_id generated: ", comparison['comparison_id'])
        print("Contributions: ", datas['contributions'])

        # data format when we use simcomp api got get contribution to compare
        data_format = {
            "thing_type": "COMPARISON",
            "thing_key": comparison['comparison_id'],
            "config": {
                "contributions": datas['contributions'],
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

            if len(datas['contributions']) >= 2:
                i = 0
                contrib = ""
                # format contribution to appropriate form corresponding in simcomp api
                for item in datas['contributions']:
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
                # dumps de json data
                json_data = json.dumps(data_format)

                # store the data in a file
                output_file = "test/data.json"
                with open(output_file, "w") as file:
                    json.dump(data_format, file)

                return json_data
            else:
                raise ValueError(
                    'Your must provide at least 2 contributions to compare')
        except:
            raise ValueError("error during the process")

    # ceate dataframe comparison in order to populate the comparison with contribution data
    def create_dataframe_comparison(self, token, comparison_folder_path):

        list_file_comps = os.listdir(comparison_folder_path)
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            # "Authorization": "Bearer" + token
        }
        i = 1
        for file in list_file_comps:
            print("\n============== COMPARISON ", i, "===================")
            if file.endswith("json"):

                data = self.compare_contribution(
                    token=token, comparison_file_input=f"{comparison_folder_path}/{file}")
                print(
                    "======= STEP 2: Compare Contribution ============")

                print(
                    "======= STEP 3: Create dataFrame ============")
                try:

                    self.full_api = "https://incubating.orkg.org/simcomp/thing/"
                    response = requests.post(
                        self.full_api, data=data, headers=headers)
                    if response.status_code == 201:
                        i += 1
                        print({
                            "status": 201,
                            "message": "Success",
                            "content": response.content
                        })

                    else:
                        print({
                            "status": response.status_code,
                            "content": response.content
                        })
                except ValueError as e:
                    return ValueError(e)
