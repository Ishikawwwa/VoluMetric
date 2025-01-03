import requests
import time

class ParseUIDS:
    def __init__(self, uid_path):
        self.uid_path = uid_path

    def fetch_uids(self, BASE_URL, HEADERS, params, MAX_SIZE_MB):
        uids = []
        
        next_url = BASE_URL
        
        while len(uids) < 10000 and next_url:
            response = requests.get(next_url, headers=HEADERS, params=params if next_url == BASE_URL else None)
            if response.status_code == 200:
                data = response.json()
                models = data.get('results', [])
                
                for model in models:
                    if len(uids) >= 10000:
                        break
                    uid = model['uid']
                    if model['archives']['gltf']['size'] < MAX_SIZE_MB * 1024 * 1024:
                        uids.append(uid)
                
                # Get the next URL for pagination
                next_url = data.get('next')

                while not next_url:
                    print("Rate limit, retrying")
                    next_url = data.get('next')
                    time.sleep(2)

                if next_url:
                    print(f'Fetching next page: {next_url}')
            else:
                print(f'Error fetching models: {response.status_code}')
                break

            # So the API is not banning us too often
            #time.sleep(5)

        return uids

    def parse(self, MAX_FILE_SIZE_MB):

        f = open("TOKEN.txt", 'r')
        API_TOKEN = f.read()
        HEADERS = {
            'Authorization': f'Token {API_TOKEN}'
        }

        BASE_URL = 'https://api.sketchfab.com/v3/models'

        # Define the parameters for the request
        params = {
            'downloadable': 'true',  # Filter to only include downloadables
            'license': 'CC0,CC-BY,CC-BY-SA',  # Filter to include only free models
            'sort_by': '-likeCount',  # Sort by most liked models
            'type': 'models',
            'q': ''
        }

        # Fetch the UIDs
        uids = self.fetch_uids(BASE_URL, HEADERS, params, MAX_FILE_SIZE_MB)

        f = open(self.uid_path, 'w')
        for uid in uids:
            f.write(f"{uid}\n")

parser = ParseUIDS("uids.txt")
parser.parse(20)
