import looker_sdk
from looker_sdk import models40
import json
import pandas as pd

sdk = looker_sdk.init40(config_file = '../looker.ini', section = 'Looker')

my_user = sdk.me()
first_name = my_user['first_name']
name_split = '-'.join(first_name.upper())
print(f"My bologna has a first name. It's {name_split}.")

# for project in sdk.all_projects():
#     print(project['name'])

# for file in sdk.all_project_files(project_id = "square_risk"):
#     file_name = file['title']
#     file_type = file['type']
#     print(f"{file_name}: {file_type}")

explores = sdk.lookml_model('Risk_Ops')['explores']
explore_dict = dict({})

for explore in explores:
    ex = sdk.lookml_model_explore('Risk_Ops', explore['name'])
    views = []
    views.append(ex['view_name'])
    for join in ex['joins']:
        views.append(join['name'])
    explore_dict[explore['name']] = views
        
for k in explore_dict.keys():
    print(f"{k}: {explore_dict[k]}")
    print("\n")