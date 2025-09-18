import threading
import base64
import os
import time
import re
import requests
import socket
import sys
from time import sleep
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import json
from collections import Counter, deque, defaultdict
from urllib.parse import urlparse, parse_qs
import random
import math
import hashlib
import platform
import subprocess
import statistics
import string
import urllib.parse

# Check và cài đặt các thư viện cần thiết từ banner.py
try:
    from faker import Faker
    from requests import session
    from colorama import Fore, Style, init
    import pystyle
    init(autoreset=True) # Thêm từ vtd8.py
except ImportError:
    print('__Đang cài đặt thư viện, vui lòng chờ...__')
    os.system("pip install faker requests colorama bs4 pystyle rich numpy")
    os.system("pip3 install requests pysocks")
    print('__Cài đặt hoàn tất, vui lòng chạy lại Tool__')
    sys.exit()

# Check numpy từ vtd8.py
try:
    import numpy as np
except ImportError:
    np = None

# =====================================================================================
# PHẦN 2: MÃ NGUỒN TỪ FILE banner.py (XÁC THỰC)
# =====================================================================================

# CONFIGURATION FOR VIP KEY
VIP_KEY_URL = "https://raw.githubusercontent.com/DUONGKP2401/KEY-VIP.txt/main/KEY-VIP.txt"
VIP_CACHE_FILE = 'vip_cache.json'

# Encrypt and decrypt data using base64
def encrypt_data(data):
    return base64.b64encode(data.encode()).decode()

def decrypt_data(encrypted_data):
    return base64.b64decode(encrypted_data.encode()).decode()

# Colors for display
xnhac = "\033[1;36m"
do = "\033[1;31m"
luc = "\033[1;32m"
vang = "\033[1;33m"
xduong = "\033[1;34m"
hong = "\033[1;35m"
trang = "\033[1;39m"
end = '\033[0m'

# Đổi tên hàm banner của file banner.py để tránh xung đột
def authentication_banner():
    os.system("cls" if os.name == "nt" else "clear")
    banner_text = f"""
{luc}████████╗ ██████╗░░ ██╗░░██╗░
{luc}╚══██╔══╝ ██╔══██╗░ ██║██╔╝░░
{luc}░░░██║░░░ ██║░░██║░ █████╔╝░░
{luc}░░░██║░░░ ██║░░██║░ ██╔═██╗░░
{luc}░░░██║░░░ ██║░░██║░ ██║░╚██╗░
{luc}░░░╚═╝░░░ ╚█████╔╝░ ╚═╝░░╚═╝░
{trang}══════════════════════════

{vang}Admin: DUONG PHUNG
{vang}Nhóm Zalo: https://zalo.me/g/ddxsyp497
{vang}Tele: @tankeko12
{trang}══════════════════════════
"""
    for char in banner_text:
        sys.stdout.write(char)
        sys.stdout.flush()
        sleep(0.0001)

# DEVICE ID AND IP ADDRESS FUNCTIONS
def get_device_id():
    """Generates a stable device ID based on CPU information."""
    system = platform.system()
    try:
        if system == "Windows":
            cpu_info = subprocess.check_output('wmic cpu get ProcessorId', shell=True, text=True, stderr=subprocess.DEVNULL)
            cpu_info = ''.join(line.strip() for line in cpu_info.splitlines() if line.strip() and "ProcessorId" not in line)
        else:
            try:
                cpu_info = subprocess.check_output("cat /proc/cpuinfo", shell=True, text=True)
            except:
                cpu_info = platform.processor()
        if not cpu_info:
            cpu_info = platform.processor()
    except Exception:
        cpu_info = "Unknown"

    hash_hex = hashlib.sha256(cpu_info.encode()).hexdigest()
    only_digits = re.sub(r'\D', '', hash_hex)
    if len(only_digits) < 16:
        only_digits = (only_digits * 3)[:16]
    
    return f"DEVICE-{only_digits[:16]}"

def get_ip_address():
    """Gets the user's public IP address."""
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        ip_data = response.json()
        return ip_data.get('ip')
    except Exception as e:
        print(f"{do}Lỗi khi lấy địa chỉ IP: {e}{trang}")
        return None

