import json
import tls_client
import time
from solver import solve_captcha
import solver
from mail import tempmail
from login import Uwu
from console import Console
from urllib.parse import unquote
import re
from bs4 import BeautifulSoup
import threading
from puller import puller
from colorama import Fore
import os
from datetime import datetime
from colorama import Fore
import json
import ctypes
import shutil
from itertools import cycle
from threading import Lock
from mergerAcc import process_account
import requests
import hashlib
import sys
from linker import linkpromo, oneMonth, threeMonths, linked
import random
from concurrent.futures import ThreadPoolExecutor
import string
with open('config.json', 'r', encoding='utf-8-sig') as file:
    config_data = json.load(file)

console = Console()
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    license_key = config.get("license")


def generate_random_password(format_string):
    result = []
    for char in format_string:
        if char == '*':
            result.append(random.choice(string.ascii_letters + string.digits + '*#$@&%!^'))
        else:
            result.append(char)
    return ''.join(result)


passwordhehe = generate_random_password(config_data['StreamlabAccountPassword'])
onlygen = config.get("GenPromoOnly")
autolink = config.get("AutoLink")
accgen = config.get("GenAccountsOnly")
changepass = config.get("AutoPassChange")
linktwitter = config.get("LinkTwitter")

file_lock = threading.Lock()

class bcolors:
    BLACK = '\033[30m'
    TIME = '\033[90m'
    OKBLUE = '\033[94m'
    DEEPBLUE = '\033[34m'
    PURPLE = '\033[95m'
    FAIL = '\033[91m'
    SUCCESS = '\033[92m'
    ENDC = '\033[0m'
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    TIME = '\033[90m'
    DARKGREEN = '\033[32m'

def timestamp():
    return f"{bcolors.TIME}{datetime.datetime.now().strftime('%H:%M:%S')} → {bcolors.ENDC}"

def get_twitter_token():
    with file_lock:
        try:
            with open('Input/twitter.txt', 'r') as f:
                tokens = f.readlines()
            if not tokens:
                # console.error(thread_id, "No Twitter tokens found in twitter.txt.")
                return None
            token = tokens[0].strip()
            with open('Input/twitter.txt', 'w') as f:
                f.writelines(tokens[1:])
            return token
        except FileNotFoundError:
            console.error(0, "twitter.txt file not found.")
            return None





retrieved = 0
failed = 0
error = 0
purchased = 0
errorFetch = 0

start_time = time.perf_counter()
elapsed_time_running = True
elapsed_time_running3 = True

def update_elapsed_time():
    global elapsed_time_running
    while elapsed_time_running:
        elapsed_time = time.perf_counter() - start_time
        title = (f"Streamlabs 1 Month Promo Gen | Fast Boost | https://fastbb.mysellix.io | https://t.me/fastboostservices | Accounts Generated: {retrieved} | Cloudflare Solved: {solver.cfSolved} | Email Purchased: {purchased} | Failed: {errorFetch} | Time Elapsed: {elapsed_time:.6f} seconds")
        ctypes.windll.kernel32.SetConsoleTitleW(title)

def update_elapsed_time3():
    global elapsed_time_running3
    while elapsed_time_running3:
        elapsed_time = time.perf_counter() - start_time
        title = (f"Streamlabs 1 Month Promo Gen | Fast Boost | https://fastbb.mysellix.io | https://t.me/fastboostservices | Accounts Logged In: {retrieved} | Success: {oneMonth} | Failed: {errorFetch} | Time Elapsed: {elapsed_time:.6f} seconds")
        ctypes.windll.kernel32.SetConsoleTitleW(title)


def update_elapsed_time2():
    title = (f"Streamlabs 1 Month Promo Gen | Fast Boost | https://fastbb.mysellix.io | https://t.me/fastboostservices")
    ctypes.windll.kernel32.SetConsoleTitleW(title)

def time_right_now():
    return datetime.now().strftime("%I:%M %p")

def timestamp():
    return datetime.now().strftime("%H:%M:%S") 



def extract_cookies(formatted_cookies):
    slsid_match = re.search(r'slsid=([^;]+)', formatted_cookies)
    xsrf_match = re.search(r'XSRF-TOKEN=([^;]+)', formatted_cookies)

    if slsid_match and xsrf_match:
        slsid = slsid_match.group(1)
        xsrf_token = xsrf_match.group(1)
        return slsid, xsrf_token
    else:
        return None, None



