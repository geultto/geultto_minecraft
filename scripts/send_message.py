import requests
#게임해또_마크서버에서 특정스레드에 메세지를 보내기 위한 코드입니다.

import json

CHANNEL_ID = "C08AQ7KLUJ3"
thread_ts = "1738420859.268459"
# 🛠 환경변수에서 Slack Bot Token 불러오기
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
if not SLACK_BOT_TOKEN:
    raise ValueError("❌ 환경변수 SLACK_BOT_TOKEN이 설정되지 않았습니다.")

def send_reply(thread_ts, message):
    url = "https://slack.com/api/chat.postMessage"
    headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}", "Content-Type": "application/json"}

    data = {
        "channel": CHANNEL_ID,
        "text": message,
        "thread_ts": thread_ts  # 스레드 ID (댓글을 달 메시지)
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_data = response.json()

    if response_data["ok"]:
        print(f"✅ 스레드에 댓글 작성 완료: {message}")
    else:
        print("❌ 댓글 작성 실패:", response_data)

# 특정 메시지에 댓글 남기기
send_reply(thread_ts, "🎉 서버에 새로운 플레이어가 입장했습니다!")
