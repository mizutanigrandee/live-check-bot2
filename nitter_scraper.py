import requests
import os
import json

# Nitterで監視するアカウントのURL一覧 (例)
SITES = [
    # ここに実際のNitter URLを追加
    "https://nitter.poast.org/BTS_twt",
    "https://nitter.poast.org/higedan_Official",
    "https://nitter.poast.org/KingGnu_JP",
    "https://nitter.poast.org/YOASOBI_staff",
]

# 検知キーワード(大文字小文字を無視して判定)
KEYWORDS = ["京セラドーム", "ヤンマースタジアム", "kyocera"]

# (任意) URL→アーティスト名の対応表
ARTIST_MAP = {
    "https://nitter.poast.org/BTS_twt": "BTS",
    "https://nitter.poast.org/higedan_Official": "Official髭男dism",
    "https://nitter.poast.org/KingGnu_JP": "King Gnu",
    "https://nitter.poast.org/YOASOBI_staff": "YOASOBI",
    # ... 必要に応じて追加
}

def load_found_snippets():
    """
    過去に検出した行情報を found_snippets_nitter.json から読み込む。
    """
    try:
        with open("found_snippets_nitter.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_found_snippets(data):
    """
    found_snippets_nitter.json に書き込み
    """
    with open("found_snippets_nitter.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def send_slack_message(text):
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
    if not webhook_url:
        print("No Slack webhook URL found in environment.")
        return
    payload = {"text": text}
    try:
        resp = requests.post(webhook_url, json=payload, timeout=10)
        if resp.status_code != 200:
            print(f"Slack post failed: {resp.text}")
    except Exception as e:
        print(f"Slack post error: {e}")

def detect_new_lines(url, found_data):
    """
    NitterページをGETし、キーワード含む行を抽出。
    既にfound_dataに登録されていない行だけを返す。
    """
    new_lines = []
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        lines = resp.text.split("\n")

        for line in lines:
            # 行を小文字化
            lower_line = line.lower()
            for kw in KEYWORDS:
                # キーワードも小文字化
                if kw.lower() in lower_line:
                    # まだ登録されていないなら、新行とみなす
                    if line not in found_data.get(url, []):
                        new_lines.append(line.strip())
                    break
    except Exception as e:
        print(f"[ERROR] {url} - {e}")
    return new_lines

if __name__ == "__main__":
    found_data = load_found_snippets()

    for url in SITES:
        artist_name = ARTIST_MAP.get(url, "アーティスト不明")
        newly_found_lines = detect_new_lines(url, found_data)
        if newly_found_lines:
            for line in newly_found_lines:
                msg = (
                    f"【Nitter監視：新投稿でライブ情報？】\n"
                    f"アーティスト: {artist_name}\n"
                    f"URL: {url}\n"
                    f"該当行: {line}"
                )
                print(msg)
                send_slack_message(msg)

            # found_data に追加
            if url not in found_data:
                found_data[url] = []
            found_data[url].extend(newly_found_lines)

    save_found_snippets(found_data)