twitter_tokens_exhausted = False
threads = []

with open("Input/streamlabs_proxies.txt", "r") as f:
    proxies = [line.strip() for line in f.readlines() if line.strip()]

proxy_index = 0

def get_next_proxy():
    global proxy_index
    proxy = proxies[proxy_index % len(proxies)]
    proxy_index += 1
    return f"http://{proxy}"

def creator(thread_id):
    global errorFetch, retrieved, oneMonth, twitter_tokens_exhausted, cfSolved, purchased

    while True:
        
        twitter_token = get_twitter_token()
        if not twitter_token:
            # console.error(thread_id, "No more Twitter tokens available. Stopping account creation.")
            twitter_tokens_exhausted = True
            break

        
        ses = tls_client.Session(client_identifier="chrome_131", random_tls_extension_order=True)
        captcha_token = solve_captcha(thread_id)
        temp_mail_instance = tempmail()
        email, id = temp_mail_instance.create_temp_email(thread_id)
        if not proxies:
            console.error(thread_id, "No proxies available. Stopping account creation.")
            break

        proxy = get_next_proxy() 
    
    
        ses.proxies = {
            "http": proxy,
            "https": proxy,
        }

        if not email or not id:
            return

        local_part, domain_part = email.split('@')
        masked_domain = '*' * len(domain_part.split('.')[0])
        masked_email = f"{local_part}@{masked_domain}.com"
        
        console.purchase(thread_id, f"Successfully purchased email", email=masked_email)
        purchased += 1


        headers = {
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'en-US,en;q=0.9',
                'priority': 'u=1, i',
                'referer': 'https://streamlabs.com/slid/signup',
                'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
                'sec-ch-ua-arch': '"x86"',
                'sec-ch-ua-bitness': '"64"',
                'sec-ch-ua-full-version': '"132.0.6834.160"',
                'sec-ch-ua-full-version-list': '"Not A(Brand";v="8.0.0.0", "Chromium";v="132.0.6834.160", "Google Chrome";v="132.0.6834.160"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-model': '""',
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua-platform-version': '"10.0.0"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
            }
        response2=ses.get('https://streamlabs.com/api/v5/available-features', headers=headers)
        xsrf = ses.cookies.get('XSRF-TOKEN')


        if not xsrf:
            console.error(thread_id, "Failed To Fetch XSRF token", error=response2.text[:50])
            continue

        ses.headers.update({
            'accept': 'application/json, text/plain, */*',
            'cache-control': 'no-cache',
            'client-id': '419049641753968640',
            'content-type': 'application/json',
            'origin': 'https://streamlabs.com',
            'referer': 'https://streamlabs.com/',
            'x-xsrf-token': xsrf,
        })

        pas1 = generate_random_password(config_data['StreamlabAccountPassword'])
        
        json_data = {
            'email': email,
            'username': '',
            'password': pas1,
            'agree': True,
            'agreePromotional': False,
            'dob': '',
            'captcha_token': captcha_token,
            'locale': 'en-US',
        }


        # print(captcha_token)


        retry_count = 0
        max_retries = 100

        while retry_count < max_retries:
            response = ses.post('https://api-id.streamlabs.com/v1/auth/register', json=json_data)
            
            local_part, domain_part = email.split('@')
            masked_domain = '*' * len(domain_part.split('.')[0])
            masked_email = f"{local_part}@{masked_domain}.com"

            if response.status_code == 200:
                break

            try:
                error_msg = response.json().get("message", "")
                
                if "requests too quickly" in error_msg:
                    sleep_time = int(''.join(filter(str.isdigit, error_msg)))
                    retry_count += 1
                    console.sleep(thread_id, "Ratelimited, sleeping..", email=masked_email, time=f"{sleep_time} seconds")
                    time.sleep(sleep_time)
                else:
                    time.sleep(1)
                    retry_count += 1

            except json.JSONDecodeError:
                time.sleep(1)

                retry_count += 1

            time.sleep(1)
            retry_count += 1

        if retry_count == max_retries:
            console.error(thread_id, "Max retries reached, Skipping this account.", email=masked_email, error=error_msg)
            with open("Output/emails.txt", "a") as f:
                    f.write(f"{email}:{id}\n")
            errorFetch += 1
            return

        otp_verified = False
        while not otp_verified:
            otp = temp_mail_instance.get_email_code(id, thread_id)

            if otp:
                otp_verified = verifier(thread_id, xsrf, otp, email, ses)
                if otp_verified:
                    console.gen(thread_id, "Generated streamlabs account", email=masked_email, otp=otp)
                    retrieved += 1
                    
                    if linktwitter:
                        csrf_token = csrf(thread_id, xsrf, ses)
                        merge_success = merge(thread_id, ses, csrf_token, twitter_token)
                        if merge_success:
                            console.twitter(thread_id, "Twitter linked to account", email=masked_email, twitter=twitter_token[:21])
                            if changepass:
                                time.sleep(5)
                                changePassFunction(xsrf, pas1, ses, thread_id, masked_email, email)
                            else:
                                with open("Output/accounts.txt", "a") as f:
                                    f.write(f"{email}:{pas1}\n")
                        else:
                            console.error(thread_id, "Failed to link twitter", email=masked_email, twitter=twitter_token[:21])
                            with open("Output/accounts.txt", "a") as f:
                                f.write(f"{email}:{pas1}\n")

                    else:
                        if changepass:
                            time.sleep(5)
                            changePassFunction(xsrf, pas1, ses, thread_id, masked_email, email)
                        else:
                            with open("Output/accounts.txt", "a") as f:
                                f.write(f"{email}:{pas1}\n")
                break







