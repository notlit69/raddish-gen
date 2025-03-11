import requests
import json
from console import Console
from colorama import Fore

console = Console()

with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    akey = config.get('ScrappeyKey')
    mretries = config.get('PullerRetries')
    
MAX_RETRIES = mretries

def puller(cookies):
    retries = 0 
    while retries < MAX_RETRIES:
        try:
            json_data = {
                'cmd': 'request.get',
                'url': 'https://streamlabs.com/discord/nitro',
                "cloudflareBypass": True,
                'cookies': cookies,
            }

            response = requests.post(
                f'https://publisher.scrappey.com/api/v1?key={akey}',
                json=json_data,
            )

            response.raise_for_status()

            data = response.json()
            return data['solution']['currentUrl']

        except requests.exceptions.RequestException as e:
            console.error(0, f"Request error | error: {e}")
            retries += 1  
            continue
        except KeyError as e:
            console.error(0, f"Response content | error: {response.text if 'response' in locals() else 'No response'}")
            retries += 1
            continue
