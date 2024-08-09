import requests
import json
import time
import os
import random
import string

# URL for the API endpoint
url = 'https://codes.thisisnotawebsitedotcom.com/'

# Base headers
base_headers = {
    'accept': '*/*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'Referer': 'https://thisisnotawebsitedotcom.com/'
}

class AdaptiveDelay:
    def __init__(self, initial_delay=0.2, min_delay=0.18, max_delay=0.35, increase_factor=1.05, decrease_factor=0.95):
        self.current_delay = initial_delay
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.increase_factor = increase_factor
        self.decrease_factor = decrease_factor
        self.success_count = 0
        self.success_threshold = 50
        self.last_successful_delay = initial_delay

    def wait(self):
        time.sleep(self.current_delay)

    def increase_delay(self):
        self.current_delay = min(self.current_delay * self.increase_factor, self.max_delay)
        self.success_count = 0
        self.min_delay = self.last_successful_delay

    def decrease_delay(self):
        self.current_delay = max(self.current_delay * self.decrease_factor, self.min_delay)

    def request_success(self):
        self.success_count += 1
        self.last_successful_delay = self.current_delay
        if self.success_count >= self.success_threshold:
            self.decrease_delay()
            self.success_count = 0

    def request_failed(self):
        self.increase_delay()
        self.success_count = 0

def generate_boundary():
    return '----WebKitFormBoundary' + ''.join(random.choices(string.ascii_letters + string.digits, k=16))

def send_request(session, code, adaptive_delay, retries=3):
    boundary = generate_boundary()
    headers = {
        **base_headers,
        'content-type': f'multipart/form-data; boundary={boundary}',
    }
    data = f'--{boundary}\r\nContent-Disposition: form-data; name="code"\r\n\r\n{code}\r\n--{boundary}--\r\n'
    
    for attempt in range(retries):
        try:
            adaptive_delay.wait()
            response = session.post(url, headers=headers, data=data, allow_redirects=False)
            
            if response.status_code == 200:
                save_successful_result(code, response.text)
                print(f"Success with code: {code}")
                adaptive_delay.request_success()
                return True
            elif response.status_code == 429:
                print(f"Rate limited. Increasing delay. Current delay: {adaptive_delay.current_delay:.2f} seconds")
                adaptive_delay.request_failed()
            else:
                print(f"Failed with code: {code}. Status: {response.status_code}")
                adaptive_delay.request_success()
                return False
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            adaptive_delay.request_failed()
    
    print(f"Max retries reached for code: {code}")
    return False

def save_successful_result(code, response_text):
    try:
        with open('successful_codes.json', 'r+') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append({
        "code": code,
        "response": response_text
    })

    with open('successful_codes.json', 'w') as f:
        json.dump(data, f, indent=2)

def load_word_list(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def save_progress(current_word):
    with open('progress.json', 'w') as f:
        json.dump({"current_word": current_word}, f)

def load_progress():
    try:
        with open('progress.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def main():
    word_list_path = 'sanitized_wordlist2.txt'  # Replace with your actual path
    adaptive_delay = AdaptiveDelay()

    words = load_word_list(word_list_path)
    progress = load_progress()

    # Handle cases where progress might be None or missing 'current_word' key
    if progress and 'current_word' in progress:
        start_word = progress['current_word']
        start_index = words.index(start_word) if start_word in words else 0
    else:
        start_word = None
        start_index = 0

    print(f"Starting from word: {words[start_index]}")

    with requests.Session() as session:
        for word in words[start_index:]:
            save_progress(word)
            send_request(session, word, adaptive_delay)
            print(f"Current delay: {adaptive_delay.current_delay:.2f} seconds")

    # If we've completed all words, remove the progress file
    if os.path.exists('progress.json'):
        os.remove('progress.json')
        print("Completed all words. Progress file removed.")

if __name__ == "__main__":
    main()