def changePassFunction(xsrf, currentpass, ses, thread_id, masked_email, email):
    url = "https://api-id.streamlabs.com/v1/auth/change-password"
    pas2 = generate_random_password(config_data['StreamlabAccountPassword'])

    payload = {
        "current_password": currentpass,
        "new_password": pas2,
        "new_password_confirmation": pas2
    }
    ses.headers.update(
        {
            "x-xsrf-token": xsrf,
        }
    )

    response = ses.post(url, json=payload)
    if response.status_code == 204:
        console.password(thread_id, "Account password changed", email=masked_email)
        with open("Output/accounts.txt", "a") as f:
            f.write(f"{email}:{pas2}\n")

        return True
    else:
        console.error(thread_id, "Failed to change password", email=masked_email, error=response.text)
        return False














def verifier(thread_id, xsrf, otp, email, ses):
    url = "https://api-id.streamlabs.com/v1/users/@me/email/verification/confirm"
    payload = {
        "code": otp,
        "email": email,
        "tfa_code": ""
    }
    ses.headers.update(
        {
            "x-xsrf-token": xsrf,
        }
    )

    response = ses.post(url, json=payload)
    if response.status_code == 204:
        return True
    else:
        local_part, domain_part = email.split('@')
        masked_domain = '*' * len(domain_part.split('.')[0])
        masked_email = f"{local_part}@{masked_domain}.com"

        console.error(thread_id, "Failed to verify streamlabs account", email=masked_email, otp=otp, error=response.text)
        return False














def csrf(thread_id, xsrf, ses):
    url = "https://api-id.streamlabs.com/v1/identity/clients/419049641753968640/oauth2"
    payload = {
        "origin": "https://streamlabs.com",
        "intent": "connect",
        "state": ""
    }
    headers = {
        "X-XSRF-Token": xsrf,
        "Content-Type": "application/json"
    }
    
    response = ses.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        redirect_url = data.get("redirect_url")
        
        if redirect_url:
            while redirect_url:
                redirect_response = ses.get(redirect_url, allow_redirects=False)
                ses.cookies.update(redirect_response.cookies)
                if redirect_response.status_code in (301, 302) and 'Location' in redirect_response.headers:
                    redirect_url = redirect_response.headers['Location']
                else:
                    match = re.search(r"var\s+redirectUrl\s*=\s*'(.*?)';", redirect_response.text)
                    if match:
                        redirect_url = match.group(1)
                        red4 = ses.get(redirect_url)
                        ses.cookies.update(red4.cookies)
                        red5 = ses.get("https://streamlabs.com/dashboard")
                        ses.cookies.update(red5.cookies)
                        soup = BeautifulSoup(red5.text, "html.parser")
                        csrf = soup.find("meta", {"name": "csrf-token"})["content"]
                        return csrf
        else:
            console.error(thread_id, "Redirect URL not found in the response", error=response.text)
            return None
    else:
        console.error(thread_id, "Request failed", error=response.text)
        return None

