def display_machine_info(ip_address, device_id):
    """Displays the banner, IP address, and Device ID."""
    authentication_banner() # Gọi hàm banner đã đổi tên
    if ip_address:
        print(f"{trang}[{do}<>{trang}] {do}Địa chỉ IP: {vang}{ip_address}{trang}")
    else:
        print(f"{do}Không thể lấy địa chỉ IP của thiết bị.{trang}")
    
    if device_id:
        print(f"{trang}[{do}<>{trang}] {do}Mã Máy: {vang}{device_id}{trang}")
    else:
        print(f"{do}Không thể lấy Mã Máy của thiết bị.{trang}")


# FREE KEY HANDLING FUNCTIONS
def luu_thong_tin_ip(ip, key, expiration_date):
    """Saves free key information to a json file."""
    data = {ip: {'key': key, 'expiration_date': expiration_date.isoformat()}}
    encrypted_data = encrypt_data(json.dumps(data))
    with open('ip_key.json', 'w') as file:
        file.write(encrypted_data)

def tai_thong_tin_ip():
    """Loads free key information from the json file."""
    try:
        with open('ip_key.json', 'r') as file:
            encrypted_data = file.read()
        return json.loads(decrypt_data(encrypted_data))
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def kiem_tra_ip(ip):
    """Checks for a saved free key for the current IP."""
    data = tai_thong_tin_ip()
    if data and ip in data:
        try:
            expiration_date = datetime.fromisoformat(data[ip]['expiration_date'])
            if expiration_date > datetime.now():
                return data[ip]['key']
        except (ValueError, KeyError):
            return None
    return None

def generate_key_and_url(ip_address):
    """Creates a free key and a URL to bypass the link."""
    ngay = int(datetime.now().day)
    key1 = str(ngay * 27 + 27)
    ip_numbers = ''.join(filter(str.isdigit, ip_address))
    key = f'VTD8{key1}{ip_numbers}'
    expiration_date = datetime.now().replace(hour=23, minute=59, second=0, microsecond=0)
    url = f'https://keyvtdv8.blogspot.com/2025/09/key-vtdv8_18.html?m={key}'
    return url, key, expiration_date

def get_shortened_link_phu(url):
    """Shortens the link to get the free key."""
    try:
        token = "6725c7b50c661e3428736919"
        api_url = f"https://link4m.co/api-shorten/v2?api={token}&url={url}"
        response = requests.get(api_url, timeout=5)
        if response.status_code == 200:
            return response.json()
        return {"status": "error", "message": "Không thể kết nối đến dịch vụ rút gọn URL."}
    except Exception as e:
        return {"status": "error", "message": f"Lỗi khi rút gọn URL: {e}"}

def process_free_key(ip_address):
    """Handles the entire process of obtaining a free key."""
    url, key, expiration_date = generate_key_and_url(ip_address)
    
    with ThreadPoolExecutor(max_workers=1) as executor:
        yeumoney_future = executor.submit(get_shortened_link_phu, url)
        yeumoney_data = yeumoney_future.result()

    if yeumoney_data and yeumoney_data.get('status') == "error":
        print(yeumoney_data.get('message'))
        return False
    
    link_key_yeumoney = yeumoney_data.get('shortenedUrl')
    print(f'{trang}[{do}<>{trang}] {hong}Link Để Vượt Key Là {xnhac}: {link_key_yeumoney}{trang}')

    while True:
        keynhap = input(f'{trang}[{do}<>{trang}] {vang}Key Đã Vượt Là: {luc}')
        if keynhap == key:
            print(f'{luc}Key Đúng! Mời Bạn Dùng Tool{trang}')
            sleep(2)
            luu_thong_tin_ip(ip_address, keynhap, expiration_date)
            return True
        else:
            print(f'{trang}[{do}<>{trang}] {hong}Key Sai! Vui Lòng Vượt Lại Link {xnhac}: {link_key_yeumoney}{trang}')


# VIP KEY HANDLING FUNCTIONS
def save_vip_key_info(device_id, key, expiration_date_str):
    """Saves VIP key information to a local cache file."""
    data = {'device_id': device_id, 'key': key, 'expiration_date': expiration_date_str}
    encrypted_data = encrypt_data(json.dumps(data))
    with open(VIP_CACHE_FILE, 'w') as file:
        file.write(encrypted_data)
    print(f"{luc}Đã lưu thông tin Key VIP cho lần đăng nhập sau.{trang}")

def load_vip_key_info():
    """Loads VIP key information from the local cache file."""
    try:
        with open(VIP_CACHE_FILE, 'r') as file:
            encrypted_data = file.read()
        return json.loads(decrypt_data(encrypted_data))
    except (FileNotFoundError, json.JSONDecodeError, TypeError):
        return None

