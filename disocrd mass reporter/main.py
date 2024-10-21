import os
import requests
import threading
import time
import json

class DiscordReporter:
    def __init__(self):
        self.GUILD_ID = input('[>] Guild ID: ')
        self.CHANNEL_ID = input('[>] Channel ID: ')
        self.MESSAGE_ID = input('[>] Message ID: ')
        self.REASON = self._get_reason()
        self.RESPONSES = {
            '401: Unauthorized': '[!] Invalid Discord token.',
            'Missing Access': '[!] Missing access to channel or guild.',
            'You need to verify your account in order to perform this action.': '[!] Unverified.'
        }
        self.sent = 0
        self.errors = 0
        self.running = True
        self.tokens = self._load_tokens()
        self.token_index = 0

    def _get_reason(self):
        reason = input(
            '\n[1] Illegal content\n'
            '[2] Harassment\n'
            '[3] Spam or phishing links\n'
            '[4] Self-harm\n'
            '[5] NSFW content\n\n'
            '[>] Reason: '
        )
        reasons = {
            '1': 0,
            '2': 1,
            '3': 2,
            '4': 3,
            '5': 4
        }
        return reasons.get(reason, None)

    def _load_tokens(self):
        tokens = []
        if os.path.exists('tokens.txt'):
            with open('tokens.txt', 'r') as f:
                tokens = [line.strip() for line in f if line.strip()]
        else:
            tokens = input('[>] Enter Discord tokens (separated by spaces): ').split()
            with open('tokens.txt', 'w') as f:
                for token in tokens:
                    f.write(token + '\n')
        return tokens

    def _check_server_status(self):
        try:
            response = requests.get('https://discord.com/api/v8/gateway')
            if response.status_code == 200:
                print('[+] Discord API is reachable.')
                return True
            else:
                print('[-] Discord API is unreachable. Status Code:', response.status_code)
                return False
        except requests.ConnectionError:
            print('[-] Failed to connect to Discord API.')
            return False

    def _reporter(self):
        while self.running:
            token = self.tokens[self.token_index]
            report = requests.post(
                'https://discordapp.com/api/v8/report', json={
                    'channel_id': self.CHANNEL_ID,
                    'message_id': self.MESSAGE_ID,
                    'guild_id': self.GUILD_ID,
                    'reason': self.REASON
                }, headers={
                    'Accept': '*/*',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'sv-SE',
                    'User-Agent': 'Discord/21295 CFNetwork/1128.0.1 Darwin/19.6.0',
                                       'Content-Type': 'application/json',
                    'Authorization': token
                }
            )
            if (status := report.status_code) == 201:
                self.sent += 1
                print(f'[!] Reported successfully. Total Reports Sent: {self.sent}')
            elif status in (401, 403):
                self.errors += 1
                print(self.RESPONSES.get(report.json().get('message'), f'[!] Error: {report.text} | Status Code: {status}'))
            else:
                self.errors += 1
                print(f'[!] Error: {report.text} | Status Code: {status}')

            self.token_index = (self.token_index + 1) % len(self.tokens)
            time.sleep(0.5)  

    def _multi_threading(self):
        threads = []
        for _ in range(len(self.tokens)):
            thread = threading.Thread(target=self._reporter)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def setup(self):
        if not self._check_server_status():
            return

        self._multi_threading()

if __name__ == '__main__':
    os.system('cls && title [Discord Reporter] - Main Menu')
    reporter = DiscordReporter()
    reporter.setup()