def merge(thread_id, ses, csrf, twitter_token: str) -> bool:
    try:
        response = ses.get(
            "https://streamlabs.com/api/v5/user/accounts/merge/twitter_account",
            params={"r": "/dashboard#/settings/account-settings/platforms"}
        )
        
        if response.status_code != 200:
            console.error(thread_id, "Failed to get OAuth URL", error=response.status_code)
            return False
                
        oauth_url = response.json().get('redirect_url')
        oauth_token = oauth_url.split("oauth_token=")[1]

        session = tls_client.Session('chrome_131', random_tls_extension_order=True)

        auth_response = session.get(
            oauth_url, 
            headers={'cookie': f"auth_token={twitter_token};"}
        )
        
        try:
            authenticity_token = auth_response.text.split(
                ' <input name="authenticity_token" type="hidden" value="'
            )[1].split('">')[0]
        except IndexError:
            # console.error(thread_id, "Invalid Twitter Account.")
            return False
            
        auth_data = {
            'authenticity_token': authenticity_token,
            'oauth_token': oauth_token
        }
            
        final_response = session.post(
            'https://twitter.com/oauth/authorize', 
            data=auth_data, 
            headers={'cookie': f"auth_token={twitter_token};"}
        )
        
        redirect_url = None
        for attempt in range(3):
            try:
                redirect_url = final_response.text.split(
                    '<p>If your browser doesn\'t redirect you please <a class="maintain-context" href="'
                )[1].split('">')[0]
                break
            except IndexError:
                console.error(thread_id, "Failed to extract redirect URL", twitter=twitter_token[:21], attempt=f"{attempt+1}/3")


                if attempt == 2:
                    return False
                final_response = session.post(
                    'https://twitter.com/oauth/authorize', 
                    data=auth_data, 
                    headers={'cookie': f"auth_token={twitter_token};"}
                )
        
        if redirect_url:
            if 'You are being' in redirect_url:
                console.error(thread_id, "Twitter account already used", twitter=twitter_token[:21])
                return False
            session.headers.update({'referer': "https://twitter.com"})
            response = ses.get(unquote(redirect_url).replace("amp;", '').replace("amp;", ''))
            if response.status_code == 302:
                return True
            else:
                console.error(thread_id, "Failed to link twitter account", twitter=twitter_token[:21], error=response.json())
        else:
            console.error(thread_id, "Failed to find redirect URL")
                
        return False
    except Exception as e:
        console.error(thread_id, "Failed to link twitter account", twitter=twitter_token[:21], error=e)
        return False

columns = shutil.get_terminal_size().columns






















thread_id_counter = 1

def create_threads():
    global threads, twitter_tokens_exhausted, thread_id_counter
    
    thread_count = config.get("Threads", 3)
    
    while not twitter_tokens_exhausted:
        batch_threads = []
        
        for _ in range(thread_count):
            thread = threading.Thread(target=creator, args=(thread_id_counter,))
            thread.daemon = True
            thread.start()
            batch_threads.append(thread)
            threads.append(thread)
            
            thread_id_counter += 1
        
        for thread in batch_threads:
            thread.join()
        

csrf_tokens = []



