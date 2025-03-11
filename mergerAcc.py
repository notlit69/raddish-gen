import tls_client
import re
import time
from bs4 import BeautifulSoup
import concurrent.futures
import requests
from urllib.parse import unquote
import random
import time
import tls_client
import threading
from concurrent.futures import ThreadPoolExecutor
from console import Console
from urllib.parse import unquote
console = Console()

proxies = open("Input/streamlabs_proxies.txt").read().splitlines()

def get_proxy():
    proxy = random.choice(proxies)
    if not proxy.startswith("http"):
        proxy = f"http://{proxy}"
    return proxy
def login_streamlabs(email, password):
    proxy = get_proxy()
    ses = tls_client.Session(
            client_identifier="chrome_131", random_tls_extension_order=True
        )
    ses.proxies = {"http": proxy, "https": proxy}    
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "referer": "https://streamlabs.com/slid/signup",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    }

    ses.get("https://streamlabs.com/api/v5/available-features", headers=headers)
    xsrf = ses.cookies.get("XSRF-TOKEN")
    
    if not xsrf:
        return None, None

    ses.headers.update({
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "origin": "https://streamlabs.com",
        "x-xsrf-token": xsrf,
    })

    json_data = {"email": email, "password": password}
    response = ses.post("https://api-id.streamlabs.com/v1/auth/login", json=json_data)

    if response.status_code != 200:
        
        return None, None
    
    slsid = ses.cookies.get("slsid")

    if not slsid:
        return None, None
    
    with open("cookies.txt", "a") as accsave:
        accsave.write(f"{xsrf}:{slsid}\n")

    return xsrf, ses

def get_csrf(ses):
    xsrf_token = ses.cookies.get("XSRF-TOKEN")
    if not xsrf_token:
        return None

    headers = {
        "X-XSRF-Token": xsrf_token,
        "Content-Type": "application/json",
    }
    payload = {"origin": "https://streamlabs.com", "intent": "connect", "state": ""}
    url = "https://api-id.streamlabs.com/v1/identity/clients/419049641753968640/oauth2"

    response = ses.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        return None

    data = response.json()
    redirect_url = data.get("redirect_url")
    if not redirect_url:
        return None

    max_redirects = 10
    redirect_count = 0

    while redirect_url and redirect_count < max_redirects:
        redirect_response = ses.get(redirect_url, allow_redirects=False)
        ses.cookies.update(redirect_response.cookies)

        if redirect_response.status_code in (301, 302) and 'Location' in redirect_response.headers:
            redirect_url = redirect_response.headers['Location']
        else:
            match = re.search(r"var\s+redirectUrl\s*=\s*'(.*?)';", redirect_response.text)
            if match:
                redirect_url = match.group(1)
                ses.get(redirect_url)
            else:
                break

        redirect_count += 1

    if redirect_count >= max_redirects:
        return None

    dashboard_response = ses.get("https://streamlabs.com/dashboard")
    ses.cookies.update(dashboard_response.cookies)

    soup = BeautifulSoup(dashboard_response.text, "html.parser")
    csrf_token = soup.find("meta", {"name": "csrf-token"})

    if csrf_token:
        return csrf_token["content"]
    else:
        return None


def get_twitter_token():
    try:
        with open('Input/twitter.txt', 'r') as f:
            tokens = f.readlines()
        if not tokens:
            return None
        token = tokens[0].strip()
        with open('Input/twitter.txt', 'w') as f:
            f.writelines(tokens[1:])
        return token
    except FileNotFoundError:
        return None

