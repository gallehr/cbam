import json
from datetime import datetime

# Testing adding Reporting Declarant to Roles of Build (had only System Manager) and Wesite (had no roles). If it works, also adding the path to the list for Integrations, Tools and so on.
# apps/frappe/frappe/automation/workspace/tools/tools.json
# ...
@frappe.whitelist()
def add_reporting_declarant_role():
    workspace_path = ['apps/frappe/frappe/website/workspace/website/website.json', 'apps/frappe/frappe/core/workspace/build/build.json']
    for file in workspace_path:
        with open(file, 'r') as file:
            data = json.load(file)

        if 'roles' not in data:
            data['roles'] = []

        new_role = {"role": "Reporting Declarant"}
        data['roles'].append(new_role)

        data['modified'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

        with open(file, 'w') as file:
            json.dump(data, file, indent=4)
