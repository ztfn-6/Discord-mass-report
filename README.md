# 🚀 More reports incoming soon

# 🚨 Discord Mass Reporter

**⚠️ Warning**  
This tool is strictly for **educational purposes**. Automating reports on Discord violates its Terms of Service and can result in permanent bans. Use at your own risk.

---

## 🧰 Features

- Choose from multiple report types (spam, harassment, etc.)
- Specify number of reports and delay between each
- Handles rate limits (`429 Too Many Requests`)
- Colorful animated console banner using `pystyle`

---

## 📋 Requirements

- Python 3.7+
- pip (Python package installer)

### Installation

```bash
git clone https://github.com/ztfn-6/Discord-mass-report.git
cd Discord-mass-report
pip install -r requirements.txt
```

---

## ⚙️ Usage

Run the script with:

```bash
python main.py
```

Then follow the prompts:

1. **Authorization Token** – Your Discord token (keep this private!)
2. **Channel ID** – The ID of the channel containing the target message
3. **Message ID** – The ID of the message you want to report
4. **Choose report reason**:
   ```
   [1] I don't like this message
   [2] Spam
   [3] Harassing me or someone else
   [4] Using rude, vulgar, or offensive language
   [5] User is under 13
   ```
5. Enter how many reports to send and the delay (in seconds) between them

---

## 🔍 How It Works

- Sends POST requests to Discord's internal API:
  `https://discord.com/api/v9/reporting/message`
- Includes custom headers and dynamic payload depending on your choices
- Shows each API response (status code and message)
- Handles rate limiting with cooldowns

---

## ⚠️ Disclaimer

- **This project is for educational purposes only.**
- Using it for real abuse may get your account or IP permanently banned.
- Never use your main account.
- Never share your token with anyone.

---

## 🛠️ Contributing

Pull requests are welcome. Feel free to fork and improve features such as:
- Multi-token support
- Proxies
- GUI or web interface

---

## 📚 Requirements

Add this to your `requirements.txt`:

```text
requests
pystyle
```

---