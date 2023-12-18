import requests
import sys
from editdistance import eval


if __name__ == "__main__":
    resources = sys.argv[1:]
    print("ressoures orkg", resources)

    output = []
    for resource in resources:
        response = requests.get(
            f'https://orkg.org/api/resources/?q={resource}')
        result = response.json()['content']
        best_result = sorted(result, key=lambda r: eval(resource, r['label']))[
            0] if len(result) > 0 else []

        if best_result:
            output.append(
                f" - Input : {resource} \n\t-> id = {best_result['id']}, label = {best_result['label']}, link = https://orkg.org/resource/{best_result['id']}")
        else:
            output.append(f" - Input : {resource} \n\t-> ----Not Found----")

    for line in output:
        print(f"{line}")
