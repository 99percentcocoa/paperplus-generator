import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

WEB_APP_URL = os.getenv("WEB_APP_URL")
SKILLS_FILE = "skills.json"

def _fetch_from_api(url):
    """Fetch data from the web app API"""
    try:
        # requests.get automatically handles the 302 redirect from Google
        response = requests.get(url)
        
        # Raise an exception for 4XX or 5XX errors
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None

def _transform_data(data):
    """
    Transform API data:
    - Remove "No." column
    - Convert headers to lowercase snake_case
    """
    header_map = {
        "Code": "code",
        "Difficulty Level": "difficulty_level",
        "Skill": "skill",
        "Example": "example",
        "Misconceptions": "misconceptions",
        "Dependencies": "dependencies",
    }
    
    transformed = []
    for item in data:
        new_item = {}
        for old_key, new_key in header_map.items():
            if old_key in item:
                new_item[new_key] = item[old_key]
        transformed.append(new_item)
    
    return transformed

def _load_local_data():
    """Load skills from local cached file"""
    try:
        with open(SKILLS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def _save_data(data):
    """Save data to local file"""
    with open(SKILLS_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Updated {SKILLS_FILE} with {len(data)} items")

def get_skills():
    """
    Get skills data from API, checking for changes.
    
    Always attempts to fetch from the API first.
    - If API succeeds: compares with local cache and updates only if data changed
    - If API fails: returns cached data if available
    
    Returns:
        list: Skills data with transformed headers, or None if API fails and no cache exists
    """
    # Fetch from API
    remote_data = _fetch_from_api(WEB_APP_URL)
    
    if remote_data is None:
        # API call failed - return cached data if available
        print("Falling back to cached data")
        return _load_local_data()
    
    # Transform the data
    transformed_data = _transform_data(remote_data)
    
    # Check if data changed
    local_data = _load_local_data()
    
    if local_data != transformed_data:
        _save_data(transformed_data)
    else:
        print("Data unchanged, skipping save")
    
    return transformed_data

if __name__ == "__main__":
    data = get_skills()
    
    if data:
        print(f"Successfully retrieved {len(data)} rows.")
        print(data[0])