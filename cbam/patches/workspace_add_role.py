import frappe
import json
from datetime import datetime

# Not completely tested yet
@frappe.whitelist()
def execute():
    workspace_paths = [
        '/workspace/frappe-bench/apps/frappe/frappe/website/workspace/website/website.json',
        '/workspace/frappe-bench/apps/frappe/frappe/core/workspace/build/build.json',
        '/workspace/frappe-bench/apps/frappe/frappe/automation/workspace/tools/tools.json',
        '/workspace/frappe-bench/apps/frappe/frappe/integrations/workspace/integrations/integrations.json'
    ]
    for path in workspace_paths:
        with open(path, 'r') as file:
            data = json.load(file)

        if 'roles' not in data:
            data['roles'] = []

        if {"role": "System Manager"} not in data['roles']:
            new_role = {"role": "System Manager"}
            data['roles'].append(new_role)
            data['modified'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

        with open(path, 'w') as file:
            json.dump(data, file, indent=4)
