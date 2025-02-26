from aiohttp import (
    ClientResponseError,
    ClientSession,
    ClientTimeout
)
from aiohttp_socks import ProxyConnector
from fake_useragent import FakeUserAgent
from datetime import datetime
from colorama import *
import asyncio, json, os, pytz

wib = pytz.timezone('Asia/Jakarta')

class Teneo:
    def __init__(self) -> None:
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
            "Origin": "https://dashboard.teneo.pro",
            "Referer": "https://dashboard.teneo.pro/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": FakeUserAgent().random
        }
        self.api_key = "OwAG3kib1ivOJG4Y0OCZ8lJETa6ypvsDtGmdhcjB"
        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(
            f"""
        {Fore.GREEN + Style.BRIGHT}Auto Ping {Fore.BLUE + Style.BRIGHT}Teneo - BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Join For More Scripts: {Fore.YELLOW + Style.BRIGHT} (https://t.me/D4rkCipherX)
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    def load_accounts(self):
        filename = "accounts.json"
        try:
            if not os.path.exists(filename):
                self.log(f"{Fore.RED}File {filename} Not Found.{Style.RESET_ALL}")
                return

            with open(filename, 'r') as file:
                data = json.load(file)
                if isinstance(data, list):
                    return data
                return []
        except json.JSONDecodeError:
            return []
    
    async def load_proxies(self, use_proxy_choice: int):
        filename = "proxy.txt"
        try:
            if use_proxy_choice == 1:
                async with ClientSession(timeout=ClientTimeout(total=30)) as session:
                    async with session.get("https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/all.txt") as response:
                        response.raise_for_status()
                        content = await response.text()
                        with open(filename, 'w') as f:
                            f.write(content)
                        self.proxies = content.splitlines()
            else:
                if not os.path.exists(filename):
                    self.log(f"{Fore.RED + Style.BRIGHT}File {filename} Not Found.{Style.RESET_ALL}")
                    return
                with open(filename, 'r') as f:
                    self.proxies = f.read().splitlines()
            
            if not self.proxies:
                self.log(f"{Fore.RED + Style.BRIGHT}No Proxies Found.{Style.RESET_ALL}")
                return

            self.log(
                f"{Fore.GREEN + Style.BRIGHT}Proxies Total  : {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(self.proxies)}{Style.RESET_ALL}"
            )
        
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Failed To Load Proxies: {e}{Style.RESET_ALL}")
            self.proxies = []

    def check_proxy_schemes(self, proxies):
        schemes = ["http://", "https://", "socks4://", "socks5://"]
        if any(proxies.startswith(scheme) for scheme in schemes):
            return proxies
        return f"http://{proxies}"

    def get_next_proxy_for_account(self, email):
        if email not in self.account_proxies:
            if not self.proxies:
                return None
            proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
            self.account_proxies[email] = proxy
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return self.account_proxies[email]

    def rotate_proxy_for_account(self, email):
        if not self.proxies:
            return None
        proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
        self.account_proxies[email] = proxy
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return proxy
    
    def mask_account(self, account):
        if "@" in account:
            local, domain = account.split('@', 1)
            mask_account = local[:3] + '*' * 3 + local[-3:]
            return f"{mask_account}@{domain}"
        
        mask_account = account[:3] + '*' * 3 + account[-3:]
        return mask_account

    def print_message(self, account, proxy, color, message):
        self.log(
            f"{Fore.CYAN + Style.BRIGHT}[ Account:{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} {self.mask_account(account)} {Style.RESET_ALL}"
            f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT} Proxy: {Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT}{proxy}{Style.RESET_ALL}"
            f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT}Status:{Style.RESET_ALL}"
            f"{color + Style.BRIGHT} {message} {Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT}]{Style.RESET_ALL}"
        )

    def print_question(self):
        while True:
            try:
                print("1. Run With Monosans Proxy")
                print("2. Run With Private Proxy")
                print("3. Run Without Proxy")
                choose = int(input("Choose [1/2/3] -> ").strip())

                if choose in [1, 2, 3]:
                    proxy_type = (
                        "Run With Monosans Proxy" if choose == 1 else 
                        "Run With Private Proxy" if choose == 2 else 
                        "Run Without Proxy"
                    )
                    print(f"{Fore.GREEN + Style.BRIGHT}{proxy_type} Selected.{Style.RESET_ALL}")
                    return choose
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter either 1, 2 or 3.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1, 2 or 3).{Style.RESET_ALL}")
    
    async def user_data(self, token: str, proxy=None):
        url = "https://auth.teneo.pro/api/user"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "X-Api-Key": self.api_key
        }
        connector = ProxyConnector.from_url(proxy) if proxy else None
        try:
            async with ClientSession(connector=connector, timeout=ClientTimeout(total=120)) as session:
                async with session.get(url=url, headers=headers) as response:
                    response.raise_for_status()
                    result = await response.json()
                    return result['email']
        except (Exception, ClientResponseError) as e:
            return self.print_message(token, proxy, Fore.RED, f"GET User Data Failed: {Fore.YELLOW + Style.BRIGHT}{str(e)}")
    
    async def campaigns_status(self, email: str, token: str, type: str, proxy=None, retries=5):
        url = f"https://api.teneo.pro/api/campaigns/{type}/status"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}"
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=120)) as session:
                    async with session.get(url=url, headers=headers) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue

                return self.print_message(email, proxy, Fore.RED, f"GET {type} Campaigns Data Failed: {Fore.YELLOW + Style.BRIGHT}{str(e)}")
    
    async def claim_campaigns(self, email: str, token: str, type: str, title: str, campaign_id: str, proxy=None, retries=5):
        url = f"https://api.teneo.pro/api/campaigns/{campaign_id}/claim"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "Content-Length": "0"
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=120)) as session:
                    async with session.post(url=url, headers=headers) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue

                return self.print_message(email, proxy, Fore.RED, f"Claim {title} {type} Campaigns Reward Failed: {Fore.YELLOW + Style.BRIGHT}{str(e)}")
    
    async def user_refferal(self, email: str, token: str, proxy=None, retries=5):
        url = "https://api.teneo.pro/api/users/referrals"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}"
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=120)) as session:
                    async with session.get(url=url, headers=headers) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue

                return self.print_message(email, proxy, Fore.RED, f"GET Refferal Data Failed: {Fore.YELLOW + Style.BRIGHT}{str(e)}")
    
    async def claim_refferal(self, email: str, token: str, refferal_email: str, referral_id: str, proxy=None, retries=5):
        url = "https://api.teneo.pro/api/users/referrals/claim"
        data = json.dumps({"referralId":referral_id})
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=120)) as session:
                    async with session.post(url=url, headers=headers, data=data) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue

                return self.print_message(email, proxy, Fore.RED, f"Claim Refferal {refferal_email} Reward Failed: {Fore.YELLOW + Style.BRIGHT}{str(e)}")
        
    async def connect_websocket(self, email: str, token: str, use_proxy: bool):
        wss_url = f"wss://secure.ws.teneo.pro/websocket?accessToken={token}&version=v0.2"
        headers = {
            "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
            "Cache-Control": "no-cache",
            "Connection": "Upgrade",
            "Host": "secure.ws.teneo.pro",
            "Origin": "chrome-extension://emcclcoaglgcpoognfiggmhnhgabppkm",
            "Pragma": "no-cache",
            "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
            "Sec-WebSocket-Key": "g0PDYtLWQOmaBE5upOBXew==",
            "Sec-WebSocket-Version": "13",
            "Upgrade": "websocket",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
        }
        connected = False

        while True:
            proxy = self.get_next_proxy_for_account(token) if use_proxy else None
            connector = ProxyConnector.from_url(proxy) if proxy else None
            session = ClientSession(connector=connector, timeout=ClientTimeout(total=300))
            try:
                async with session.ws_connect(wss_url, headers=headers) as wss:
                    
                    async def send_heartbeat_message():
                        while True:
                            await asyncio.sleep(10)
                            await wss.send_json({"type":"PING"})
                            print(
                                f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                                f"{Fore.BLUE + Style.BRIGHT}Node Connection Estabilished...{Style.RESET_ALL}",
                                end="\r",
                                flush=True
                            )

                    if not connected:
                        self.print_message(email, proxy, Fore.GREEN, "Websocket Is Connected")
                        connected = True
                        send_ping = asyncio.create_task(send_heartbeat_message())

                    while connected:
                        try:
                            response = await wss.receive_json()
                            if response.get("message") == "Connected successfully":
                                today_point = response.get("pointsToday", 0)
                                total_point = response.get("pointsTotal", 0)
                                self.print_message(
                                    email, proxy, Fore.GREEN, 
                                    f"Connected Successfully "
                                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                                    f"{Fore.CYAN + Style.BRIGHT} Earning: {Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT}Today {today_point} PTS{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT}Total {total_point} PTS{Style.RESET_ALL}"
                                )

                            elif response.get("message") == "Pulse from server":
                                today_point = response.get("pointsToday", 0)
                                total_point = response.get("pointsTotal", 0)
                                heartbeat_today = response.get("heartbeats", 0)
                                self.print_message(
                                    email, proxy, Fore.GREEN, 
                                    f"Pulse From Server"
                                    f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                                    f"{Fore.CYAN + Style.BRIGHT}Earning:{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} Today {today_point} PTS {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} Total {total_point} PTS {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                                    f"{Fore.CYAN + Style.BRIGHT} Heartbeat: {Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT}Today {heartbeat_today} HB{Style.RESET_ALL}"
                                )

                        except Exception as e:
                            self.print_message(email, proxy, Fore.YELLOW, f"Websocket Connection Closed: {Fore.RED + Style.BRIGHT}{str(e)}")
                            if send_ping:
                                send_ping.cancel()
                                try:
                                    await send_ping
                                except asyncio.CancelledError:
                                    self.print_message(email, proxy, Fore.YELLOW, f"Send Heartbeat Cancelled")

                            await asyncio.sleep(5)
                            connected = False
                            break

            except Exception as e:
                self.print_message(email, proxy, Fore.RED, f"Websocket Not Connected: {Fore.YELLOW + Style.BRIGHT}{str(e)}")
                self.rotate_proxy_for_account(email) if use_proxy else None
                await asyncio.sleep(5)

            except asyncio.CancelledError:
                self.print_message(email, proxy, Fore.YELLOW, "Websocket Closed")
                break
            finally:
                await session.close()

    async def process_claim_campaigns_reward(self, email: str, token: str, use_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(token) if use_proxy else None

            campaigns_type = ["heartbeat", "referral"]
            for type in campaigns_type:
                campaigns = await self.campaigns_status(email, token, type, proxy)

                if campaigns:
                    completed = False
                    
                    for campaign in campaigns:
                        if campaign:
                            campaign_id = campaign["id"]
                            title = campaign["title"]
                            reward = campaign["points_reward"]
                            status = campaign["status"]

                            if status == "claimable":
                                claim = await self.claim_campaigns(email, token, type, title, campaign_id, proxy)
                                if claim and claim.get("message") == "Reward claimed":
                                    self.print_message(email, proxy, Fore.WHITE, 
                                        f"Campaign {type} {title}"
                                        f"{Fore.GREEN+Style.BRIGHT} Is Claimed {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                                        f"{Fore.CYAN+Style.BRIGHT} Reward: {Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT}{reward} PTS{Style.RESET_ALL}"
                                    )

                        else:
                            completed = True

                    if completed:
                        self.print_message(email, proxy, Fore.GREEN, f"All Available {type} Campaigns Reward Is Claimed")

            await asyncio.sleep(24 * 60 * 60)

    async def process_claim_refferal_reward(self, email: str, token: str, use_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(token) if use_proxy else None

            refferal_lists = await self.user_refferal(email, token, proxy)
            if refferal_lists:
                completed = False

                unfiltered_refferals = refferal_lists.get("unfiltered", {}).get("refferals", [])
                filtered_refferals = refferal_lists.get("filtered", {}).get("refferals", [])
                
                for refferal in [unfiltered_refferals, filtered_refferals]:
                    if refferal:
                        refferal_id = refferal["id"]
                        refferal_email = refferal["inviteeEmail"]
                        reward = refferal["invitedPoints"]
                        can_claim = refferal["canClaim"]

                        if can_claim:
                            claim = await self.claim_refferal(email, token, refferal_email, refferal_id, proxy)
                            if claim and claim.get("message") == "Referral point claimed successfully":
                                self.print_message(email, proxy, Fore.WHITE, 
                                    f"Refferal {refferal_email}"
                                    f"{Fore.GREEN+Style.BRIGHT} Is Claimed {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                                    f"{Fore.CYAN+Style.BRIGHT} Reward: {Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT}{reward} PTS{Style.RESET_ALL}"
                                )

                    else:
                        completed = True

                if completed:
                    self.print_message(email, proxy, Fore.GREEN, f"All Available Refferal Reward Is Claimed")

            await asyncio.sleep(24 * 60 * 60)
            
    async def process_get_user_data(self, token: str, use_proxy: bool):
        proxy = self.get_next_proxy_for_account(token) if use_proxy else None
        email = None
        while email is None:
            email = await self.user_data(token, proxy)
            if not email:
                proxy = self.rotate_proxy_for_account(token) if use_proxy else None
                await asyncio.sleep(5)
                continue
            
            self.print_message(email, proxy, Fore.GREEN, "GET User Data Success")
            return email
        
    async def process_accounts(self, token: str, use_proxy: bool):
        email = await self.process_get_user_data(token, use_proxy)
        if email:

            tasks = []
            tasks.append(asyncio.create_task(self.process_claim_campaigns_reward(email, token, use_proxy)))
            tasks.append(asyncio.create_task(self.process_claim_refferal_reward(email, token, use_proxy)))
            tasks.append(asyncio.create_task(self.connect_websocket(email, token, use_proxy)))
            await asyncio.gather(*tasks)
        
    async def main(self):
        try:
            with open('tokens.txt', 'r') as file:
                tokens = [line.strip() for line in file if line.strip()]
            
            use_proxy_choice = self.print_question()

            use_proxy = False
            if use_proxy_choice in [1, 2]:
                use_proxy = True

            self.clear_terminal()
            self.welcome()
            self.log(
                f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(tokens)}{Style.RESET_ALL}"
            )

            if use_proxy:
                await self.load_proxies(use_proxy_choice)

            self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)

            while True:
                tasks = []
                for token in tokens:
                    if token:
                        tasks.append(asyncio.create_task(self.process_accounts(token, use_proxy)))

                await asyncio.gather(*tasks)
                await asyncio.sleep(10)

        except FileNotFoundError:
            self.log(f"{Fore.RED}File 'tokens.txt' Not Found.{Style.RESET_ALL}")
            return
        except Exception as e:
            self.log(f"{Fore.RED+Style.BRIGHT}Error: {e}{Style.RESET_ALL}")
            raise e

if __name__ == "__main__":
    try:
        bot = Teneo()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.RED + Style.BRIGHT}[ EXIT ] Teneo - BOT{Style.RESET_ALL}                                       "                              
        )
