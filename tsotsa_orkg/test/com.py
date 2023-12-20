import requests
import json


def compare_contribution(contributions, comparison_id):
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
    url = "https://incubating.orkg.org/simcomp/contribution/compare?"
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
            url = f"{url}{contrib}&type=PATH"
            #  get contribution to comapare
            response = requests.get(url, headers=headers)
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


# data = compare_contribution(data_format)


def populate_comparison(comparison_id, contributions):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    try:
        url = "https://incubating.orkg.org/simcomp/thing/"
        response = requests.post(
            url, data=compare_contribution(contributions, comparison_id), headers=headers)
        print(response.content)
    except ValueError as e:
        raise ValueError(e)


populate_comparison("R937639", ["R903146",
                                "R903147"])
