import requests
import time
import json
import os
from pystyle import Colorate, Colors, Center, Add

def get_animated_banner():
    banner_logo = """
         ⣴⣶⣄
       ⣴⣿⣇⡙⢿⣷⣄
     ⣴⣿⣿⣄⠨⣍⡀⠙⣿⡇
   ⣴⣿⣿⡈⣉⠛⢷⣌⣻⣿⠟
 ⣴⠿⢋⣉⠻⢧⡈⢴⣦⣾⠟
 ⢿⣷⣌⠁⣶⢌⣿⣾⠟⢡⣶⣄
  ⠙⢿⣷⣤⣾⠟   ⠙⢿⣷⣄
             ⠙⢿⣷⣄
               ⠙⢿⣷⣄
                 ⠙⢿⣷⣄
                   ⠙⡙⣴⣦⠙
                    ⣌⠛⢋⣴
"""
    banner_text = """
  _____ _____  _____  _____ ____  ____          _   _ 
 |  __ \_   _|/ ____|/ ____/ __ \|  _ \   /\   | \ | |
 | |  | || | | (___ | |   | |  | | |_) | /  \  |  \| |
 | |  | || |  \___ \| |   | |  | |  _ < / /\ \ | . ` |
 | |__| || |_ ____) | |___| |__| | |_) / ____ \| |\  |
 |_____/_____|_____/ \_____\____/|____/_/    \_\_| \_|
                                                      
          Discord Mass Reporter by ztnq
"""
    return Colorate.Vertical(Colors.purple_to_blue, Center.XCenter(Add.Add(banner_logo, banner_text, 0)), 1)

def load_tokens(file_path="tokens.txt"):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tokens = [line.strip() for line in f if line.strip()]
        if not tokens:
            raise Exception("No tokens found in tokens.txt.")
        return tokens
    except FileNotFoundError:
        print(f"[ERROR] File not found: {file_path}")
        return []
    except Exception as e:
        print(f"[ERROR] Failed to read tokens: {e}")
        return []

def send_reports():
    url = "https://discord.com/api/v9/reporting/message"
    report_options = {
        "1": ([7, 94], "I don't like this message"),
        "2": ([7, 95], "Spam"),
        "3": ([7, 73, 98], "Harassing me or someone else"),
        "4": ([7, 73, 99], "Using rude, vulgar, or offensive language"),
        "5": ([7, 77, 87, 122], "User is under 13")
    }

    os.system('cls' if os.name == 'nt' else 'clear')
    print(get_animated_banner())
    print("\n--- Provide report details ---")

    channel_id = input("(!) Enter the CHANNEL ID: ").strip()
    message_id = input("(!) Enter the MESSAGE ID to report: ").strip()

    if not all([channel_id, message_id]):
        print("\n[ERROR] Channel ID and message ID are required. Aborting.")
        return

    print("\n--- Select report type ---")
    for key, value in report_options.items():
        print(f"  [{key}] {value[1]}")

    choice = ""
    while choice not in report_options:
        choice = input("\n(?) Enter your choice (1-5): ").strip()
        if choice not in report_options:
            print("[ERROR] Invalid choice. Try again.")

    breadcrumbs = report_options[choice][0]
    reason_text = report_options[choice][1]
    print(f"[*] Report type: {reason_text}")

    try:
        num_reports = int(input("\n(?) How many reports per token? "))
        delay = float(input("(?) Delay between each report (in seconds): "))
    except ValueError:
        print("[ERROR] Invalid number. Aborting.")
        return

    tokens = load_tokens("tokens.txt")
    if not tokens:
        print("[ERROR] No valid tokens to use.")
        return

    print("\n" + "="*50)
    print(f"Starting to send reports using {len(tokens)} token(s)...")
    print("="*50 + "\n")

    total_success = 0
    total_fail = 0

    for token_index, token in enumerate(tokens, start=1):
        print(f"\n🧪 Using token {token_index}/{len(tokens)}")

        headers = {
            'Authorization': token,
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Referer': f'https://discord.com/channels/@me/{channel_id}',
            'Origin': 'https://discord.com',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
        }

        payload = {
            "version": "1.0",
            "variant": "7",
            "language": "en",
            "breadcrumbs": breadcrumbs,
            "elements": {},
            "channel_id": channel_id,
            "message_id": message_id,
            "name": "message"
        }

        for i in range(num_reports):
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=10)
                response_text = response.text.strip() if response.text else "No Response Body"
                print(f"📨 [{i + 1}] Status: {response.status_code} | {response_text}")

                if response.status_code in [200, 204]:
                    print(f"✅ Report sent successfully.")
                    total_success += 1
                elif response.status_code == 401:
                    print(f"❌ Invalid token. Skipping to next.")
                    total_fail += 1
                    break
                elif response.status_code == 429:
                    retry_after = response.json().get('retry_after', delay * 2)
                    print(f"⚠️ Rate limited. Waiting {retry_after:.2f} seconds...")
                    time.sleep(retry_after)
                    continue
                else:
                    print(f"❌ Failed to report. Status: {response.status_code}")
                    total_fail += 1

                if i < num_reports - 1:
                    time.sleep(delay)

            except Exception as e:
                print(f"[ERROR] Exception while reporting: {e}")
                total_fail += 1
                time.sleep(10)

    print("\n" + "="*50)
    print("Reporting process completed.")
    print(f"✅ Total Successes: {total_success}")
    print(f"❌ Total Failures: {total_fail}")
    print("="*50)
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    send_reports()
