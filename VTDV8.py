import hashlib
from collections import Counter, deque
import statistics
import platform
from datetime import datetime
import base64
import urllib.parse
import requests
import random
import string
import math
import json
import os
import time
try:
    import numpy as np
except ImportError:
    np = None
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    pass

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
        self.history_data = deque(maxlen=200)  # Lưu 200 kết quả gần nhất
        self.pattern_memory = {}
        self.frequency_tracker = {i: 0 for i in range(1, 7)}
        self.sequence_patterns = deque(maxlen=50)
        self.hot_cold_tracker = {i: {'hot': 0, 'cold': 0} for i in range(1, 7)}
        self.winning_strategies = []
        
    def add_result(self, result):
        """Thêm kết quả mới vào hệ thống phân tích"""
        self.history_data.append(result)
        self.frequency_tracker[result] += 1
        self.sequence_patterns.append(result)
        self._update_hot_cold(result)
        
    def _update_hot_cold(self, result):
        """Cập nhật trạng thái hot/cold của các số"""
        for num in range(1, 7):
            if num == result:
                self.hot_cold_tracker[num]['hot'] += 1
                self.hot_cold_tracker[num]['cold'] = 0
            else:
                self.hot_cold_tracker[num]['cold'] += 1
                
    def analyze_patterns(self):
        """Phân tích các pattern trong dữ liệu"""
        if len(self.history_data) < 10:
            return None
            
        patterns = {}
        data_list = list(self.history_data)
        
        # Phân tích chu kỳ
        for cycle_len in range(2, min(20, len(data_list))):
            pattern_score = 0
            for i in range(cycle_len, len(data_list)):
                if data_list[i] == data_list[i - cycle_len]:
                    pattern_score += 1
            if len(data_list) > cycle_len:
                patterns[f'cycle_{cycle_len}'] = pattern_score / (len(data_list) - cycle_len)
            else:
                patterns[f'cycle_{cycle_len}'] = 0
            
        # Phân tích cặp số liên tiếp
        consecutive_patterns = {}
        for i in range(1, len(data_list)):
            pair = (data_list[i-1], data_list[i])
            consecutive_patterns[pair] = consecutive_patterns.get(pair, 0) + 1
            
        return patterns, consecutive_patterns
        
    def calculate_probability_matrix(self):
        """Tính ma trận xác suất dựa trên lịch sử"""
        if len(self.history_data) < 20:
            return {i: 1/6 for i in range(1, 7)}
            
        data_list = list(self.history_data)
        
        # Tính tần suất xuất hiện
        frequencies = Counter(data_list)
        total = len(data_list)
        
        # Tính trọng số dựa trên thời gian (dữ liệu gần hơn có trọng số cao hơn)
        weighted_probs = {}
        for num in range(1, 7):
            base_prob = frequencies[num] / total if num in frequencies else 0
            
            # Tính trọng số thời gian (20% cho các kết quả gần nhất)
            recent_weight = 0
            recent_count = min(20, len(data_list))
            if recent_count > 0:
                for i in range(-recent_count, 0):
                    if data_list[i] == num:
                        recent_weight += (recent_count + i) / recent_count
                        
                # Kết hợp tần suất tổng thể và trọng số gần đây
                weighted_probs[num] = base_prob * 0.7 + (recent_weight / recent_count) * 0.3
            else:
                weighted_probs[num] = base_prob
            
        return weighted_probs
        
    def predict_next_winner(self, last_10_results, last_100_stats):
        """Dự đoán số thắng tiếp theo với độ chính xác cao"""
        if len(self.history_data) < 10:
            # Nếu chưa có đủ dữ liệu, chọn số ít xuất hiện nhất trong top 10 gần đây
            return self._safe_fallback_choice(last_10_results)
            
        # Phân tích nhiều yếu tố
        predictions = self._multi_factor_analysis(last_10_results, last_100_stats)
        
        # Chọn số có điểm số cao nhất (tránh số thắng gần nhất)
        avoid_numbers = set(last_10_results[:3])  # Tránh 3 số thắng gần nhất
        
        best_choice = None
        best_score = -1
        
        for num, score in predictions.items():
            if num not in avoid_numbers and score > best_score:
                best_choice = num
                best_score = score
                
        return best_choice if best_choice else self._safe_fallback_choice(last_10_results)
        
    def _multi_factor_analysis(self, last_10_results, last_100_stats):
        """Phân tích đa yếu tố để dự đoán - Cải tiến cho tỷ lệ thắng cao"""
        scores = {i: 0 for i in range(1, 7)}
        
        # Yếu tố 1: Tần suất xuất hiện trong 100 ván gần nhất (siêu tăng trọng số)
        total_100 = sum(last_100_stats) if sum(last_100_stats) > 0 else 6
        for i, count in enumerate(last_100_stats, 1):
            # Ưu tiên CỰC MẠNH số ít xuất hiện
            relative_freq = count / total_100
            if relative_freq < 0.12:  # Số xuất hiện < 12%
                scores[i] += 80
            elif relative_freq < 0.15:  # 12-15%
                scores[i] += 60
            elif relative_freq < 0.18:  # 15-18%
                scores[i] += 40
            else:
                scores[i] += 5  # Giảm điểm cho số xuất hiện nhiều
                
        # Yếu tố 2: Phân tích chuỗi gần đây (quan trọng nhất)
        recent_5 = last_10_results[:5] if len(last_10_results) >= 5 else last_10_results
        recent_counter = Counter(recent_5)
        
        # Tránh CỰC MẠNH các số xuất hiện nhiều trong 5 ván gần nhất
        for num, count in recent_counter.items():
            if count >= 3:  # Xuất hiện >= 3 lần trong 5 ván
                scores[num] -= 100
            elif count == 2:  # Xuất hiện 2 lần trong 5 ván
                scores[num] -= 60
            elif count == 1:
                scores[num] -= 25
                
        # Yếu tố 3: Chuỗi lặp lại liên tiếp (siêu nghiêm ngặt)
        if len(last_10_results) >= 1:
            last_winner = last_10_results[0]
            # Tránh TUYỆT ĐỐI số vừa thắng
            scores[last_winner] -= 200
            
            # Nếu có 2 số giống nhau liên tiếp, tránh số đó
            if len(last_10_results) >= 2 and last_10_results[0] == last_10_results[1]:
                scores[last_winner] -= 100
                
            # Nếu có 3 số giống nhau trong 4 ván gần nhất, tránh cực mạnh
            if len(last_10_results) >= 4:
                recent_4 = last_10_results[:4]
                for num in range(1, 7):
                    if recent_4.count(num) >= 3:
                        scores[num] -= 150
                
        # Yếu tố 4: Phân tích pattern chu kỳ nâng cao
        if len(self.history_data) >= 10:
            patterns, consecutive = self.analyze_patterns()
            if consecutive:
                # Tránh các cặp số hay xuất hiện liên tiếp
                last_num = last_10_results[0] if last_10_results else 0
                for (prev, curr), freq in consecutive.items():
                    if prev == last_num and freq > 1:
                        scores[curr] -= 20
                        
        # Yếu tố 5: Cân bằng thống kê tổng thể
        for num in range(1, 7):
            cold_streak = self.hot_cold_tracker[num]['cold']
            if cold_streak >= 8:  # Số "siêu lạnh"
                scores[num] += cold_streak * 5
            elif cold_streak >= 5:
                scores[num] += cold_streak * 3
                
        # Yếu tố 6: Bonus cho số ít được chọn trong lịch sử
        if len(self.history_data) > 0:
            history_counter = Counter(self.history_data)
            min_count = min(history_counter.values())
            for num in range(1, 7):
                if history_counter[num] == min_count:
                    scores[num] += 25
                    
        return scores
    
    def advanced_selection_strategy(self, last_10_results, last_100_stats, predicted_winner):
        """Chiến lược chọn số nâng cao với độ chính xác cao hơn"""
        scores = self._multi_factor_analysis(last_10_results, last_100_stats)
        
        # Bổ sung thêm các yếu tố nâng cao
        
        # Yếu tố 7: Phân tích gap giữa các lần xuất hiện
        if len(self.history_data) >= 20:
            data_list = list(self.history_data)
            for num in range(1, 7):
                last_positions = [i for i, x in enumerate(data_list) if x == num]
                if len(last_positions) >= 2:
                    # Tính gap trung bình
                    gaps = [last_positions[i] - last_positions[i-1] for i in range(1, len(last_positions))]
                    avg_gap = sum(gaps) / len(gaps)
                    current_gap = len(data_list) - last_positions[-1] - 1
                    
                    # Nếu gap hiện tại > gap trung bình, tăng điểm
                    if current_gap > avg_gap:
                        scores[num] += (current_gap - avg_gap) * 3
        
        # Yếu tố 8: Tránh số có xu hướng đi theo cluster
        recent_3 = last_10_results[:3] if len(last_10_results) >= 3 else last_10_results
        cluster_nums = [num for num in recent_3 if recent_3.count(num) >= 2]
        for num in cluster_nums:
            scores[num] -= 30
            
        # Yếu tố 9: Ưu tiên số có pattern xuất hiện đều đặn
        if len(last_100_stats) == 6:
            ideal_freq = sum(last_100_stats) / 6
            for i, count in enumerate(last_100_stats, 1):
                if count < ideal_freq * 0.8:  # Số thiếu hụt
                    scores[i] += 25
                elif count > ideal_freq * 1.2:  # Số thừa
                    scores[i] -= 15
        
        # Yếu tố 10: Tránh chuỗi số liên tiếp
        if len(last_10_results) >= 3:
            for i in range(len(last_10_results) - 2):
                seq = last_10_results[i:i+3]
                if len(set(seq)) == 1:  # 3 số giống nhau liên tiếp
                    scores[seq[0]] -= 60
                elif len(set(seq)) == 2:  # 2/3 số giống nhau
                    for num in set(seq):
                        if seq.count(num) >= 2:
                            scores[num] -= 25
        
        # Chọn số có điểm cao nhất với yếu tố ngẫu nhiên thông minh
        filtered_scores = {k: v for k, v in scores.items() if k != predicted_winner}
        if not filtered_scores:
            return self._safe_fallback_choice(last_10_results)
        
        # Lấy top 2-3 số có điểm cao nhất
        sorted_candidates = sorted(filtered_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Nếu có số nào điểm quá cao so với các số khác, chọn luôn
        if len(sorted_candidates) >= 2:
            best_score = sorted_candidates[0][1]
            second_score = sorted_candidates[1][1]
            
            # Nếu số tốt nhất có điểm cao hơn rất nhiều (>50 điểm), chọn luôn
            if best_score - second_score > 50:
                return sorted_candidates[0][0]
        
        # Ngược lại, chọn ngẫu nhiên trong top 2-3 ứng viên tốt nhất
        top_candidates = sorted_candidates[:min(3, len(sorted_candidates))]
        top_nums = [num for num, score in top_candidates if score > -50]  # Loại số có điểm quá thấp
        
        if not top_nums:
            return sorted_candidates[0][0]
            
        return random.choice(top_nums)
        
    def _safe_fallback_choice(self, last_10_results):
        """Lựa chọn an toàn khi chưa có đủ dữ liệu"""
        # Chọn số xuất hiện ít nhất trong 10 ván gần đây
        counter = Counter(last_10_results)
        min_count = min(counter.values()) if counter else 0
        candidates = [num for num in range(1, 7) if counter[num] == min_count]
        
        # Nếu có nhiều ứng viên, chọn số ở giữa để tăng cơ hội
        if len(candidates) > 1:
            return candidates[len(candidates) // 2]
        return candidates[0] if candidates else random.choice([1, 2, 3, 4, 5, 6])

# Khởi tạo analyzer toàn cục
smart_analyzer = SmartAnalyzer()

def clear_screen():
    os.system('cls' if platform.system() == "Windows" else 'clear')

def prints(r, g, b, text="text", end="\n"):
    print("\033[38;2;{};{};{}m{}\033[0m".format(r, g, b, text), end=end)

def banner(game):
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
    prints(7, 205, 240, "Telegram: tankeko12")
    prints(7, 205, 240, "Nhóm Zalo: https://zalo.me/g/viiuml595")
    prints(7, 205, 240, "Admin: Duong Phung | Zalo: 0865656488")
    prints(247, 255, 97, "═" * 47)

def load_data_cdtd():
    if os.path.exists('data-xw-cdtd.txt'):
        prints(0, 255, 243, 'Bạn có muốn sử dụng thông tin đã lưu hay không? (y/n): ', end='')
        x = input()
        if x == 'y':
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
    json_data = {
        'user-id': user_id,
        'user-secret-key': user_secretkey,
    }
    with open('data-xw-cdtd.txt', 'w+', encoding='utf-8') as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)
    return json_data

def top_100_cdtd(s):
    headers = {
        'accept': '*/*',
        'accept-language': 'vi,en;q=0.9',
        'origin': 'https://sprintrun.win',
        'priority': 'u=1, i',
        'referer': 'https://sprintrun.win/',
        'user-agent': 'Mozilla/5.0',
    }
    try:
        response = s.get('https://api.sprintrun.win/sprint/recent_100_issues', headers=headers).json()
        nv = [1, 2, 3, 4, 5, 6]
        kq = []
        for i in range(1, 7):
            kq.append(response['data']['athlete_2_win_times'][str(i)])
        return nv, kq
    except Exception as e:
        prints(255, 0, 0, 'Lỗi khi lấy top 100: {}'.format(e))
        return top_100_cdtd(s)

def top_10_cdtd(s, headers):
    try:
        response = s.get('https://api.sprintrun.win/sprint/recent_10_issues', headers=headers).json()
        ki = []
        kq = []
        for i in response['data']['recent_10']:
            ki.append(i['issue_id'])
            kq.append(i['result'][0])
            # Thêm kết quả vào analyzer để học
            smart_analyzer.add_result(i['result'][0])
        return ki, kq
    except Exception as e:
        prints(255, 0, 0, 'Lỗi khi lấy top 10: {}'.format(e))
        return top_10_cdtd(s, headers)

def print_data(data_top10_cdtd, data_top100_cdtd):
    prints(247, 255, 97, "═" * 47)
    prints(0, 255, 250, "DỮ LIỆU 10 VÁN GẦN NHẤT:".center(50))
    for i in range(len(data_top10_cdtd[0])):
        prints(255, 255, 0, 'Kì {}: Người về nhất : {}'.format(data_top10_cdtd[0][i], NV[int(data_top10_cdtd[1][i])]))
    prints(247, 255, 97, "═" * 47)
    prints(0, 255, 250, "DỮ LIỆU 100 VÁN GẦN NHẤT:".center(50))
    for i in range(6):
        prints(255, 255, 0, '{} về nhất {} lần'.format(NV[int(i+1)], data_top100_cdtd[1][int(i)]))
    prints(247, 255, 97, "═" * 47)

def selected_NV(data_top10_cdtd, data_top100_cdtd, htr, heso, bet_amount0):
    """Chọn người thắng bằng AI thông minh thay vì random"""
    bet_amount = bet_amount0
    if len(htr) >= 1:
        if htr[-1]['kq'] == False:
            bet_amount = heso * htr[-1]['bet_amount']
    
    try:
        # Sử dụng Smart Analyzer để dự đoán
        last_10_results = data_top10_cdtd[1]
        last_100_stats = data_top100_cdtd[1]
        
        # Dự đoán số thắng tiếp theo
        predicted_winner = smart_analyzer.predict_next_winner(last_10_results, last_100_stats)
        
        # Phân tích âm thầm (không hiển thị)
        prob_matrix = smart_analyzer.calculate_probability_matrix()
        
        # Logic nâng cấp: Chọn thông minh hơn dựa trên multiple strategies
        selected = smart_analyzer.advanced_selection_strategy(last_10_results, last_100_stats, predicted_winner)
        
        return selected, bet_amount
        
    except Exception as e:
        prints(255, 0, 0, 'Lỗi khi phân tích AI: {}'.format(e))
        # Fallback to safer logic instead of pure random
        available = [i for i in range(1, 7) if i != data_top10_cdtd[1][0]]
        return random.choice(available), bet_amount

def kiem_tra_kq_cdtd(s, headers, kq, ki):
    start = time.time()
    prints(0, 255, 37, 'Đang đợi kết quả của kì #{}'.format(ki))
    while True:
        data_top10_cdtd = top_10_cdtd(s, headers)
        if int(data_top10_cdtd[0][0]) == int(ki):
            actual_winner = data_top10_cdtd[1][0]
            prints(0, 255, 30, 'Kết quả của kì {}: Người về nhất {}'.format(ki, NV[int(actual_winner)]))
            
            # Cập nhật kết quả vào AI analyzer
            smart_analyzer.add_result(actual_winner)
            
            if actual_winner == kq:
                prints(255, 0, 0, 'Bạn đã thua. Chúc bạn may mắn lần sau!')
                return False
            else:
                prints(0, 255, 37, 'Xin chúc mừng. Bạn đã thắng!')
                return True
        prints(0, 255, 197, 'Đang đợi kết quả {:.0f}...'.format(time.time()-start), end='\r')

def user_asset(s, headers):
    try:
        json_data = {
            'user_id': int(headers['user-id']),
            'source': 'home',
        }
        response = s.post('https://wallet.3games.io/api/wallet/user_asset', headers=headers, json=json_data).json()
        asset = {
            'USDT': response['data']['user_asset']['USDT'],
            'WORLD': response['data']['user_asset']['WORLD'],
            'BUILD': response['data']['user_asset']['BUILD']
        }
        return asset
    except Exception as e:
        prints(255, 0, 0, 'Lỗi khi lấy số dư: {}'.format(e))
        return user_asset(s, headers)

def print_stats_cdtd(stats, s, headers, Coin):
    try:
        asset = user_asset(s, headers)
        prints(70, 240, 234, 'Thống kê:')
        win_rate = (stats["win"] / (stats["win"] + stats["lose"])) * 100 if (stats["win"] + stats["lose"]) > 0 else 0
        prints(50, 237, 65, 'Số trận thắng : {}/{} ({:.1f}%)'.format(stats["win"], stats["win"]+stats["lose"], win_rate))
        prints(50, 237, 65, 'Chuỗi thắng : {} (max:{})'.format(stats["streak"], stats["max_streak"]))
        loi = asset[Coin] - stats['asset_0']
        prints(0, 255, 20, "Lời: {:.2f} {}".format(loi, Coin))
        
        # Thông tin AI đã được ẩn theo yêu cầu
    except Exception as e:
        prints(255, 0, 0, 'Lỗi khi in thống kê: {}'.format(e))

def print_wallet(s, asset):
    prints(23, 232, 159, ' USDT:{:.2f}    WORLD:{:.2f}    BUILD:{:.2f}'.format(asset["USDT"], asset["WORLD"], asset["BUILD"]).center(50))

def bet_cdtd(s, headers, ki, kq, Coin, bet_amount):
    prints(255, 255, 0, 'Đang đặt {} cho kì {}:'.format(Coin, ki))
    try:
        json_data = {
            'issue_id': int(ki),
            'bet_group': 'not_winner',
            'asset_type': Coin,
            'athlete_id': kq,
            'bet_amount': bet_amount,
        }
        response = s.post('https://api.sprintrun.win/sprint/bet', headers=headers, json=json_data).json()
        print(response)
        if response['code'] == 0 and response['msg'] == 'ok':
            prints(0, 255, 19, 'Đã đặt {} {} thành công vào "Ai không là quán quân"'.format(bet_amount, Coin))
    except Exception as e:
        prints(255, 0, 0, 'Lỗi khi đặt {}: {}'.format(Coin, e))

def main_cdtd():
    s = requests.Session()
    banner("CHẠY ĐUA TỐC ĐỘ")
    
    data = load_data_cdtd()
    headers = {
        'accept': '*/*',
        'accept-language': 'vi,en;q=0.9',
        'cache-control': 'no-cache',
        'country-code': 'vn',
        'origin': 'https://xworld.info',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://xworld.info/',
        'user-agent': 'Mozilla/5.0',
        'user-id': data['user-id'],
        'user-login': 'login_v2',
        'user-secret-key': data['user-secret-key'],
        'xb-language': 'vi-VN',
    }
    asset = user_asset(s, headers)
    print_wallet(s, user_asset(s, headers))
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
        if x in ['1','2','3']:
            if x == '1':
                Coin = 'USDT'
            elif x == '2':
                Coin = 'BUILD'
            else:
                Coin = 'WORLD'
            break
        else:
            prints(247, 30, 30, 'Nhập sai, vui lòng nhập lại ...', end='\r')
    bet_amount0 = float(input('Nhập số {} muốn đặt: '.format(Coin)))
    heso = int(input('Nhập hệ số cược sau thua: '))
    delay1 = int(input('Sau bao nhiêu ván thì tạm nghỉ (Nhập 999 nếu không muốn tạm nghỉ): '))
    delay2 = int(input('Sau {} ván thì tạm nghỉ bao nhiêu ván (Nhập 0 nếu không muốn nghỉ): '.format(delay1)))
    stats = {
        'win': 0,
        'lose': 0,
        'streak': 0,
        'max_streak': 0,
        'asset_0': asset[Coin]
    }
    clear_screen()
    banner('CHẠY ĐUA TỐC ĐỘ')
    htr = []
    tong = 0
    while True:
        tong += 1
        prints(247, 255, 97, "═" * 47)
        print_wallet(s, user_asset(s, headers))
        data_top10_cdtd = top_10_cdtd(s, headers)
        data_top100_cdtd = top_100_cdtd(s)
        kq, bet_amount = selected_NV(data_top10_cdtd, data_top100_cdtd, htr, heso, bet_amount0)
        print_stats_cdtd(stats, s, headers, Coin)
        prints(0, 246, 255, 'BOT CHỌN : {}'.format(NV[int(kq)]))
        cycle = delay1 + delay2
        pos = (tong - 1) % cycle
        if pos < delay1:
            stop = False
            bet_cdtd(s, headers, data_top10_cdtd[0][0]+1, kq, Coin, bet_amount)
        else:
            stop = True
            prints(255, 255, 0, 'Ván này tạm nghỉ')
            bet_amount = bet_amount0
        result = kiem_tra_kq_cdtd(s, headers, kq, data_top10_cdtd[0][0]+1)
        if result == True:
            stats['win'] += 1
            stats['streak'] += 1
            stats['max_streak'] = max(stats['max_streak'], stats['streak'])
            if stop == False:
                htr.append({'kq': True, 'bet_amount': bet_amount})
        elif result == False:
            stats['streak'] = 0
            stats['lose'] += 1
            if stop == False:
                htr.append({'kq': False, 'bet_amount': bet_amount})
        time.sleep(10)

# Chạy chương trình
if __name__ == "__main__":
    main_cdtd()