def main():
    global errorFetch, oneMonth

    update_elapsed_time2()

    print(f"{Fore.LIGHTBLUE_EX}Promotion Generator{Fore.RESET} v1.5.0".center(columns))
    print()
    console.success(0, f"{Fore.LIGHTWHITE_EX}1.{Fore.RESET} Streamlabs Account Generator")
    console.success(0, f"{Fore.LIGHTWHITE_EX}2.{Fore.RESET} Nitro Promotion Puller")
    console.success(0, f"{Fore.LIGHTWHITE_EX}3.{Fore.RESET} Twitter Token Merger")
    choice = input(f"\n{Fore.LIGHTBLACK_EX}{timestamp()}{Fore.RESET} {Fore.LIGHTBLUE_EX}OPT {Fore.LIGHTBLACK_EX}:{Fore.RESET} Select An Option: ")
    if choice == "1":
        thread_count = config.get("Threads", 3)
        for _ in range(thread_count):
            threading.Thread(target=update_elapsed_time, daemon=True).start()

        create_threads()


        print()
        console.end(0, "Finished generating streamlabs accounts", accounts=retrieved)
        input(f"{Fore.LIGHTBLACK_EX}{timestamp()}{Fore.RESET} {Fore.LIGHTMAGENTA_EX}END {Fore.LIGHTBLACK_EX}:{Fore.RESET} Press enter to exit: ")
        sys.exit(1)
    elif choice == "3":
        lock = threading.Lock()

        while True:
            with lock:
                with open("Output/accounts.txt", "r") as f:
                    accounts = f.readlines()

            if not accounts:
                console.error(0, "No more accounts to process.")
                input(f"{Fore.LIGHTBLACK_EX}{timestamp()}{Fore.RESET} {Fore.LIGHTMAGENTA_EX}END {Fore.LIGHTBLACK_EX}:{Fore.RESET} Press enter to exit: ")
                break

            batch_size = min(15, len(accounts))
            batch = accounts[:batch_size]
            remaining_accounts = accounts[batch_size:]

            with lock:
                with open("Output/accounts.txt", "w") as f:
                    f.writelines(remaining_accounts)
            thread_count = config.get("TwitterMergerThreads", 3)

            print()
            with ThreadPoolExecutor(max_workers=thread_count) as executor:
                for account in batch:
                    email, password = account.strip().split(":")
                    executor.submit(process_account, email, password)

            time.sleep(5)
    elif choice == "2":
        accounts = open("Output/accounts.txt", "r").read().splitlines()
        thread_count = config.get("Login+PullerThreads", 3)
        for _ in range(thread_count):
            threading.Thread(target=update_elapsed_time, daemon=True).start()

        logged_in_accounts = []

        def mask_email(email):
            try:
                local_part, domain_part = email.split('@')
                domain_name, domain_extension = domain_part.split('.', 1)
                masked_domain = '*' * len(domain_name)
                return f"{local_part}@{masked_domain}.{domain_extension}"
            except ValueError:
                return "Hidden Email"

        def login_and_get_csrf(account_line, thread_id):
            try:
                email, password = account_line.split(":")
            except ValueError:
                return None
            csrf_token = Uwu(email, password)._start()
            if csrf_token:
                console.login(thread_id, "Successfully logged in", email=mask_email(email))
                return (email, csrf_token)
            return None

        with ThreadPoolExecutor(max_workers=thread_count) as login_executor:
            login_futures = {}
            for idx, account in enumerate(accounts):
                thread_id = idx + 1
                future = login_executor.submit(login_and_get_csrf, account, thread_id)
                login_futures[future] = (thread_id, account)
                
            for future in login_futures:
                thread_id, account = login_futures[future]
                try:
                    result = future.result()
                    if result is not None:
                        logged_in_accounts.append((result[0], result[1], thread_id))
                except Exception as e:
                    email = account.split(":")[0] if ":" in account else "unknown"
                    console.error(thread_id, "Login error for account", email=mask_email(email), error=str(e))

        with ThreadPoolExecutor(max_workers=thread_count) as puller_executor:
            puller_futures = {}
            for email, csrf_token, thread_id in logged_in_accounts:
                future = puller_executor.submit(puller, "slsid=" + csrf_token, thread_id)
                puller_futures[future] = (email, thread_id)
                
            for future in puller_futures:
                email, thread_id = puller_futures[future]
                try:
                    promo = future.result()
                    if promo:
                        if "https://discord.com/billing/partner-promotions/" in promo:
                            console.success(thread_id, "Successfully fetched promo link", promo=promo[:159])
                            oneMonth += 1
                            if autolink:
                                linkpromo(promo, thread_id)
                            elif onlygen:
                                with open("Output/promos.txt", "a") as f:
                                    f.write(f"{promo}\n")
                            elif autolink and onlygen:
                                with open("Output/promos.txt", "a") as f:
                                    f.write(f"{promo}\n")
                        else:
                            masked_email = mask_email(email)
                            console.error(thread_id, "Failed to fetch promo link", email=masked_email, error=promo)
                            errorFetch += 1
                except Exception as e:
                    console.error(thread_id, "Error in puller thread", error=str(e))

def getchecksum():
    md5_hash = hashlib.md5()
    file = open("".join(sys.argv), "rb")
    md5_hash.update(file.read())
    digest = md5_hash.hexdigest()
    return digest

def clear():
    os.system("clear||cls")


if __name__ == "__main__":
    clear()
    #answer()
    main()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting program.")

