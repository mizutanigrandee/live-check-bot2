import requests
import os
import json

#################################
#  NitterアカウントURLをまとめたリスト
#################################
SITES = [
    "https://nitter.poast.org/KinKiKids_721",
    "https://nitter.poast.org/Bz_Official",
    "https://nitter.poast.org/SHINee",
    "https://nitter.poast.org/EXO_NEWS_JP",
    "https://nitter.poast.org/exile_news__",
    "https://nitter.poast.org/gen_senden",
    "https://nitter.poast.org/nogizaka46",
    "https://nitter.poast.org/JUMP_Storm",
    "https://nitter.poast.org/generationsfext",
    "https://nitter.poast.org/BTS_jp_official",
    "https://nitter.poast.org/3rd_JSB_NEWS",
    "https://nitter.poast.org/backnumberstaff",
    "https://nitter.poast.org/BLACKPINK",
    "https://nitter.poast.org/sasfannet",
    "https://nitter.poast.org/NiziU__official",
    "https://nitter.poast.org/Infinity_rJP",
    "https://nitter.poast.org/ENHYPEN_JP",
    "https://nitter.poast.org/pledis_17jp",  
    "https://nitter.poast.org/TXT_bighit_jp",
    "https://nitter.poast.org/Stray_Kids_JP",
    "https://nitter.poast.org/SN__20200122",
    "https://nitter.poast.org/BEFIRSTofficial",
    "https://nitter.poast.org/SixTONES_SME",
    "https://nitter.poast.org/reissuerecords",
    "https://nitter.poast.org/vaundy_engawa",
    "https://nitter.poast.org/AORINGOHUZIN",
    "https://nitter.poast.org/YOASOBI_staff",
    "https://nitter.poast.org/spitz30th_UM",
    "https://nitter.poast.org/SekaiNoOwariOFC",
    "https://nitter.poast.org/mc_official_jp",
    "https://nitter.poast.org/aimyonGtter",
    "https://nitter.poast.org/KingGnu_JP",
    "https://nitter.poast.org/officialhige",
    "https://nitter.poast.org/ado1024imokenp",
    "https://nitter.poast.org/yuzu_official",
    "https://nitter.poast.org/ONEOKROCK_japan",
    "https://nitter.poast.org/JYPETWICE_JAPAN",
    "https://nitter.poast.org/sudamasakimusic",
    "https://nitter.poast.org/BROS_1991",
    "https://nitter.poast.org/fujiikazestaff",
    "https://nitter.poast.org/dcte_staff",
    "https://nitter.poast.org/tobeofficial_jp",
    "https://nitter.poast.org/kp_official0523",
    "https://nitter.poast.org/glay_official",
    "https://nitter.poast.org/LArc_official",
    "https://nitter.poast.org/OVTT_official",
    "https://nitter.poast.org/728_Storm",
    "https://nitter.poast.org/Aegroupofficial",
    "https://nitter.poast.org/hikki_staff",
    "https://nitter.poast.org/TeamKobukuro",
    "https://nitter.poast.org/NCT_OFFICIAL_JP",
    "https://nitter.poast.org/official__INI",
    "https://nitter.poast.org/Da_iCE_STAFF",
    "https://nitter.poast.org/number_i_staff",
]

