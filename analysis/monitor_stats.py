import os
import re
import gzip
import datetime
from collections import defaultdict

# 🛠 마인크래프트 로그 파일이 저장된 디렉토리
LOG_DIR = "/home/wasadm/logs"  # 경로 수정 필요

# 🛠 데이터 저장용 딕셔너리
login_count = defaultdict(int)  # 접속 횟수
play_time = defaultdict(int)  # 총 플레이 시간 (초)
death_count = defaultdict(int)  # 사망 횟수
death_details = defaultdict(lambda: defaultdict(int))  # 사망한 몬스터별 횟수 저장
advancements = defaultdict(int)  # 업적 달성 횟수
advancement_list = defaultdict(list)  # 플레이어별 업적 리스트
shortest_stay_ratio = {}  # 체류 시간이 짧은 사람 (체류시간 / 접속 횟수)

# 🎮 플레이어 ID → 실제 이름 변환 테이블
player_name_map = {
    "integerji": "지정수",
    "belleoque7": "임정",
    "jung_ggplot": "임정",
    "gogogonini": "박건희",
    "bossminji": "우민지a",
    "hojongs": "전종호",
    "YulBae": "배성율",
    "G_NI": "송태현",
    "MakeURegret": "의문의 남자",  # 제외할 봇
    "imnotheomin": "허민(글또 9기)",
    "nasirkr17": "김종진",
    "AugustusJihanVI": "박지한",
    "ventulus95": "이창섭",
    "teddygood": "이찬호",
    "kangdaehyup": "강승현",
    "suminping": "김수민b",
    "nakjunnakjun": "황낙준"
}

# 🛠 로그에서 플레이어 활동 데이터 분석
def parse_logs():
    login_times = {}  # 로그인 시간 기록

    for log_file in sorted(os.listdir(LOG_DIR)):
        log_path = os.path.join(LOG_DIR, log_file)

        # 압축된 .gz 로그 파일 처리
        if log_file.endswith(".gz"):
            with gzip.open(log_path, "rt", encoding="utf-8") as f:
                process_log_lines(f, login_times)
        # 일반 .log 파일 처리
        elif log_file.endswith(".log"):
            with open(log_path, "r", encoding="utf-8") as f:
                process_log_lines(f, login_times)

# 🕒 로그에서 시간 파싱 (HH:mm:ss 또는 HH:mm:ss.SSS)
def parse_time(time_str):
    today = datetime.datetime.today().date()
    time_formats = ["%H:%M:%S", "%H:%M:%S.%f"]

    for fmt in time_formats:
        try:
            time_obj = datetime.datetime.strptime(time_str, fmt).time()
            return datetime.datetime.combine(today, time_obj)
        except ValueError:
            continue

    return datetime.datetime.now()  # 기본값 (오류 방지용)

# 🛠 로그 파일에서 줄 단위로 데이터 분석
def process_log_lines(log_lines, login_times):
    for line in log_lines:
        # ⏳ 접속 로그
        login_match = re.search(r"\[(.*?)\] \[Server thread/INFO\]: (.+?) joined the game", line)
        logout_match = re.search(r"\[(.*?)\] \[Server thread/INFO\]: (.+?) left the game", line)
        
        # ☠ 사망 로그 (몬스터별 사망자 기록)
        death_match = re.search(r"\[(.*?)\] \[Server thread/INFO\]: (.+?) was slain by (.+)", line)

        # 🏆 업적 달성 로그
        advancement_match = re.search(r"\[(.*?)\] \[Server thread/INFO\]: (.+?) has made the advancement \[(.+?)\]", line)

        if login_match:
            time_str, player = login_match.groups()
            if player == "MakeURegret":  # 봇 제외
                continue
            login_times[player] = parse_time(time_str)
            login_count[player] += 1  # 접속 횟수 증가

        elif logout_match:
            time_str, player = logout_match.groups()
            if player == "MakeURegret":  # 봇 제외
                continue
            logout_time = parse_time(time_str)

            if player in login_times:
                session_time = (logout_time - login_times[player]).total_seconds()
                play_time[player] += session_time
                del login_times[player]  # 로그인 정보 삭제

        elif death_match:
            _, player, killer = death_match.groups()
            if player == "MakeURegret":  # 봇 제외
                continue
            death_count[player] += 1  # 사망 횟수 증가
            death_details[player][killer] += 1  # 몬스터별 사망 횟수 기록

        elif advancement_match:
            _, player, advancement = advancement_match.groups()
            if player == "MakeURegret":  # 봇 제외
                continue
            advancements[player] += 1
            advancement_list[player].append(advancement)  # 업적 리스트 저장

# 🏆 결과 출력
def display_results():
    # 🚀 체류 시간이 짧은 사람 (총 체류시간 / 접속 횟수)
    for player in play_time:
        if login_count[player] > 0:
            shortest_stay_ratio[player] = play_time[player] / login_count[player]
    
    most_logins = max(login_count, key=login_count.get, default=None)
    longest_play = max(play_time, key=play_time.get, default=None)
    most_deaths = max(death_count, key=death_count.get, default=None)
    most_advancements = max(advancements, key=advancements.get, default=None)
    shortest_stay = min(shortest_stay_ratio, key=shortest_stay_ratio.get, default=None)

    print("\n🏆 **마인크래프트 서버 통계 결과** 🏆\n")

    print("\n🔹 사용자별 접속한 시간:")
    for player, time in play_time.items():
        player_name = player_name_map.get(player, player)
        print(f"   - {player_name}: {time / 3600:.2f} 시간")

    print(f"🚀 가장 많이 접속한 플레이어: **{player_name_map.get(most_logins, most_logins)}** ({login_count[most_logins]}회)")
    print(f"🕒 가장 오래 플레이한 플레이어: **{player_name_map.get(longest_play, longest_play)}** ({play_time[longest_play] / 3600:.2f} 시간)")

    print(f"💀 가장 많이 사망한 플레이어: **{player_name_map.get(most_deaths, most_deaths)}** ({death_count[most_deaths]}회)")
    if most_deaths in death_details:
        print(f"   ➤ 몬스터별 사망 횟수:")
        for monster, count in death_details[most_deaths].items():
            print(f"     - {monster}: {count}회")

    print(f"🏆 가장 많은 업적을 달성한 플레이어: **{player_name_map.get(most_advancements, most_advancements)}** ({advancements[most_advancements]}개)")

    print(f"🐌 가장 체류시간이 짧은 플레이어: **{player_name_map.get(shortest_stay, shortest_stay)}** (평균 {shortest_stay_ratio[shortest_stay]:.2f} 초)")

# 실행
if __name__ == "__main__":
    parse_logs()
    display_results()
