import argparse
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def search_places(query):
    ig_access_token = os.environ.get('IG_ACCESS_TOKEN')
    
    if not ig_access_token:
        print("Error: IG_ACCESS_TOKEN must be set in .env")
        return

    # Facebook Graph API Pages Search endpoint
    search_url = "https://graph.facebook.com/v22.0/pages/search"
    params = {
        'q': query,
        'fields': 'id,name,location',
        'access_token': ig_access_token
    }

    res = requests.get(search_url, params=params)
    data = res.json()

    if 'error' in data:
        print("Error during search:", data['error'].get('message', data['error']))
        return

    places = data.get('data', [])
    if not places:
        print("No matching places found.")
        return

    for place in places:
        name = place.get('name', 'Unknown')
        page_id = place.get('id', 'Unknown')
        location = place.get('location', {})
        
        city = location.get('city', '')
        state = location.get('state', '')
        country = location.get('country', '')
        street = location.get('street', '')
        
        address_parts = [p for p in [street, city, state, country] if p]
        address = ", ".join(address_parts) if address_parts else "No address info"
        
        # Format output so the agent can parse it line-by-line easily
        print(f"[{page_id}] {name} | {address}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Search for Facebook Places to get Location IDs for Instagram Posts")
    parser.add_argument('query', help='Name of the place or business to search for')
    
    args = parser.parse_args()
    search_places(args.query)
