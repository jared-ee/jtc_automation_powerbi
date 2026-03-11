import json
import requests
import csv

from actions.create.create_apis import get_policies_url, get_policies_headers, add_user_security_url, add_user_security_headers, get_roles_url, get_roles_headers
from actions.cookies_utils import get_api_cookies
from actions.create.add_users_row_level_security import get_dashboard_id 

from data.data import SECURITY_DATA

def get_policies(powerbi_id):
    print("Getting Policies")

    get_policies_url_refined = get_policies_url.replace('<powerbi_id>', powerbi_id)
    get_policies_headers['Cookie'] = get_api_cookies()

    response = requests.get(
        get_policies_url_refined,
        headers=get_policies_headers
    )

    print(response)
    if response.status_code == 200:
        print("Policies obtained")
        print('--------------')
        return response.json()
    else:
        print("Failed to obtain Policies")
        print('--------------')
        return response
    
def get_roles(powerbi_id):
    print("Getting Roles")

    get_roles_url_refined = get_roles_url.replace('<powerbi_id>', powerbi_id)
    get_roles_headers['Cookie'] = get_api_cookies()

    response = requests.get(
        get_roles_url_refined,
        headers=get_roles_headers
    )

    print(response)
    if response.status_code == 200:
        print("Roles obtained")
        print('--------------')
        return response.json()
    else:
        print("Failed to obtain Roles")
        print('--------------')
        return response

def make_role_desc_map(powerbi_id):
    role_desc_map = {}
    response = get_roles(powerbi_id)

    for value in response['value']:
        name = value["Name"]
        desc = value["Description"]
        role_desc_map[name] = desc

    return role_desc_map

def add_user_security(powerbi_id, email, roles, role_desc_map, policies_response):
    print(f"Adding User {email} to Security")

    add_user_security_url_refined = add_user_security_url.replace('<powerbi_id>', powerbi_id)
    add_user_security_headers['Cookie'] = get_api_cookies()
    new_user = {
        "GroupUserName": email,
        "Roles": [{"Name": role, "Description": role_desc_map[role]} for role in roles]
    }
    payload = {}
    payload["Id"] = policies_response["Id"]
    payload["InheritParentPolicy"] = policies_response["InheritParentPolicy"]
    policies = policies_response["Policies"]
    policies.append(new_user)
    payload["Policies"] = policies

    response = requests.put(
        add_user_security_url_refined,
        headers=add_user_security_headers,
        data=json.dumps(payload)
    )

    print(response)
    if response.status_code == 200:
        print(f"Added User to Security")
        print('--------------')
        return response
    else:
        print("Failed to Add User to Security")
        print('--------------')
        return response
    
def add_users_security(dashboard):
    dashboard_path = f'Path=%27/JTC/{dashboard}%27'
    powerbi_id = get_dashboard_id(dashboard_path)

    role_desc_map = make_role_desc_map(powerbi_id)
    
    policies_response = get_policies(powerbi_id)

    with open(SECURITY_DATA, newline='') as f:
        reader = csv.reader(f)
        next(reader)
        for r in reader:
            #Developer's note: Currently, policies are only attained once in line 191 for code efficiency
            #However, there may be some error if another user from another computer were to manually add a user to security
            #while the script is running. If so, the policies in this loop will no longer be accurate, causing a potential error.
            #If needed, get the policies at every loop via the commmented line below, instead of at line 191.
            #policies_response = get_policies(powerbi_id)
            email = r[0]
            roles = r[1].split(',')
            add_user_security(powerbi_id, email, roles, role_desc_map, policies_response)