def display_remaining_time(expiry_date_str):
    """Calculates and displays the remaining time for a VIP key."""
    try:
        expiry_date = datetime.strptime(expiry_date_str, '%d/%m/%Y').replace(hour=23, minute=59, second=59)
        now = datetime.now()
        
        if expiry_date > now:
            delta = expiry_date - now
            days = delta.days
            hours, remainder = divmod(delta.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            print(f"{xnhac}Key VIP của bạn còn lại: {luc}{days} ngày, {hours} giờ, {minutes} phút.{trang}")
        else:
            print(f"{do}Key VIP của bạn đã hết hạn.{trang}")
    except ValueError:
        print(f"{vang}Không thể xác định ngày hết hạn của key.{trang}")

def check_vip_key(machine_id, user_key):
    """Checks the VIP key from the URL on GitHub."""
    print(f"{vang}Đang kiểm tra Key VIP...{trang}")
    try:
        response = requests.get(VIP_KEY_URL, timeout=10)
        if response.status_code != 200:
            print(f"{do}Lỗi: Không thể tải danh sách key (Status code: {response.status_code}).{trang}")
            return 'error', None

        key_list = response.text.strip().split('\n')
        for line in key_list:
            parts = line.strip().split('|')
            if len(parts) >= 4:
                key_ma_may, key_value, _, key_ngay_het_han = parts
                
                if key_ma_may == machine_id and key_value == user_key:
                    try:
                        expiry_date = datetime.strptime(key_ngay_het_han, '%d/%m/%Y')
                        if expiry_date.date() >= datetime.now().date():
                            return 'valid', key_ngay_het_han
                        else:
                            return 'expired', None
                    except ValueError:
                        continue
        return 'not_found', None
    except requests.exceptions.RequestException as e:
        print(f"{do}Lỗi kết nối đến server key: {e}{trang}")
        return 'error', None

# MAIN AUTHENTICATION FLOW
def main_authentication():
    ip_address = get_ip_address()
    device_id = get_device_id()
    display_machine_info(ip_address, device_id)

    if not ip_address or not device_id:
        print(f"{do}Không thể lấy thông tin thiết bị cần thiết. Vui lòng kiểm tra kết nối mạng.{trang}")
        return False

    cached_vip_info = load_vip_key_info()
    if cached_vip_info and cached_vip_info.get('device_id') == device_id:
        try:
            expiry_date = datetime.strptime(cached_vip_info['expiration_date'], '%d/%m/%Y')
            if expiry_date.date() >= datetime.now().date():
                print(f"{luc}Đã tìm thấy Key VIP hợp lệ, tự động đăng nhập...{trang}")
                display_remaining_time(cached_vip_info['expiration_date'])
                sleep(3)
                return True
            else:
                print(f"{vang}Key VIP đã lưu đã hết hạn. Vui lòng lấy hoặc nhập key mới.{trang}")
        except (ValueError, KeyError):
            print(f"{do}Lỗi file lưu key. Vui lòng nhập lại key.{trang}")

    if kiem_tra_ip(ip_address):
        print(f"{trang}[{do}<>{trang}] {hong}Key free hôm nay vẫn còn hạn. Mời bạn dùng tool...{trang}")
        time.sleep(2)
        return True

    while True:
        print(f"{trang}========== {vang}MENU LỰA CHỌN{trang} ==========")
        print(f"{trang}[{luc}1{trang}] {xduong}Nhập Key VIP{trang}")
        print(f"{trang}[{luc}2{trang}] {xduong}Lấy Key Free (Dùng trong ngày){trang}")
        print(f"{trang}======================================")

        try:
            choice = input(f"{trang}[{do}<>{trang}] {xduong}Nhập lựa chọn của bạn: {trang}")
            print(f"{trang}═══════════════════════════════════")

            if choice == '1':
                vip_key_input = input(f'{trang}[{do}<>{trang}] {vang}Vui lòng nhập Key VIP: {luc}')
                status, expiry_date_str = check_vip_key(device_id, vip_key_input)
                
                if status == 'valid':
                    print(f"{luc}Xác thực Key VIP thành công!{trang}")
                    save_vip_key_info(device_id, vip_key_input, expiry_date_str)
                    display_remaining_time(expiry_date_str)
                    sleep(3)
                    return True
                elif status == 'expired':
                    print(f"{do}Key VIP của bạn đã hết hạn. Vui lòng liên hệ admin.{trang}")
                elif status == 'not_found':
                    print(f"{do}Key VIP không hợp lệ hoặc không tồn tại cho mã máy này.{trang}")
                else:
                    print(f"{do}Đã xảy ra lỗi trong quá trình xác thực. Vui lòng thử lại.{trang}")
                sleep(2)

            elif choice == '2':
                return process_free_key(ip_address)
            
            else:
                print(f"{vang}Lựa chọn không hợp lệ, vui lòng nhập 1 hoặc 2.{trang}")

        except (KeyboardInterrupt):
            print(f"\n{trang}[{do}<>{trang}] {do}Cảm ơn bạn đã dùng Tool !!!{trang}")
            sys.exit()

# =====================================================================================
# PHẦN 3: MÃ NGUỒN TỪ FILE vtd8.py (TOOL GAME)
# =====================================================================================
NV = {
    1: 'Bậc thầy tấn công',
    2: 'Quyền sắt',
    3: 'Thợ lặn sâu',
    4: 'Cơn lốc sân cỏ',
    5: 'Hiệp sĩ phi nhanh',
    6: 'Vua home run'
}

class SmartAnalyzer:
    def __init__(self):
        self.history_data = deque(maxlen=200)
        self.pattern_memory = {}
        self.frequency_tracker = {i: 0 for i in range(1, 7)}
        self.sequence_patterns = deque(maxlen=50)
        self.hot_cold_tracker = {i: {'hot': 0, 'cold': 0} for i in range(1, 7)}
        self.winning_strategies = []
        
    def add_result(self, result):
        self.history_data.append(result)
        self.frequency_tracker[result] += 1
        self.sequence_patterns.append(result)
        self._update_hot_cold(result)
        
    def _update_hot_cold(self, result):
        for num in range(1, 7):
            if num == result:
                self.hot_cold_tracker[num]['hot'] += 1
                self.hot_cold_tracker[num]['cold'] = 0
            else:
                self.hot_cold_tracker[num]['cold'] += 1
                
    def analyze_patterns(self):
        if len(self.history_data) < 10:
            return None, None
        patterns = {}
        data_list = list(self.history_data)
        for cycle_len in range(2, min(20, len(data_list))):
            pattern_score = 0
            for i in range(cycle_len, len(data_list)):
                if data_list[i] == data_list[i - cycle_len]:
                    pattern_score += 1
            if len(data_list) > cycle_len:
                patterns[f'cycle_{cycle_len}'] = pattern_score / (len(data_list) - cycle_len)
            else:
                patterns[f'cycle_{cycle_len}'] = 0
        consecutive_patterns = {}
        for i in range(1, len(data_list)):
            pair = (data_list[i-1], data_list[i])
            consecutive_patterns[pair] = consecutive_patterns.get(pair, 0) + 1
        return patterns, consecutive_patterns
        
    def calculate_probability_matrix(self):
        if len(self.history_data) < 20:
            return {i: 1/6 for i in range(1, 7)}
        data_list = list(self.history_data)
        frequencies = Counter(data_list)
        total = len(data_list)
        weighted_probs = {}
        for num in range(1, 7):
            base_prob = frequencies.get(num, 0) / total
            recent_weight = 0
            recent_count = min(20, len(data_list))
            if recent_count > 0:
                for i in range(-recent_count, 0):
                    if data_list[i] == num:
                        recent_weight += (recent_count + i) / recent_count
                weighted_probs[num] = base_prob * 0.7 + (recent_weight / recent_count) * 0.3
            else:
                weighted_probs[num] = base_prob
        return weighted_probs
        
    def predict_next_winner(self, last_10_results, last_100_stats):
        if len(self.history_data) < 10:
            return self._safe_fallback_choice(last_10_results)
        predictions = self._multi_factor_analysis(last_10_results, last_100_stats)
        avoid_numbers = set(last_10_results[:3])
        best_choice = None
        best_score = -1
        for num, score in predictions.items():
            if num not in avoid_numbers and score > best_score:
                best_choice = num
                best_score = score
        return best_choice if best_choice else self._safe_fallback_choice(last_10_results)
        
    def _multi_factor_analysis(self, last_10_results, last_100_stats):
        scores = {i: 0 for i in range(1, 7)}
        total_100 = sum(last_100_stats) if sum(last_100_stats) > 0 else 6
        for i, count in enumerate(last_100_stats, 1):
            relative_freq = count / total_100
            if relative_freq < 0.12: scores[i] += 80
            elif relative_freq < 0.15: scores[i] += 60
            elif relative_freq < 0.18: scores[i] += 40
            else: scores[i] += 5
        recent_5 = last_10_results[:5] if len(last_10_results) >= 5 else last_10_results
        recent_counter = Counter(recent_5)
        for num, count in recent_counter.items():
            if count >= 3: scores[num] -= 100
            elif count == 2: scores[num] -= 60
            elif count == 1: scores[num] -= 25
        if len(last_10_results) >= 1:
            last_winner = last_10_results[0]
            scores[last_winner] -= 200
            if len(last_10_results) >= 2 and last_10_results[0] == last_10_results[1]:
                scores[last_winner] -= 100
            if len(last_10_results) >= 4:
                recent_4 = last_10_results[:4]
                for num in range(1, 7):
                    if recent_4.count(num) >= 3:
                        scores[num] -= 150
        if len(self.history_data) >= 10:
            patterns, consecutive = self.analyze_patterns()
            if consecutive:
                last_num = last_10_results[0] if last_10_results else 0
                for (prev, curr), freq in consecutive.items():
                    if prev == last_num and freq > 1:
                        scores[curr] -= 20
        for num in range(1, 7):
            cold_streak = self.hot_cold_tracker[num]['cold']
            if cold_streak >= 8: scores[num] += cold_streak * 5
            elif cold_streak >= 5: scores[num] += cold_streak * 3
        if len(self.history_data) > 0:
            history_counter = Counter(self.history_data)
            min_count = min(history_counter.values())
            for num in range(1, 7):
                if history_counter.get(num, 0) == min_count:
                    scores[num] += 25
        return scores
    
    def advanced_selection_strategy(self, last_10_results, last_100_stats, predicted_winner):
        scores = self._multi_factor_analysis(last_10_results, last_100_stats)
        if len(self.history_data) >= 20:
            data_list = list(self.history_data)
            for num in range(1, 7):
                last_positions = [i for i, x in enumerate(data_list) if x == num]
                if len(last_positions) >= 2:
                    gaps = [last_positions[i] - last_positions[i-1] for i in range(1, len(last_positions))]
                    avg_gap = sum(gaps) / len(gaps)
                    current_gap = len(data_list) - last_positions[-1] - 1
                    if current_gap > avg_gap:
                        scores[num] += (current_gap - avg_gap) * 3
        recent_3 = last_10_results[:3] if len(last_10_results) >= 3 else last_10_results
        cluster_nums = [num for num in recent_3 if recent_3.count(num) >= 2]
        for num in cluster_nums:
            scores[num] -= 30
        if len(last_100_stats) == 6:
            ideal_freq = sum(last_100_stats) / 6
            for i, count in enumerate(last_100_stats, 1):
                if count < ideal_freq * 0.8: scores[i] += 25
                elif count > ideal_freq * 1.2: scores[i] -= 15
        if len(last_10_results) >= 3:
            for i in range(len(last_10_results) - 2):
                seq = last_10_results[i:i+3]
                if len(set(seq)) == 1: scores[seq[0]] -= 60
                elif len(set(seq)) == 2:
                    for num in set(seq):
                        if seq.count(num) >= 2:
                            scores[num] -= 25
        filtered_scores = {k: v for k, v in scores.items() if k != predicted_winner}
        if not filtered_scores:
            return self._safe_fallback_choice(last_10_results)
        sorted_candidates = sorted(filtered_scores.items(), key=lambda x: x[1], reverse=True)
        if len(sorted_candidates) >= 2:
            if sorted_candidates[0][1] - sorted_candidates[1][1] > 50:
                return sorted_candidates[0][0]
        top_candidates = sorted_candidates[:min(3, len(sorted_candidates))]
        top_nums = [num for num, score in top_candidates if score > -50]
        if not top_nums:
            return sorted_candidates[0][0]
        return random.choice(top_nums)
        
    def _safe_fallback_choice(self, last_10_results):
        counter = Counter(last_10_results)
        min_count = min(counter.values()) if counter else 0
        candidates = [num for num in range(1, 7) if counter.get(num, 0) == min_count]
        if len(candidates) > 1:
            return candidates[len(candidates) // 2]
        return candidates[0] if candidates else random.choice([1, 2, 3, 4, 5, 6])

smart_analyzer = SmartAnalyzer()

def clear_screen():
    os.system('cls' if platform.system() == "Windows" else 'clear')

def prints(r, g, b, text="text", end="\n"):
    print("\033[38;2;{};{};{}m{}\033[0m".format(r, g, b, text), end=end)

# Đổi tên hàm banner của file vtd8.py để tránh xung đột
def game_banner(game):
    banner_txt = """
████████╗██████╗ ██╗  ██╗
╚══██╔══╝██╔══██╗██║ ██╔╝
   ██║   ██████╔╝█████╔╝ 
   ██║   ██╔═══╝ ██╔═██╗ 
   ██║   ██║     ██║  ██╗
   ╚═╝   ╚═╝     ╚═╝  ╚═╝  
    """
    for i in banner_txt.split('\n'):
        x, y, z = 200, 255, 255
        for j in range(len(i)):
            prints(x, y, z, i[j], end='')
            x -= 4
            time.sleep(0.001)
        print()
    prints(247, 255, 97, "✨" + "═" * 45 + "✨")
    prints(32, 230, 151, "🌟 XWORLD - {} v8.PRO🌟".format(game).center(45))
    prints(247, 255, 97, "═" * 47)
    prints(7, 205, 240, "Telegram: @tankeko12")
    prints(7, 205, 240, "Nhóm Zalo: https://zalo.me/g/ddxsyp497")
    prints(7, 205, 240, "Admin: Duong Phung ")
    prints(247, 255, 97, "═" * 47)

def load_data_cdtd():
    if os.path.exists('data-xw-cdtd.txt'):
        prints(0, 255, 243, 'Bạn có muốn sử dụng thông tin đã lưu hay không? (y/n): ', end='')
        x = input()
        if x.lower() == 'y':
            with open('data-xw-cdtd.txt', 'r', encoding='utf-8') as f:
                return json.load(f)
        prints(247, 255, 97, "═" * 47)
    guide = """
    Huướng dẫn lấy link:
    1.Truy cập vào trang web xworld.io
    2.Đăng nhập tải khoản của bạn
    3.Tìm và nhấn vào chạy đua tốc độ
    4. Nhấn lập tức truy cập
    5.Copy link trang web đó và dán vào đây
"""
    prints(218, 255, 125, guide)
    prints(247, 255, 97, "═" * 47)
    prints(125, 255, 168, '📋Nhập link của bạn:', end=' ')
    link = input()
    user_id = link.split('&')[0].split('?userId=')[1]
    user_secretkey = link.split('&')[1].split('secretKey=')[1]
    prints(218, 255, 125, '    User id của bạn là {}'.format(user_id))
    prints(218, 255, 125, '    User secret key của bạn là {}'.format(user_secretkey))
    json_data = {'user-id': user_id, 'user-secret-key': user_secretkey}
    with open('data-xw-cdtd.txt', 'w+', encoding='utf-8') as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)
    return json_data

def top_100_cdtd(s):
    headers = {'accept': '*/*', 'user-agent': 'Mozilla/5.0'}
    try:
        response = s.get('https://api.sprintrun.win/sprint/recent_100_issues', headers=headers).json()
        nv = list(range(1, 7))
        kq = [response['data']['athlete_2_win_times'][str(i)] for i in nv]
        return nv, kq
    except Exception as e:
        prints(255, 0, 0, f'Lỗi khi lấy top 100: {e}')
        return top_100_cdtd(s)

def top_10_cdtd(s, headers):
    try:
        response = s.get('https://api.sprintrun.win/sprint/recent_10_issues', headers=headers).json()
        ki = [i['issue_id'] for i in response['data']['recent_10']]
        kq = []
        for i in response['data']['recent_10']:
            result = i['result'][0]
            kq.append(result)
            smart_analyzer.add_result(result)
        return ki, kq
    except Exception as e:
        prints(255, 0, 0, f'Lỗi khi lấy top 10: {e}')
        return top_10_cdtd(s, headers)

def print_data(data_top10_cdtd, data_top100_cdtd):
    prints(247, 255, 97, "═" * 47)
    prints(0, 255, 250, "DỮ LIỆU 10 VÁN GẦN NHẤT:".center(50))
    for i in range(len(data_top10_cdtd[0])):
        prints(255, 255, 0, f'Kì {data_top10_cdtd[0][i]}: Người về nhất : {NV[int(data_top10_cdtd[1][i])]}')
    prints(247, 255, 97, "═" * 47)
    prints(0, 255, 250, "DỮ LIỆU 100 VÁN GẦN NHẤT:".center(50))
    for i in range(6):
        prints(255, 255, 0, f'{NV[i+1]} về nhất {data_top100_cdtd[1][i]} lần')
    prints(247, 255, 97, "═" * 47)

def selected_NV(data_top10_cdtd, data_top100_cdtd, htr, heso, bet_amount0):
    bet_amount = bet_amount0
    if htr and not htr[-1]['kq']:
        bet_amount = heso * htr[-1]['bet_amount']
    try:
        last_10_results = data_top10_cdtd[1]
        last_100_stats = data_top100_cdtd[1]
        predicted_winner = smart_analyzer.predict_next_winner(last_10_results, last_100_stats)
        selected = smart_analyzer.advanced_selection_strategy(last_10_results, last_100_stats, predicted_winner)
        return selected, bet_amount
    except Exception as e:
        prints(255, 0, 0, f'Lỗi khi phân tích AI: {e}')
        available = [i for i in range(1, 7) if i != data_top10_cdtd[1][0]]
        return random.choice(available), bet_amount

def kiem_tra_kq_cdtd(s, headers, kq, ki):
    start = time.time()
    prints(0, 255, 37, f'Đang đợi kết quả của kì #{ki}')
    while True:
        data_top10_cdtd = top_10_cdtd(s, headers)
        if int(data_top10_cdtd[0][0]) == int(ki):
            actual_winner = data_top10_cdtd[1][0]
            prints(0, 255, 30, f'Kết quả của kì {ki}: Người về nhất {NV[int(actual_winner)]}')
            smart_analyzer.add_result(actual_winner)
            if actual_winner == kq:
                prints(255, 0, 0, 'Bạn đã thua. Chúc bạn may mắn lần sau!')
                return False
            else:
                prints(0, 255, 37, 'Xin chúc mừng. Bạn đã thắng!')
                return True
        prints(0, 255, 197, f'Đang đợi kết quả {time.time()-start:.0f}...', end='\r')
        time.sleep(1)

def user_asset(s, headers):
    try:
        json_data = {'user_id': int(headers['user-id']), 'source': 'home'}
        response = s.post('https://wallet.3games.io/api/wallet/user_asset', headers=headers, json=json_data).json()
        return response['data']['user_asset']
    except Exception as e:
        prints(255, 0, 0, f'Lỗi khi lấy số dư: {e}')
        return user_asset(s, headers)

def print_stats_cdtd(stats, s, headers, Coin):
    try:
        asset = user_asset(s, headers)
        prints(70, 240, 234, 'Thống kê:')
        win_rate = (stats["win"] / (stats["win"] + stats["lose"])) * 100 if (stats["win"] + stats["lose"]) > 0 else 0
        prints(50, 237, 65, f'Số trận thắng : {stats["win"]}/{stats["win"]+stats["lose"]} ({win_rate:.1f}%)')
        prints(50, 237, 65, f'Chuỗi thắng : {stats["streak"]} (max:{stats["max_streak"]})')
        loi = asset.get(Coin, 0) - stats['asset_0']
        prints(0, 255, 20, f"Lời: {loi:.2f} {Coin}")
    except Exception as e:
        prints(255, 0, 0, f'Lỗi khi in thống kê: {e}')

def print_wallet(asset):
    usdt = asset.get('USDT', 0.0)
    world = asset.get('WORLD', 0.0)
    build = asset.get('BUILD', 0.0)
    prints(23, 232, 159, f' USDT:{usdt:.2f}    WORLD:{world:.2f}    BUILD:{build:.2f}'.center(50))

def bet_cdtd(s, headers, ki, kq, Coin, bet_amount):
    prints(255, 255, 0, f'Đang đặt {Coin} cho kì {ki}:')
    try:
        json_data = {
            'issue_id': int(ki), 'bet_group': 'not_winner', 'asset_type': Coin,
            'athlete_id': kq, 'bet_amount': bet_amount
        }
        response = s.post('https://api.sprintrun.win/sprint/bet', headers=headers, json=json_data).json()
        print(response)
        if response.get('code') == 0 and response.get('msg') == 'ok':
            prints(0, 255, 19, f'Đã đặt {bet_amount} {Coin} thành công vào "Ai không là quán quân"')
    except Exception as e:
        prints(255, 0, 0, f'Lỗi khi đặt {Coin}: {e}')

def main_cdtd():
    s = requests.Session()
    game_banner("CHẠY ĐUA TỐC ĐỘ") # Gọi hàm banner đã đổi tên
    
    data = load_data_cdtd()
    headers = {
        'accept': '*/*', 'accept-language': 'vi,en;q=0.9', 'cache-control': 'no-cache',
        'country-code': 'vn', 'origin': 'https://xworld.info', 'pragma': 'no-cache',
        'priority': 'u=1, i', 'referer': 'https://xworld.info/', 'user-agent': 'Mozilla/5.0',
        'user-id': data['user-id'], 'user-login': 'login_v2', 
        'user-secret-key': data['user-secret-key'], 'xb-language': 'vi-VN'
    }
    asset = user_asset(s, headers)
    print_wallet(asset)
    choice_txt = """
    Nhập loại tiền mà bạn muốn chơi:
        1.USDT
        2.BUILD
        3.WORLD
    """
    prints(219, 237, 138, choice_txt)
    while True:
        prints(125, 255, 168, 'Nhập loại tiền bạn muốn chơi (1/2/3):', end=' ')
        x = input()
        if x in ['1', '2', '3']:
            Coin = ['USDT', 'BUILD', 'WORLD'][int(x)-1]
            break
        else:
            prints(247, 30, 30, 'Nhập sai, vui lòng nhập lại ...', end='\r')
    bet_amount0 = float(input(f'Nhập số {Coin} muốn đặt: '))
    heso = int(input('Nhập hệ số cược sau thua: '))
    delay1 = int(input('Sau bao nhiêu ván thì tạm nghỉ (Nhập 999 nếu không muốn tạm nghỉ): '))
    delay2 = int(input(f'Sau {delay1} ván thì tạm nghỉ bao nhiêu ván (Nhập 0 nếu không muốn nghỉ): '))
    stats = {
        'win': 0, 'lose': 0, 'streak': 0, 'max_streak': 0,
        'asset_0': asset.get(Coin, 0)
    }
    clear_screen()
    game_banner('CHẠY ĐUA TỐC ĐỘ') # Gọi hàm banner đã đổi tên
    htr = []
    tong = 0
    while True:
        tong += 1
        prints(247, 255, 97, "═" * 47)
        print_wallet(user_asset(s, headers))
        data_top10_cdtd = top_10_cdtd(s, headers)
        data_top100_cdtd = top_100_cdtd(s)
        kq, bet_amount = selected_NV(data_top10_cdtd, data_top100_cdtd, htr, heso, bet_amount0)
        print_stats_cdtd(stats, s, headers, Coin)
        prints(0, 246, 255, f'BOT CHỌN : {NV[int(kq)]}')
        cycle = delay1 + delay2
        pos = (tong - 1) % cycle if cycle > 0 else 0
        if pos < delay1:
            stop = False
            bet_cdtd(s, headers, data_top10_cdtd[0][0]+1, kq, Coin, bet_amount)
        else:
            stop = True
            prints(255, 255, 0, 'Ván này tạm nghỉ')
            bet_amount = bet_amount0
        result = kiem_tra_kq_cdtd(s, headers, kq, data_top10_cdtd[0][0]+1)
        if not stop:
            if result:
                stats['win'] += 1
                stats['streak'] += 1
                stats['max_streak'] = max(stats['max_streak'], stats['streak'])
                htr.append({'kq': True, 'bet_amount': bet_amount})
            else:
                stats['streak'] = 0
                stats['lose'] += 1
                htr.append({'kq': False, 'bet_amount': bet_amount})
        time.sleep(10)

# =====================================================================================
# PHẦN 4: ĐIỂM KHỞI ĐỘNG CHÍNH CỦA CHƯƠNG TRÌNH
# =====================================================================================
if __name__ == "__main__":
    # Bước 1: Chạy quy trình xác thực từ banner.py
    authentication_successful = main_authentication()

    # Bước 2: Nếu xác thực thành công, chạy tool game từ vtd8.py
    if authentication_successful:
        print("\n" + luc + "Xác thực thành công! Đang khởi động tool game..." + trang)
        time.sleep(2)
        main_cdtd() # Bắt đầu tool game
    else:
        print("\n" + do + "Xác thực không thành công. Không thể khởi động tool." + trang)
        time.sleep(3)
        sys.exit()

