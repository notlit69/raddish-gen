import os
import requests
from colorama import Fore
import json
import threading
from datetime import datetime
from console import Console

console = Console()
threeMonths = 0
oneMonth = 0
linked = 0

lock = threading.Lock()

def linkpromo(promo):
    global oneMonth, threeMonths, linked
    inputTokens = "Input/tokens.txt"
    outputFolder = "Output/Linked"
    outputTokens = os.path.join(outputFolder, "tokens.txt")
    outputPromos = os.path.join(outputFolder, "promos.txt")
    outputCombined = os.path.join(outputFolder, "combined.txt")
    outputUsedPromos = os.path.join(outputFolder, "usedpromos.txt")

    def fileExithm(file_path):
        if not os.path.exists(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            open(file_path, 'w').close()

    def loadLines(file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return [line.strip() for line in file.readlines() if line.strip()]
        return []

    def update_file(file_path, lines):
        with open(file_path, 'w') as file:
            file.writelines(line + '\n' for line in lines)

    def writeFile(file_path, content):
        fileExithm(file_path)
        with open(file_path, 'a') as file:
            file.write(content + '\n')

    def time_right_now():
        return datetime.now().strftime("%I:%M %p")

    fileExithm(outputTokens)
    fileExithm(outputPromos)
    fileExithm(outputCombined)
    fileExithm(outputUsedPromos)

    with lock:
        tokens = loadLines(inputTokens)
        if not tokens:
            writeFile("Output/promos.txt", promo)
            return
        token_line = tokens.pop(0)
        update_file(inputTokens, tokens)

    token = token_line.split(":")[-1]

    try:
        promo_id, promo_jwt = promo.split('/')[5:7]
        promo_url = f"https://discord.com/api/v9/entitlements/partner-promotions/{promo_id}"
        headers = {
            "authorization": token,
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://discord.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        }

        response = requests.post(promo_url, headers=headers, json={"jwt": promo_jwt})

        if response.status_code == 200:
            promo_data = response.json()
            promo_redemption_id = promo_data.get("code")

            checkPromoType = "3 Months" if promo_id == "1310745123109339258" else "1 Month" if promo_id == "1310745070936391821" else "Unknown"
            if checkPromoType == "3 Months":
                threeMonths += 1
            elif checkPromoType == "1 Month":
                oneMonth += 1

            if promo_redemption_id:
                linked += 1
                console.linked(f"Successfully linked token {Fore.LIGHTBLACK_EX}token:{Fore.RESET} {token[:30]}... {Fore.LIGHTBLACK_EX}promo:{Fore.RESET} {promo_redemption_id} {Fore.LIGHTBLACK_EX}duration:{Fore.RESET} {checkPromoType}")
                writeFile(outputPromos, f"https://promos.discord.gg/{promo_redemption_id}")
                writeFile(outputTokens, token_line)
                writeFile(outputCombined, f"{token_line}|https://promos.discord.gg/{promo_redemption_id}")
                writeFile(outputUsedPromos, promo)
        else:
            console.error(f"Error linking token {Fore.LIGHTBLACK_EX}token:{Fore.RESET} {token[:30]}... {Fore.LIGHTBLACK_EX}error:{Fore.RESET} {response.text}")
            writeFile("Output/promos.txt", promo)



    except Exception as e:
        console.error(f"Error linking token {Fore.LIGHTBLACK_EX}token:{Fore.RESET} {token[:30]}... {Fore.LIGHTBLACK_EX}error:{Fore.RESET} {e}")
        writeFile("Output/promos.txt", promo)
