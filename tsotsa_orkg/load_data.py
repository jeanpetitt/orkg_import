import json


def load_data_contribution(data_json, property_ids):
    list_contribution = []
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

    for item in data_json['visualisation']:
        i = 1
        # add name food as a contribution
        contribution_label = item['nameFood']
        data_template["contribution"]['label'] = contribution_label

        # add values to property
        for props in item['components']:
            data_template["literals"][f'#temp{i}'] = {
                'label': props['valueComponent'],
                'data_type': 'xsd:decimal'
            }

            # add property to contribution (i-1 because the first elements of the list have 0 as index)
            data_template["contribution"]["statements"][f"{property_ids[i-1]}"] = [{
                "id": f"#temp{i}"
            }]
            i += 1
        # json serialize
        json_data = json.dumps(data_template)
        list_contribution.append(json_data)
        output_file = "data_contrib.json"
        with open(output_file, "w") as file:
            json.dump(data_template, file)

    return list_contribution


def load_data_comparison(comparison_file):
    with open(comparison_file, 'r') as f:
        comparison_input = json.load(f)
        data_template = {
            "title": comparison_input['title'],
            "description": comparison_input['description'],
            "research_fields": comparison_input['research_fields'],
            "authors": comparison_input['authors'],
            "references": [],
            "contributions": comparison_input['contributions'] if comparison_input['contributions'] and
            len(comparison_input['contributions']) >= 2
            else print("You should provide at least 2 contributions to compare "),
            "observatories": comparison_input['observatories'],
            "organizations": comparison_input['organizations'],
            "is_anonymized": comparison_input['is_anonymized'],
            "extraction_method": comparison_input['extraction_method']

        }
        data_template = json.dumps(data_template)

    return data_template


prop_ids = [
    "P107024", "P107024", "P107025", "P107026", "P107027", "P107028", "P107029",
    "P107030", "P107031", "P107032", "P107033", "P107034", "P107035", "P107036",
    "P107037", "P107038", "P107039", "P107040", "P107041", "P107042", "P107043",
    "P107044", "P107045", "P107046", "P107047", "P107048", "P107049", "P107050",
    "P107051", "P107052",

]

# print(load_data_contribution(data_json=data_app, property_ids=prop_ids))
