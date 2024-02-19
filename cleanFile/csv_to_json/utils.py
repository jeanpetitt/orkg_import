import os
import csv


def csv_to_json(csv_path_dir):

    list_files = os.listdir(csv_path_dir)

    for file in list_files:
        # open csv file
        with open(f'{csv_path_dir}/{file}', 'r') as csv_file:
            json_template = {
                'name': '',
                'paper': '',
                'table': []
            }
            nameFood = []
            numberRecipes = []
            components = []
            unit = []
            nameComponent = []
            valueComponent = []
            reader = csv.reader(csv_file, delimiter=',')
            i = 0
            for line in reader:
                if i == 0:
                    json_template['name'] = file.split('.')[0]
                    json_template['paper'] = line[1]
                    i += 1
                elif i == 1:
                    for food in line[1:len(line) - 1]:
                        nameFood.append(food)
                        # json_template['visualization'].append({
                        #     'nameFood': visual['nameFood'],
                        # })
                    i += 1
                else:
                    if line[0].upper == 'Number of recipescollected'.upper:
                        for recipes_n in line[1:len(line) - 1]:
                            numberRecipes.append(recipes_n)
                    else:
                        nameComponent.append(line[0])
                        valueComponent.append(line[1:len(line) - 1])
                        unit.append(line[len(line) - 1])

            print(json_template)


csv_to_json()
