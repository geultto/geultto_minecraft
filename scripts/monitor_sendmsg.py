import time
import requests
import json
from mcstatus import JavaServer
import os



# 🛠 마인크래프트 서버 정보
SERVER_IP = "127.0.0.1"  # 로컬 서버 또는 퍼블릭 IP
QUERY_PORT = 25565       # 마인크래프트 서버 포트
server = JavaServer.lookup(f"{SERVER_IP}:{QUERY_PORT}")

# 🛠 Slack API 설정
CHANNEL_ID = "C07Q82KJLUT"  # Slack 채널 ID (비공개 채널도 가능)
THREAD_TS = "1738423813.881969"  # Slack 스레드 ID 저장
# 🛠 환경변수에서 Slack Bot Token 불러오기
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
if not SLACK_BOT_TOKEN:
    raise ValueError("❌ 환경변수 SLACK_BOT_TOKEN이 설정되지 않았습니다.")

# 🛠 ID → 이름 매핑 (등록되지 않은 경우 ID 그대로 출력)
player_name_map = {
    "integerji": "지정수",
    "jung_ggplot": "임정",
    "gogogonini": "박건희",
    "bossminji": "우민지a",
    "hojongs": "전종호",
    "YulBae": "배성율",
    "G_NI": "송태현",
    "imnotheomin": "허민(글또 9기)",
    "nasirkr17": "김종진",
    "AugustusJihanVI": "박지한",
    "ventulus95": "이창섭",
    "teddygood": "이찬호",
    "kangdaehyup": "강승현",
    "suminping": "김수민b",
    "nakjunnakjun": "황낙준",
    "NamiHam" : "남희정"
}

# 🔄 이전 접속자 목록 저장 (비교를 위해 사용)
previous_players = set()

# send_slack_message()는 사용안함
# 📌 Slack에 메시지 보내고 `thread_ts` 값 가져오기
def send_slack_message():
    global thread_ts
    url = "https://slack.com/api/chat.postMessage"
    headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}", "Content-Type": "application/json"}
    
    data = {
        "channel": CHANNEL_ID,
        "text": "🌟 마인크래프트 서버 접속 감지 시작!"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_data = response.json()

    if response_data["ok"]:
        thread_ts = response_data["ts"]  # Slack 메시지의 thread_ts 값 저장
        print(f"✅ Slack 메시지 전송 성공, thread_ts: {thread_ts}")
    else:
        print("❌ Slack 메시지 전송 실패:", response_data)


# 📌 Slack 스레드에 댓글 남기기 (새로운 플레이어 입장 시)
def send_slack_reply(message):
    url = "https://slack.com/api/chat.postMessage"
    headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}", "Content-Type": "application/json"}

    data = {
        "channel": CHANNEL_ID,
        "text": message,
        "thread_ts": THREAD_TS  # 스레드 ID 사용
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_data = response.json()

    if response_data["ok"]:
        print(f"✅ Slack 스레드에 댓글 작성 완료: {message}")
    else:
        print("❌ Slack 댓글 작성 실패:", response_data)


# 📌 서버 인원 체크 루프 실행
def monitor_minecraft_server():
    global previous_players

    # 🔹 최초 실행 시 Slack 메시지 전송-> 필요없음 기존 thread에 달거임
    #send_slack_message()
    print("🔄 마인크래프트 서버 접속 감지 시작...")
    
    while True:
        try:
            # 서버 상태 가져오기
            status = server.status()
            current_players = set(player.name for player in status.players.sample) if status.players.sample else set()

            # 🔹 새로운 플레이어 입장 확인
            new_players = current_players - previous_players
            left_players = previous_players - current_players

            message_list = []

            # ✅ 여러 명이 동시에 입장하면 한 번에 메시지 출력
            if new_players:
                joined_names = [player_name_map.get(player, player) for player in new_players]
                joined_message = f"🎉 {', '.join(joined_names)} 님이 입장했습니다!"
                message_list.append(joined_message)

            # ✅ 여러 명이 동시에 퇴장하면 한 번에 메시지 출력
            if left_players:
                left_names = [player_name_map.get(player, player) for player in left_players]
                left_message = f"👋 {', '.join(left_names)} 님이 퇴장했습니다!"
                message_list.append(left_message)

            # ✅ 현재 인원도 한 번만 출력
            if message_list:
                total_players = len(current_players)
                message_list.append(f"🔹 현재 접속 인원: {total_players}명")
                send_slack_reply("\n".join(message_list))


            # 🔹 접속자 목록 업데이트
            previous_players = current_players
        except Exception as e:
            print(f"❌ 서버 정보를 가져오는 중 오류 발생: {e}")

        # 5초마다 반복 실행
        time.sleep(10)

# 🔥 실행
if __name__ == "__main__":
    monitor_minecraft_server()
