import json, pyotp, base64
import requests
from handlers import totphandler as totphand
from email.utils import parsedate_to_datetime
from random import randrange
import random

class Token:
    def __init__(self):
        self.tokenUrl = "https://open.spotify.com/api/token"
        self.serverTimeUrl = "https://open.spotify.com/"
        self.sp_dc = self.get_spdc_cookies()

    def get_spdc_cookies(self):
        with open("settings.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data['sp_dc']

    def fetch_random_useragent(self):
        browser = random.choice(['chrome', 'firefox', 'edge', 'safari'])

        if browser == 'chrome':
            os_choice = random.choice(['mac', 'windows'])
            if os_choice == 'mac':
                return (
                    f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_{random.randrange(11, 15)}_{random.randrange(4, 9)}) "
                    f"AppleWebKit/{random.randrange(530, 537)}.{random.randrange(30, 37)} (KHTML, like Gecko) "
                    f"Chrome/{random.randrange(80, 105)}.0.{random.randrange(3000, 4500)}.{random.randrange(60, 125)} "
                    f"Safari/{random.randrange(530, 537)}.{random.randrange(30, 36)}"
                )
            else:
                chrome_version = random.randint(80, 105)
                build = random.randint(3000, 4500)
                patch = random.randint(60, 125)
                return (
                    f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    f"AppleWebKit/537.36 (KHTML, like Gecko) "
                    f"Chrome/{chrome_version}.0.{build}.{patch} Safari/537.36"
                )

        elif browser == 'firefox':
            os_choice = random.choice(['windows', 'mac', 'linux'])
            version = random.randint(90, 110)
            if os_choice == 'windows':
                return (
                    f"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:{version}.0) "
                    f"Gecko/20100101 Firefox/{version}.0"
                )
            elif os_choice == 'mac':
                return (
                    f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_{random.randrange(11, 15)}_{random.randrange(0, 10)}; rv:{version}.0) "
                    f"Gecko/20100101 Firefox/{version}.0"
                )
            else:
                return (
                    f"Mozilla/5.0 (X11; Linux x86_64; rv:{version}.0) "
                    f"Gecko/20100101 Firefox/{version}.0"
                )

        elif browser == 'edge':
            os_choice = random.choice(['windows', 'mac'])
            chrome_version = random.randint(80, 105)
            build = random.randint(3000, 4500)
            patch = random.randint(60, 125)
            version_str = f"{chrome_version}.0.{build}.{patch}"
            if os_choice == 'windows':
                return (
                    f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    f"AppleWebKit/537.36 (KHTML, like Gecko) "
                    f"Chrome/{version_str} Safari/537.36 Edg/{version_str}"
                )
            else:
                return (
                    f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_{random.randrange(11, 15)}_{random.randrange(0, 10)}) "
                    f"AppleWebKit/605.1.15 (KHTML, like Gecko) "
                    f"Version/{random.randint(13, 16)}.0 Safari/605.1.15 Edg/{version_str}"
                )

        elif browser == 'safari':
            os_choice = 'mac'
            if os_choice == 'mac':
                mac_major = random.randrange(11, 16)
                mac_minor = random.randrange(0, 10)
                webkit_major = random.randint(600, 610)
                webkit_minor = random.randint(1, 20)
                webkit_patch = random.randint(1, 20)
                safari_version = random.randint(13, 16)
                return (
                    f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_{mac_major}_{mac_minor}) "
                    f"AppleWebKit/{webkit_major}.{webkit_minor}.{webkit_patch} (KHTML, like Gecko) "
                    f"Version/{safari_version}.0 Safari/{webkit_major}.{webkit_minor}.{webkit_patch}"
                )
            else:
                return ""
        else:
            return ""
        
    def fetch_server_time(self, userAgent):
        headers = {
            "User-Agent": userAgent,
            "Accept": "*/*",
        }
        response = requests.head(self.serverTimeUrl, headers=headers)
        response.raise_for_status()
        date_hdr = response.headers.get("Date")
        if not date_hdr:
            raise RuntimeError("Missing 'Date' header")
        return int(parsedate_to_datetime(date_hdr).timestamp())


    def generate_totp(self):
        totp_version, secret_bytes = totphand.fetch_new_secret()
        transformed = [e ^ ((t % 33) + 9) for t, e in enumerate(secret_bytes)]
        joined = "".join(str(num) for num in transformed)
        hex_str = joined.encode().hex()
        secret = base64.b32encode(bytes.fromhex(hex_str)).decode().rstrip("=")
        return pyotp.TOTP(secret, digits=6, interval=30), totp_version
        
    def get_token(self):
        userAgent = self.fetch_random_useragent()
        server_time = self.fetch_server_time(userAgent)
        totp, totp_version = self.generate_totp()
        totp_value = totp.at(server_time)

        params = {
            "reason": "transport",
            "productType": "web-player",
            "totp": totp_value,
            "totpServer": totp_value,
            "totpVer": totp_version
        }

        headers = {
        "User-Agent": userAgent,
        "Accept": "application/json",
        "Referer": "https://open.spotify.com/",
        "App-Platform": "WebPlayer",
        "Cookie": f"sp_dc={self.sp_dc}",
    }

        response = requests.get(self.tokenUrl, params=params, headers=headers)
        if response.status_code == 200:
            response = response.json()
            return response['accessToken']