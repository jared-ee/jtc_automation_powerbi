import json
import requests
import csv

from actions.create.create_apis import get_dashboard_url, get_dashboard_headers, get_data_model_roles_url, get_data_model_roles_headers, get_data_model_role_assignments_url, get_data_model_role_assignments_headers, add_user_row_level_security_url, add_user_row_level_security_headers, get_policies_url, get_policies_headers, add_user_security_url, add_user_security_headers, get_roles_url, get_roles_headers
from actions.cookies_utils import get_api_cookies

from data.data import ROW_LEVEL_SECURITY_DATA, SECURITY_DATA

def get_dashboard_id(dashboard_path):
    print("Getting Dashboard")

    get_dashboard_url_refined = get_dashboard_url.replace('<dashboard_path>', dashboard_path)
    get_dashboard_headers['Cookie'] = get_api_cookies()

    response = requests.get(
        get_dashboard_url_refined,
        headers=get_dashboard_headers
    )

    print(response)
    if response.status_code == 200:
        print("Dashboard obtained")
        print('--------------')
        return response.json()["Id"]
    else:
        print("Failed to Obtain Dashboard")
        print('--------------')
        return response
    
def get_data_model_roles(powerbi_id):
    print("Getting Data Model Roles")

    get_data_model_roles_url_refined = get_data_model_roles_url.replace('<powerbi_id>', powerbi_id)
    get_data_model_roles_headers['Cookie'] = get_api_cookies()

    response = requests.get(
        get_data_model_roles_url_refined,
        headers=get_data_model_roles_headers
    )

    print(response)
    if response.status_code == 200:
        print("Data Model Roles obtained")
        print('--------------')
        return response.json()["value"]
    else:
        print("Failed to obtain Data Model Roles")
        print('--------------')
        return response
    
def get_data_model_role_assignments(powerbi_id):
    print("Getting Data Model Role Assignments")

    get_data_model_role_assignments_url_refined = get_data_model_role_assignments_url.replace('<powerbi_id>', powerbi_id)
    get_data_model_role_assignments_headers['Cookie'] = get_api_cookies()

    response = requests.get(
        get_data_model_role_assignments_url_refined,
        headers=get_data_model_role_assignments_headers
    )

    print(response)
    if response.status_code == 200:
        print("Data Model Role Assignments obtained")
        print('--------------')
        return response.json()["value"]
    else:
        print("Failed to obtain Data Model Role Assignments")
        print('--------------')
        return response
    
def add_user_row_level_security(powerbi_id, assignments, email, role_ids):
    print(f"Adding User {email} to Row Level Security")

    add_user_row_level_security_url_refined = add_user_row_level_security_url.replace('<powerbi_id>', powerbi_id)
    add_user_row_level_security_headers['Cookie'] = get_api_cookies()
    new_user = {
        "GroupUserName": email,
        "DataModelRoles": role_ids
    }
    assignments.append(new_user)

    response = requests.put(
        add_user_row_level_security_url_refined,
        headers=add_user_row_level_security_headers,
        data=json.dumps(assignments)
    )

    print(response)
    if response.status_code == 200:
        print(f"Added User to Row Level Security")
        print('--------------')
        return response
    else:
        print("Failed to Add User to Row Level Security")
        print('--------------')
        return response
    
def add_users_row_level_security(dashboard):
    dashboard_path = f'Path=%27/JTC/{dashboard}%27'
    powerbi_id = get_dashboard_id(dashboard_path)

    data_model_roles = get_data_model_roles(powerbi_id)
    rolename_roleid_dict = {}
    for data_model_role in data_model_roles:
        role_name = data_model_role['ModelRoleName']
        role_id = data_model_role['ModelRoleId']
        rolename_roleid_dict[role_name] = role_id
    
    assignments = get_data_model_role_assignments(powerbi_id)

    with open(ROW_LEVEL_SECURITY_DATA, newline='') as f:
        reader = csv.reader(f)
        next(reader)
        for r in reader:
            #Developer's note: Currently, data model role assignments are only attained once in line 111 for code efficiency
            #However, there may be some error if another user from another computer were to manually add a user to row level security
            #while the script is running. If so, the assignments in this loop will no longer be accurate, causing a potential error.
            #If needed, get the assignments at every loop via the commmented line below, instead of at line 111.
            #assignments = get_data_model_role_assignments(powerbi_id)
            email = r[0]
            role_names = r[1].split(',')
            role_ids = [rolename_roleid_dict[role_name] for role_name in role_names]
            add_user_row_level_security(powerbi_id, assignments, email, role_ids)


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



