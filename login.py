import curl_cffi.requests
import time
import json
import urllib.parse
import requests
from concurrent.futures import ThreadPoolExecutor
from console import Console
import threading
from colorama import Fore
console = Console()
file_lock = threading.Lock()
import random

failed = 0
errorFetched = 0
retrieved = 0


def remove_line(file, line_to_remove):
    with file_lock:
        with open(file, "r") as f:
            lines = f.readlines()

        with open(file, "w") as f:
            for line in lines:
                if not line.strip().startswith(line_to_remove.strip()):
                    f.write(line)
                else:
                    return None
                


class Uwu:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.session = curl_cffi.requests.session.Session(impersonate="chrome")

        self.proxies = self.load_proxies()
        self.session.proxies = self.get_random_proxy()

    def load_proxies(self):
        try:
            with open("Input/streamlabs_proxies.txt", "r") as f:
                proxies = [line.strip() for line in f if line.strip()]
            if not proxies:
                raise ValueError("Proxy list is empty!")
            return proxies
        except Exception as e:
            console.error(f"Error loading proxies: {e}")
            return []

    def get_random_proxy(self):
        if not self.proxies:
            console.error("No proxies available! Running without a proxy.")
            return {}

        proxy = random.choice(self.proxies)

        try:
            if proxy.startswith("http://") or proxy.startswith("https://"):
                formatted_proxy = proxy 
            else:
                formatted_proxy = f"http://{proxy}"

            return {"http": formatted_proxy, "https": formatted_proxy}
        except Exception as e:
            console.error(f"Error formatting proxy: {e}")
            return self.get_random_proxy()

        
    def _login(self):
        global failed
        url = "https://api-id.streamlabs.com/v1/auth/login"
        payload = {
            "email": self.email,
            "password": self.password
        }
        headers = {
            "host": "api-id.streamlabs.com",
            "connection": "keep-alive",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-ch-ua": "\"Not(A:Brand\";v=\"99\", \"Google Chrome\";v=\"133\", \"Chromium\";v=\"133\"",
            "sec-ch-ua-mobile": "?0",
            "client-id": "419049641753968640",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "origin": "https://streamlabs.com",
            "sec-fetch-site": "same-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://streamlabs.com/",
            "accept-language": "en-US,en;q=0.9",
            "x-xsrf-token": self.XSRF_TOKEN
        }

        response = self.session.post(url, json=payload, headers=headers)
        local_part, domain_part = self.email.split('@')
        masked_domain = '*' * len(domain_part.split('.')[0])
        masked_email = f"{local_part}@{masked_domain}.com"

        if response.status_code == 200:
            return True

        console.error(f"Failed to login to streamlabs account {Fore.LIGHTBLACK_EX}email:{Fore.RESET} {masked_email}")
        failed += 1
        with open("Output/Login/failed.txt", "a") as file:
            file.write(f"{self.email}:{self.password}\n")
        return False

    def _get_default_cookies(self):
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-GB,en;q=0.9',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        }

        response = self.session.get(url='https://streamlabs.com/slid/signup?r=https%3A%2F%2Fstreamlabs.com%2Fdashboard', headers=headers)
        self.XSRF_TOKEN = urllib.parse.unquote(self.session.cookies["XSRF-TOKEN"])
        return self.XSRF_TOKEN

    def _connect(self):
        global retrieved, failed
        url = "https://api-id.streamlabs.com/v1/identity/clients/419049641753968640/oauth2"
        payload = {
            "origin": "https://streamlabs.com",
            "intent": "connect",
            "state": "e30="
        }
        headers = {
            "host": "api-id.streamlabs.com",
            "connection": "keep-alive",
            "sec-ch-ua-platform": "\"Windows\"",
            "x-xsrf-token": self.XSRF_TOKEN,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "accept": "application/json, text/plain, */*",
            "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
            "content-type": "application/json",
            "sec-ch-ua-mobile": "?0",
            "origin": "https://streamlabs.com",
            "sec-fetch-site": "same-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://streamlabs.com/",
            "accept-language": "en-US,en;q=0.9",
        }

        response = self.session.post(url, json=payload, headers=headers, allow_redirects=True)

        try:
            redirect_url = response.json()["redirect_url"].replace('\/', '/')
        except:
            local_part, domain_part = self.email.split('@')
            masked_domain = '*' * len(domain_part.split('.')[0])
            masked_email = f"{local_part}@{masked_domain}.com"


            console.error(f"Failed to connect to streamlabs account {Fore.LIGHTBLACK_EX}email:{Fore.RESET} {masked_email}")
            failed += 1

            with open("Output/Login/retry.txt", "a") as file:
                file.write(f"{self.email}:{self.password}\n")
            return False

        headers = {
            "host": "streamlabs.com",
            "connection": "keep-alive",
            "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "navigate",
            "sec-fetch-dest": "document",
            "referer": "https://streamlabs.com/slid/verify-email?email=",
            "accept-language": "en-US,en;q=0.9",
        }

        response = self.session.get(redirect_url, headers=headers, allow_redirects=True)

        if "https://streamlabs.com/slid/authorize" in response.url:
            response = self.session.get(response.url, headers=headers, allow_redirects=True)

        if "https://streamlabs.com/connect" in response.url:
            redirectUrl = response.text.split("var redirectUrl = '")[1].split("'")[0]
            response = self.session.get(url=redirectUrl, headers=headers, allow_redirects=True)

            if "https://streamlabs.com/dashboard" in response.url:
                csrf_token = response.text.split('name="csrf-token" content="')[1].split('"')[0]
                local_part, domain_part = self.email.split('@')
                masked_domain = '*' * len(domain_part.split('.')[0])
                masked_email = f"{local_part}@{masked_domain}.com"
                console.login(f"Successfully logged into streamlab account {Fore.LIGHTBLACK_EX}email:{Fore.RESET} {masked_email}")
                # with open("success.txt", "a") as file:
                #     file.write(f"{self.email}:{self.password}:{urllib.parse.unquote(self.session.cookies.get('XSRF-TOKEN'))}:{urllib.parse.unquote(self.session.cookies.get('slsid'))}\n")
                retrieved += 1
                return urllib.parse.unquote(self.session.cookies.get('slsid'))
            else:
                local_part, domain_part = self.email.split('@')
                masked_domain = '*' * len(domain_part.split('.')[0])
                masked_email = f"{local_part}@{masked_domain}.com"
                console.error(f"Failed to connect to streamlabs account {Fore.LIGHTBLACK_EX}email:{Fore.RESET} {masked_email}")
                failed += 1

                return False
        else:
            local_part, domain_part = self.email.split('@')
            masked_domain = '*' * len(domain_part.split('.')[0])
            masked_email = f"{local_part}@{masked_domain}.com"
            console.error(f"Failed to connect to streamlabs account {Fore.LIGHTBLACK_EX}email:{Fore.RESET} {masked_email}")
            failed += 1

            return False

    def _start(self, max_attempts=10):
        attempt = 0

        while attempt < max_attempts:   
            try:
                login_status = False
                XSRF_TOKEN = self._get_default_cookies()

                if XSRF_TOKEN:
                    login_status = self._login()

                if login_status:
                    csrf_token = self._connect()
                    if csrf_token:
                        return csrf_token

                attempt += 1

                if attempt >= max_attempts:
                    remove_line("Output/accounts.txt", f"{self.email}:{self.password}")

            except Exception as e:
                attempt += 1

                local_part, domain_part = self.email.split('@')
                masked_domain = '*' * len(domain_part.split('.')[0])
                masked_email = f"{local_part}@{masked_domain}.com"

                console.error(f"Failed to login to Streamlabs account {Fore.LIGHTBLACK_EX}email:{Fore.RESET} {masked_email} {Fore.LIGHTBLACK_EX}error:{Fore.RESET} {str(e)} | {Fore.LIGHTRED_EX}Retrying..{Fore.RESET} {Fore.LIGHTBLACK_EX}Attempt: {Fore.RESET}{attempt}/{max_attempts}")

                if attempt >= max_attempts:
                    with open("Output/Login/failed.txt", "a") as file:
                        file.write(f"{self.email}:{self.password}\n")
                    break
                
                time.sleep(2)