# Twitter AI Bot with TinyLlama

A Python-based Twitter bot that uses TinyLlama (via Ollama) to analyze tweets offline and interact with posts related to anime, ml etc. The bot logs into Twitter using Selenium with Brave browser, scrolls the feed, likes, and replies with short, relevant responses (up to 50 characters).

## Features
- **Offline AI Processing:** Uses TinyLlama via Ollama for lightweight, CPU-friendly tweet analysis.
- **Interest-Based Interaction:** Targets tweets with keywords: "anime," "wine," "weed."
- **Clean Replies:** Generates concise replies (e.g., "Love anime! What's your favorite?").
- **Selenium Automation:** Interacts with Twitter using Brave browser and ChromeDriver.
- **Environment Variables:** Securely handles Twitter credentials.

## Prerequisites
- **OS:** Ubuntu (or Linux-based system)
- **Browser:** Brave (`/usr/bin/brave-browser`)
- **ChromeDriver:** Version matching Brave
- **Python:** 3.8+
- **Ollama:** For running TinyLlama locally
- **Twitter Account:** Valid credentials

## Setup

### 1. Clone the Repository
```bash
git clone https://github.com/DomiGames/xbot.git
cd xbot
```
### 2.  Install Ollama
Install Ollama and pull the TinyLlama model:
```bash
curl -fsSL https://ollama.com/install.sh | sh
sudo systemctl start ollama
sudo systemctl enable ollama
ollama pull tinyllama
```
Verify Ollama and model:
```bash
ollama --version
ollama list
```
###  3. Test Ollama
Test TinyLlama in your terminal:
```bash
ollama run tinyllama
```
Enter:
```bash
Generate a short reply (up to 50 characters) about anime.
```
Expect a response like:
```bash
Love anime! What's your favorite show?
```
Exit with Ctrl+D.

###  4. Install ChromeDriver
Check your Brave version at brave://version. Download the matching ChromeDriver
```bash
wget https://storage.googleapis.com/chrome-for-testing-public/135.0.7049.115/linux64/chromedriver-linux64.zip
unzip chromedriver-linux64.zip
sudo mv chromedriver-linux64/chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
```

###  5. Set Up Python Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

###  6. Configure Twitter Credentials
Set environment variables
```bash
export TWITTER_USERNAME="your_username"
export TWITTER_PASSWORD="your_password"
echo 'export TWITTER_USERNAME="your_username"' >> ~/.bashrc
echo 'export TWITTER_PASSWORD="your_password"' >> ~/.bashrc
source ~/.bashrc
```

###  Usage
Run the bot
```bash
source venv/bin/activate
python3 xbot.py
```
The bot will:Log into Twitter.
Scroll the feed three times, processing up to five tweets per scroll.
Analyze tweets with TinyLlama (offline).
Like and reply with short responses (e.g., "Love anime! What's your favorite?").

NotesTwitter Automation Rules: Limit interactions to <50 daily actions to avoid bans. Use a test account. Resolve CAPTCHAs manually.
Content Warning: Keywords like "weed" may trigger Twitter’s content moderation. Consider safer keywords (e.g., "python," "ai").
Performance: TinyLlama requires ~1-2GB RAM. Reduce num_predict in xbot.py if slow.
Tweet Extraction: If Twitter’s UI changes, update get_tweet_text selectors (e.g., [data-testid="tweetText"] or div[lang]).