###################################################
# URL→アーティスト名 (推測含む) の対応辞書
# 必要に応じて修正・加筆ください
###################################################
ARTIST_MAP = {
    "https://nitter.poast.org/KinKiKids_721": "KinKi Kids",
    "https://nitter.poast.org/Bz_Official": "B'z",
    "https://nitter.poast.org/SHINee": "SHINee",
    "https://nitter.poast.org/EXO_NEWS_JP": "EXO",
    "https://nitter.poast.org/exile_news__": "EXILE",
    "https://nitter.poast.org/gen_senden": "星野源",
    "https://nitter.poast.org/nogizaka46": "乃木坂46",
    "https://nitter.poast.org/JUMP_Storm": "Hey!Say!JUMP",
    "https://nitter.poast.org/generationsfext": "GENERATIONS",
    "https://nitter.poast.org/BTS_jp_official": "BTS",
    "https://nitter.poast.org/3rd_JSB_NEWS": "三代目J SOUL BROTHERS",
    "https://nitter.poast.org/backnumberstaff": "back number",
    "https://nitter.poast.org/BLACKPINK": "BLACKPINK",
    "https://nitter.poast.org/sasfannet": "サザンオールスターズ?",
    "https://nitter.poast.org/NiziU__official": "NiziU",
    "https://nitter.poast.org/Infinity_rJP": "関ジャニ∞?",
    "https://nitter.poast.org/ENHYPEN_JP": "ENHYPEN",
    "https://nitter.poast.org/pledis_17jp": "SEVENTEEN",
    "https://nitter.poast.org/TXT_bighit_jp": "TXT",
    "https://nitter.poast.org/Stray_Kids_JP": "Stray Kids",
    "https://nitter.poast.org/SN__20200122": "Snow Man?",
    "https://nitter.poast.org/BEFIRSTofficial": "BE:FIRST",
    "https://nitter.poast.org/SixTONES_SME": "SixTONES",
    "https://nitter.poast.org/reissuerecords": "米津玄師",
    "https://nitter.poast.org/vaundy_engawa": "Vaundy",
    "https://nitter.poast.org/AORINGOHUZIN": "グリーンアップル",
    "https://nitter.poast.org/YOASOBI_staff": "YOASOBI",
    "https://nitter.poast.org/spitz30th_UM": "スピッツ",
    "https://nitter.poast.org/SekaiNoOwariOFC": "SEKAI NO OWARI",
    "https://nitter.poast.org/mc_official_jp": "Mr.Children",
    "https://nitter.poast.org/aimyonGtter": "あいみょん",
    "https://nitter.poast.org/KingGnu_JP": "King Gnu",
    "https://nitter.poast.org/officialhige": "Official髭男dism",
    "https://nitter.poast.org/ado1024imokenp": "Ado",
    "https://nitter.poast.org/yuzu_official": "ゆず",
    "https://nitter.poast.org/ONEOKROCK_japan": "ONE OK ROCK",
    "https://nitter.poast.org/JYPETWICE_JAPAN": "TWICE",
    "https://nitter.poast.org/sudamasakimusic": "菅田将暉",
    "https://nitter.poast.org/BROS_1991": "福山雅治",
    "https://nitter.poast.org/fujiikazestaff": "藤井風",
    "https://nitter.poast.org/dcte_staff": "DREAMS COME TRUE?",
    "https://nitter.poast.org/tobeofficial_jp": "TOBE",
    "https://nitter.poast.org/kp_official0523": "King & Prince",
    "https://nitter.poast.org/glay_official": "GLAY",
    "https://nitter.poast.org/LArc_official": "L'Arc-en-Ciel",
    "https://nitter.poast.org/OVTT_official": "timelesz",
    "https://nitter.poast.org/728_Storm": "なにわ男子",
    "https://nitter.poast.org/Aegroupofficial": "Aぇ group",
    "https://nitter.poast.org/hikki_staff": "宇多田ヒカル",
    "https://nitter.poast.org/TeamKobukuro": "コブクロ",
    "https://nitter.poast.org/NCT_OFFICIAL_JP": "NCT",
    "https://nitter.poast.org/official__INI": "INI",
    "https://nitter.poast.org/Da_iCE_STAFF": "Da-iCE",
    "https://nitter.poast.org/number_i_staff": "NUMBER I",
}


###################################################
#  検知したいキーワード（大文字小文字を無視）
###################################################
KEYWORDS = ["京セラドーム", "ヤンマースタジアム", "kyocera"]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
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
    found_snippets_nitter.json に書き込む
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
    1. Nitterページを取得
    2. 行ごとに分割し、小文字化してキーワード検索
    3. 既にfound_dataにある行はスキップ
    """
    new_lines = []
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
  
        lines = resp.text.split("\n")
        for line in lines:
            lower_line = line.lower()
            for kw in KEYWORDS:
                if kw.lower() in lower_line:
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

            # found_data に追記
            if url not in found_data:
                found_data[url] = []
            found_data[url].extend(newly_found_lines)

    save_found_snippets(found_data)
