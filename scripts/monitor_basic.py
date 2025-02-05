#import sys
#print(sys.version)
import time
from mcstatus import JavaServer

# 마인크래프트 서버 정보
SERVER_IP = "127.0.0.1"  # 로컬 서버 또는 퍼블릭 IP
QUERY_PORT = 25565       # 마인크래프트 서버 포트

server = JavaServer.lookup(f"{SERVER_IP}:{QUERY_PORT}")

# ID → 이름 매핑
player_name_map = {
    "integerji": "지정수",
    "jung_ggplot": "임정",
    "gogogonini": "박건희",
    "bossminji": "우민지a",
    "hojongs": "전종호",
    "YulBae": "배성율",
    "G_NI": "송태현",
    "MakeURegret": "의문의 남자",
    "imnotheomin": "허민(글또 9기)",
    "nasirkr17": "김종진",
    "AugustusJihanVI": "박지한",
    "ventulus95": "이창섭",
    "teddygood": "이찬호",
    "kangdaehyup": "강승현",
    "suminping": "김수민b",
    "nakjunnakjun": "황낙준"
}

# 이전 접속자 목록 저장
previous_players = set()

print("Minecraft 서버 접속 감지 시작...")

while True:
    try:
        # 서버 상태 가져오기
        status = server.status()
        current_players = set(player.name for player in status.players.sample) if status.players.sample else set()

        # 새로운 플레이어 확인
        new_players = current_players - previous_players
        if new_players:
            for player_id in new_players:
                # ID를 이름으로 변환 (없으면 그대로 출력)
                player_name = player_name_map.get(player_id, player_id)
                print(f"🎉 {player_name} 님이 서버에 입장했습니다!")

        # 접속자 목록 업데이트
        previous_players = current_players

    except Exception as e:
        print(f"서버 정보를 가져오는 중 오류 발생: {e}")

    # 일정 주기마다 반복 (예: 5초)
    time.sleep(5)
    print('loop1 지남')
