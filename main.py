import requests
import time
import json
import os
from pystyle import Colorate, Colors, Center, Add

# ####################################################################################
# IMPORTANT WARNING:
# 1. ACCOUNT AUTOMATION: Using scripts to automate actions like this violates
#    Discord's Terms of Service and can result in a permanent BAN of your account.
# 2. SECURITY: Your authorization token is like your password.
#    NEVER share it with anyone. If someone gets your token, they can control your account.
# 3. RESPONSIBILITY: This script is provided for educational purposes only.
#    Misuse is entirely your own responsibility.
# ####################################################################################

def get_animated_banner():
    """Generates and returns the animated banner text."""
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
    # The Colorate.Vertical function provides a shimmering/animated effect as it prints
    return Colorate.Vertical(Colors.purple_to_blue, Center.XCenter(Add.Add(banner_logo, banner_text, 0)), 1)

def send_reports():
    """Main function to handle the reporting process."""
    url = "https://discord.com/api/v9/reporting/message"

    # Maps user choice to the correct breadcrumbs for the payload
    report_options = {
        "1": ([7, 94], "I don't like this message"),
        "2": ([7, 95], "Spam"),
        "3": ([7, 73, 98], "Harassing me or someone else"),
        "4": ([7, 73, 99], "Using rude, vulgar, or offensive language"),
        "5": ([7, 77, 87, 122], "User is under 13 (Original report type)") # The one you had before
    }

    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(get_animated_banner())
        print("\n--- Please provide the details for the report ---")
        auth_token = input("(!) Enter your authorization TOKEN: ").strip()
        channel_id = input("(!) Enter the CHANNEL ID: ").strip()
        message_id = input("(!) Enter the MESSAGE ID to report: ").strip()

        if not all([auth_token, channel_id, message_id]):
            print("\n[ERROR] All fields (token, channel ID, message ID) are required. Aborting.")
            return

        # --- Report Type Selection Menu ---
        print("\n--- Select the type of report ---")
        for key, value in report_options.items():
            print(f"  [{key}] {value[1]}")
        
        choice = ""
        while choice not in report_options:
            choice = input("\n(?) Enter your choice (1-5): ").strip()
            if choice not in report_options:
                print("[ERROR] Invalid choice. Please select a number from the list.")

        selected_breadcrumbs = report_options[choice][0]
        selected_reason_text = report_options[choice][1]
        print(f"[*] Report type selected: {selected_reason_text}")
        
        # --- Continue with quantity and delay ---
        num_reports = int(input("\n(?) How many reports do you want to send? "))
        delay = float(input("(?) What is the delay in seconds between each report? (e.g., 1.5): "))

    except ValueError:
        print("\n[ERROR] The number of reports and the delay must be valid numbers. Aborting.")
        return
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred during setup: {e}")
        return

    headers = {
        'Authorization': auth_token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': f'https://discord.com/channels/@me/{channel_id}',
        'Origin': 'https://discord.com',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    payload = {
        "version": "1.0",
        "variant": "7",
        "language": "en",
        "breadcrumbs": selected_breadcrumbs, # <-- This is now dynamic based on user choice
        "elements": {},
        "channel_id": channel_id,
        "message_id": message_id,
        "name": "message"
    }

    print("\n" + "="*50)
    print(f"Starting to send {num_reports} report(s)...")
    print("Press Ctrl+C to stop at any time.")
    print("="*50 + "\n")

    success_count = 0
    fail_count = 0

    for i in range(num_reports):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)

            response_text = response.text.strip() if response.text else "No Response Body"
            print(f"📨 API Response [{i + 1}]: {response.status_code} | {response_text}")

            if response.status_code in [200, 204]:
                print(f"✅ Report [{i + 1}/{num_reports}] sent successfully!")
                success_count += 1
            elif response.status_code == 401:
                print(f"❌ Report [{i + 1}/{num_reports}] FAILED. AUTHENTICATION error. Check your token. Aborting.")
                fail_count += 1
                break
            elif response.status_code == 429:
                retry_after = response.json().get('retry_after', delay * 2)
                print(f"⚠️ Rate Limited! Waiting for {retry_after:.2f} seconds...")
                time.sleep(retry_after)
                # We don't increment i here, we just retry the same report after the cooldown
                continue
            else:
                print(f"❌ Report [{i + 1}/{num_reports}] FAILED.")
                fail_count += 1

            if i < num_reports - 1:
                time.sleep(delay)

        except requests.exceptions.RequestException as e:
            print(f"❌ Connection error on report [{i + 1}]: {e}")
            fail_count += 1
            print("Waiting 10 seconds before trying again...")
            time.sleep(10)
        except KeyboardInterrupt:
            print("\n\n[INFO] Operation interrupted by user.")
            break
        except Exception as e:
            print(f"\n[ERROR] An unexpected error occurred during sending: {e}")
            fail_count += 1
            break

    print("\n" + "="*50)
    print("Process finished.")
    print(f"✅ Successes: {success_count}")
    print(f"❌ Failures: {fail_count}")
    print("="*50)
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    send_reports()