def merge(ses, csrf, twitter_token: str) -> bool:
    max_retries = 5
    retries = 0

    while retries < max_retries:
        try:
            response = ses.get("https://streamlabs.com/api/v5/user/accounts/merge/twitter_account", 
                               params={"r": "/dashboard#/settings/account-settings/platforms"})
            if response.status_code != 200:
                console.error(0, "Failed to get OAuth URL.", error=response.text)
                return False
            
            oauth_url = response.json().get('redirect_url')
            if not oauth_url:
                console.error(0, "Failed to retrieve OAuth URL.", error=response.text)
                return False
            
            oauth_token = oauth_url.split("oauth_token=")[1]
            session = tls_client.Session('chrome_131', random_tls_extension_order=True)
            auth_response = session.get(oauth_url, headers={'cookie': f"auth_token={twitter_token};"})

            try:
                authenticity_token = auth_response.text.split(' <input name="authenticity_token" type="hidden" value="')[1].split('">')[0]
            except IndexError:
                console.error(0, "Invalid twitter token.", twitter=f"{twitter_token[:21]}...")
                return False

            auth_data = {'authenticity_token': authenticity_token, 'oauth_token': oauth_token}
            final_response = session.post('https://twitter.com/oauth/authorize', data=auth_data, 
                                          headers={'cookie': f"auth_token={twitter_token};"})

            try:
                redirect_url = final_response.text.split('<p>If your browser doesn\'t redirect you please <a class="maintain-context" href="')[1].split('">')[0]
                if redirect_url:
                    if 'You are being' in redirect_url:
                        console.error(0, "Twitter account already used.", twitter=f"{twitter_token[:21]}...")
                        return False

                    session.headers.update({'referer': "https://twitter.com"})
                    response = ses.get(unquote(redirect_url).replace("amp;", '').replace("amp;", ''))
                    
                    if response.status_code == 302:
                        return True
                    else:
                        console.error(0, "Failed to link Twitter account.", error=response.text, twitter=f"{twitter_token[:21]}...")
                else:
                    console.error(0, "Failed to find redirect URL", error=response.text, twitter=f"{twitter_token[:21]}...")

                    retries += 1
                    time.sleep(2)
                    continue
            except IndexError:
                retries += 1
                time.sleep(2)
                continue
        except Exception as e:
            console.error(0, "Failed to link Twitter account.", error=e, twitter=f"{twitter_token[:21]}...")
            retries += 1
            time.sleep(2)
            continue

    console.error(0, "Exceeded maximum retries. Failed to link Twitter account.", twitter=f"{twitter_token[:21]}...")

    return False

def fetch_eoy(csrf_token, ses):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'referer': 'https://streamlabs.com/dashboard',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'x-xsrf-token': csrf_token,
    }

    response = ses.get('https://streamlabs.com/api/v5/stats/eoy', headers=headers)

    if response.status_code == 200:
        data = response.json()
        platforms = data.get("platforms2", {})
        
        twitter_linked = "twitter_account" in platforms
        youtube_linked = "youtube_account" in platforms
        kick_linked = "kick_account" in platforms
        facebook_linked = "facebook_account" in platforms
        tiktok_linked = "tiktok_account" in platforms
        twitch_linked = "twitch_account" in platforms
        
        return not (twitter_linked or youtube_linked or kick_linked or facebook_linked or tiktok_linked or twitch_linked)  

    return True 
lock = threading.Lock()

def process_account(email, password):
    xsrf, session = login_streamlabs(email, password)

    if xsrf and session:
        csrf_token = get_csrf(session)
        if csrf_token:
            result = fetch_eoy(csrf_token, session)
            local_part, domain_part = email.split('@')
            masked_domain = '*' * len(domain_part.split('.')[0])
            masked_email = f"{local_part}@{masked_domain}.com"

            if result:
                console.error(0, "Streamlab account status, Trying to merge...", email=masked_email, merged="False")

                twitter_token = get_twitter_token()
                
                if twitter_token:
                    merge_status = merge(session, csrf_token, twitter_token)
                    if merge_status:
                        console.twitter(0, "Twitter merged successfully, Rechecking...", email=masked_email, twitter=f"{twitter_token[:21]}...")
                        with lock:
                            with open("Output/TwitterMerge/merged.txt", "a") as uf:
                                uf.write(f"{email}:{password}\n")
                        result = fetch_eoy(csrf_token, session)

            console.success(0, "Streamlab account status", email=masked_email, merged=not result)

            if result:
                with lock:
                    with open("Output/TwitterMerge/unmerged.txt", "a") as uf:
                        uf.write(f"{email}:{password}\n")
