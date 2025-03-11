import datetime
from colorama import Fore, Style, init
import os
import threading

print_lock = threading.Lock()
def safe_print(message):
    with print_lock:
        print(message)

class bcolors:
    BLACK        = '\033[30m'
    TIME         = '\033[90m'
    OKBLUE       = '\033[94m'
    DEEPBLUE     = '\033[34m'
    PURPLE       = '\033[95m'
    FAIL         = '\033[91m'
    SUCCESS      = '\033[92m'
    ENDC         = '\033[0m'
    HEADER       = '\033[95m'
    OKGREEN      = '\033[92m'
    WARNING      = '\033[93m'
    BOLD         = '\033[1m'
    UNDERLINE    = '\033[4m'
    DARKGREEN    = '\033[32m'
    PINK         = '\033[38;5;13m'
    TWITTERBLUE  = '\033[38;2;29;161;242m'
    CLOUDFLARE_ORANGE = '\033[38;2;243;128;32m' 

class Console:
    def __init__(self):
        init(autoreset=True)
        self.colors = {
            "green": Fore.GREEN,
            "red": Fore.RED,
            "yellow": Fore.YELLOW,
            "blue": Fore.BLUE,
            "magenta": Fore.MAGENTA,
            "cyan": Fore.CYAN,
            "white": Fore.WHITE,
            "black": Fore.BLACK,
            "reset": Style.RESET_ALL,
            "lightblack": Fore.LIGHTBLACK_EX,
            "lightred": Fore.LIGHTRED_EX,
            "lightgreen": Fore.LIGHTGREEN_EX,
            "lightyellow": Fore.LIGHTYELLOW_EX,
            "lightblue": Fore.LIGHTBLUE_EX,
            "lightmagenta": Fore.LIGHTMAGENTA_EX,
            "lightcyan": Fore.LIGHTCYAN_EX,
            "lightwhite": Fore.LIGHTWHITE_EX
        }
    
    def timestamp(self):
        return datetime.datetime.now().strftime("%H:%M:%S")
    
    def _format_message(self, level, level_color, message, thread_id=0, fields=None):
        if fields is None:
            fields = {}
        if thread_id and thread_id != 0:
            if 'thread' not in fields:
                fields['thread'] = thread_id

        ts = self.timestamp()
        base = f"{ts} {level_color}{level}{bcolors.ENDC} ● {message}"
        if fields:
            extra = f" {bcolors.TIME}→{bcolors.ENDC} "
            field_strs = []
            if 'thread' in fields:
                field_strs.append(f"thread: [{level_color}{fields['thread']}{bcolors.ENDC}]")
            for key, value in fields.items():
                if key != 'thread':
                    field_strs.append(f"{key}: [{level_color}{value}{bcolors.ENDC}]")
            extra += f" {bcolors.TIME}|{bcolors.ENDC} ".join(field_strs)
            return f"{base}{extra}"
        else:
            return base


    def error(self, thread_id=0, message="", **kwargs):
        msg = self._format_message("ERROR", bcolors.FAIL, message, thread_id, kwargs)
        safe_print(msg)
    
    def success(self, thread_id=0, message="", **kwargs):
        msg = self._format_message("SUCCESS", bcolors.SUCCESS, message, thread_id, kwargs)
        safe_print(msg)
    
    def sleep(self, thread_id=0, message="", **kwargs):
        msg = self._format_message("ZZZ", bcolors.WARNING, message, thread_id, kwargs)
        safe_print(msg)
    
    def otp(self, thread_id=0, message="", **kwargs):
        msg = self._format_message("OTP", bcolors.WARNING, message, thread_id, kwargs)
        safe_print(msg)
    
    def gen(self, thread_id=0, message="", **kwargs):
        msg = self._format_message("GEN", bcolors.PURPLE, message, thread_id, kwargs)
        safe_print(msg)
    
    def end(self, thread_id=0, message="", **kwargs):
        msg = self._format_message("END", bcolors.PURPLE, message, thread_id, kwargs)
        safe_print(msg)
    
    def login(self, thread_id=0, message="", **kwargs):
        msg = self._format_message("LOGIN", bcolors.SUCCESS, message, thread_id, kwargs)
        safe_print(msg)

    def cloudflare(self, thread_id=0, message="", **kwargs):
        msg = self._format_message("CLOUDFLARE", bcolors.CLOUDFLARE_ORANGE, message, thread_id, kwargs)
        safe_print(msg)

    def password(self, thread_id=0, message="", **kwargs):
        msg = self._format_message("PASSWORD", bcolors.WARNING, message, thread_id, kwargs)
        safe_print(msg)

    def linked(self, thread_id=0, message="", **kwargs):
        msg = self._format_message("LINK", bcolors.WARNING, message, thread_id, kwargs)
        safe_print(msg)

    def purchase(self, thread_id=0, message="", **kwargs):
        msg = self._format_message("PURCHASE", bcolors.OKGREEN, message, thread_id, kwargs)
        safe_print(msg)

    def twitter(self, thread_id=0, message="", **kwargs):
        msg = self._format_message("TWITTER", bcolors.TWITTERBLUE, message, thread_id, kwargs)
        safe_print(msg)


    def buy(self, thread_id=0, message="", **kwargs):
        msg = self._format_message("BUY", bcolors.SUCCESS, message, thread_id, kwargs)
        safe_print(msg)
    
    def inp(self, thread_id=0, message=""):
        prompt = f"{self.timestamp()} {bcolors.OKBLUE}INP{bcolors.ENDC} ● {message} "
        return input(prompt)
    
    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")
