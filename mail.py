import requests
import time
import re
import json
import random
import string
from bs4 import BeautifulSoup
from console import Console
from colorama import Fore

console = Console()

with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    API_TOKEN = config.get("EmailProviderKey") 
    EMAIL_DOMAIN = config.get("DomainType")
    RETRY = config.get("OTPRetry")
    provider = config.get("EmailProvider", "kopeechka").lower()

if provider == "kopeechka":
    BASE_URL = "https://api.kopeechka.store"
elif provider == "anymessage":
    BASE_URL = "https://api.anymessage.shop"
elif provider == "tempgmail":
    BASE_URL = "https://api.online-disposablemail.com/api"
    SERVICE_ID = "46"
    EMAIL_TYPE_ID = "3"
else:
    raise Exception("Unsupported email provider. Use 'kopeechka', 'anymessage', or 'tempgmail'.")

class tempmail:
    def create_temp_email(self, thread_id):
        if provider == "tempgmail":
            return self.create_temp_email_tempgmail(thread_id)
        url = f"{BASE_URL}/mailbox-get-email?site=streamlabs.com&mail_type={EMAIL_DOMAIN}&token={API_TOKEN}&api=2.0"
        response = requests.get(url).json()
        if response['status'] == 'OK':
            return response['mail'], response['id']
        console.error("Failed to buy email", error=response, thread=thread_id)
        return None, None

    def create_temp_email_tempgmail(self, thread_id):
        url = f"{BASE_URL}/mailbox"
        params = {
            "apiKey": API_TOKEN,
            "serviceId": SERVICE_ID,
            "emailTypeId": EMAIL_TYPE_ID,
            "quantity": 1,
            "linkPriority": True
        }
        response = requests.get(url, params=params).json()
        if response["code"] == 200:
            order = response["data"]["orders"][0]
            return order["email"], order["orderId"]
        console.error("Error purchasing email", error=response.get('msg', 'Unknown error'), thread=thread_id)
        return None, None

    def get_email_code(self, email_id, thread_id, max_attempts=RETRY, retry_interval=1):
        if provider == "tempgmail":
            return self.get_email_code_tempgmail(email_id, thread_id, max_attempts)
        for _ in range(max_attempts):
            url = f"{BASE_URL}/mailbox-get-message?id={email_id}&token={API_TOKEN}&api=2.0"
            response = requests.get(url).json()
            if response['status'] == 'OK' and 'fullmessage' in response:
                otp_match = re.search(r'<div[^>]*>\s*(\d{6,8})\s*</div>', response['fullmessage'])
                if otp_match:
                    return otp_match.group(1)
            time.sleep(retry_interval)
        console.error("Failed to fetch OTP", email_id=str(email_id)[:6], error=response, thread=thread_id)
        return None

    def get_email_code_tempgmail(self, order_id, thread_id, max_attempts=RETRY):
        url = f"{BASE_URL}/latest/code"
        params = {"orderId": order_id}
        for _ in range(max_attempts):
            response = requests.get(url, params=params).json()

            if response["code"] == 200 and response["data"]["code"]:
                return response["data"]["code"]
            time.sleep(0.5)
        console.error("Failed to fetch OTP", order_id=order_id, thread=thread_id)
        return None
