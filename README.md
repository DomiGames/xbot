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
