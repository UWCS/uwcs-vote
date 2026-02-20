import requests
from defusedxml import ElementTree as ET


def fetch_webgroups(id):
    """
    Fetches the list of webgroups a user ID is in
    """
    url = f"https://webgroups.warwick.ac.uk/query/user/u{id}/groups"

    try:
        response = requests.get(url, timeout=7)
        if response.status_code == 200:
            try:
                root = ET.fromstring(response.content)
                groups = [
                    node.get("name")
                    for node in root.findall("group")
                    if node.get("name")
                ]
                return groups
            except ET.ParseError:
                print(f"Couldn't parse groups for {id}")
    except Exception as e:
        print(f"Unknown exception: {e}")
    return []
