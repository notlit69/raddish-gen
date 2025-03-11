from twocaptcha import TwoCaptcha
import capsolver
import requests
import json
from console import Console
from colorama import Fore
from capmonster_python import TurnstileTask

console = Console()
cfSolved = 0

with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    solver_config = config.get("Solver", {})
    api_custom = solver_config.get("CustomCFSolver")
    api_key_2captcha = solver_config.get("2Captcha")
    api_key_capsolver = solver_config.get("CapSolver")
    api_key_capmonster = solver_config.get("CapMonster")

def twocaptcha_solver(thread_id):
    global cfSolved

    solver = TwoCaptcha(api_key_2captcha)
    captcha_token = solver.turnstile(
        sitekey='0x4AAAAAAACELUBpqiwktdQ9',
        url='https://streamlabs.com/slid/signup',
        userAgent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    )
    token = captcha_token['code']
    console.cloudflare(thread_id, "Solved cloudflare", token=f"{token[:30]}...")
    cfSolved += 1
    return token

def capsolver_solver(thread_id):
    global cfSolved

    capsolver.api_key = api_key_capsolver
    captcha_token = capsolver.solve({
        "type": "AntiTurnstileTaskProxyLess",
        "websiteURL": "https://streamlabs.com/slid/signup",
        "websiteKey": "0x4AAAAAAACELUBpqiwktdQ9",
        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0"
    })
    token = captcha_token['token']
    console.cloudflare(thread_id, "Solved cloudflare", token=f"{token[:30]}...")
    cfSolved += 1
    return token

def capmonster_solver(thread_id):
    global cfSolved
    
    solver = TurnstileTask(api_key_capmonster)
    task_id = solver.create_task("https://streamlabs.com/slid/signup", "0x4AAAAAAACELUBpqiwktdQ9")

    if not task_id:
        console.error(thread_id, "Failed to create CapMonster task!")
        return None

    result = solver.join_task_result(task_id)

    if not result or "token" not in result:
        console.error(thread_id, "CapMonster did not return a valid token!", error=result)
        return None

    token = result["token"]
    console.cloudflare(thread_id, "Solved cloudflare", token=f"{str(token)[:30]}...")
    cfSolved += 1
    return token

def solve_captcha(thread_id):
    if api_key_2captcha:
        return twocaptcha_solver(thread_id)
    elif api_key_capsolver:
        return capsolver_solver(thread_id)
    elif api_key_capmonster:
        return capmonster_solver(thread_id)
    else:
        console.error(thread_id, "No valid captcha solver API key found in config.json")
        return None
