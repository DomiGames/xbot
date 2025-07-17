from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import ollama
import time
import random
import os

class TwitterBot:
    def __init__(self, username, password):
        # Set up Brave browser with ChromeDriver
        options = webdriver.ChromeOptions()
        options.binary_location = "/usr/bin/brave-browser"  # Brave APT path
        options.add_argument("--disable-blink-features=AutomationControlled")  # Anti-detection
        options.add_argument("--no-sandbox")  # Mitigate DevToolsActivePort
        options.add_argument("--disable-dev-shm-usage")
        service = Service("/usr/local/bin/chromedriver")
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 10)
        self.username = username
        self.password = password
        # Define interests (keywords)
        self.interests = ["anime", "ml", "ai", "automation", "build"]  # Removed problematic keywords

    def login(self):
        """Log in to Twitter."""
        self.driver.get("https://twitter.com/login")
        time.sleep(5)

        try:
            # Enter username
            username_field = self.wait.until(EC.presence_of_element_located((By.NAME, "text")))
            username_field.send_keys(self.username)
            username_field.send_keys(Keys.ENTER)
            time.sleep(2)

            # Enter password
            password_field = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
            password_field.send_keys(self.password)
            password_field.send_keys(Keys.ENTER)
            time.sleep(3)

            # Verify login
            current_url = self.driver.current_url
            if "home" not in current_url.lower():
                raise Exception(f"Login failed, current URL: {current_url}")
            print("Login successful, on home page")
        except Exception as e:
            print(f"Login failed: {e}")
            self.driver.quit()
            raise

    def scroll(self, scrolls=1):
        """Scroll through the Twitter feed."""
        for _ in range(scrolls):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)

    def analyze_tweet(self, tweet_text):
        """Use TinyLlama via Ollama to generate a reply if tweet matches interests."""
        # Check for interest keywords
        tweet_lower = tweet_text.lower()
        is_interesting = any(keyword in tweet_lower for keyword in self.interests)
        if not is_interesting:
            return False, None

        # Generate a reply using Ollama
        prompt = f"Generate a short, positive reply (up to 50 characters) about {', '.join(self.interests)} based on this tweet: {tweet_text}"
        try:
            response = ollama.generate(
                model="tinyllama",
                prompt=prompt,
                options={
                    "num_predict": 50,
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            )
            reply = response["response"].strip()
            # Clean reply to remove prompt or tweet text
            reply = reply.replace(tweet_text, "").replace(prompt, "").strip()
            # Ensure reply is short and valid
            if not reply or len(reply) < 10:
                reply = f"Cool tweet about {random.choice(self.interests)}!"
            if len(reply) > 280:
                reply = reply[:277] + "..."
        except Exception as e:
            print(f"Error generating reply: {e}")
            reply = f"Cool tweet about {random.choice(self.interests)}!"

        return True, reply

    def like_tweet(self, tweet_element):
        """Like a tweet."""
        try:
            like_button = tweet_element.find_element(By.CSS_SELECTOR, '[data-testid="like"]')
            like_button.click()
            time.sleep(random.uniform(1, 3))
        except Exception as e:
            print(f"Could not like tweet: {e}")

    def reply_to_tweet(self, tweet_element, reply_text):
        """Reply to a tweet."""
        try:
            reply_button = tweet_element.find_element(By.CSS_SELECTOR, '[data-testid="reply"]')
            reply_button.click()
            time.sleep(1)

            reply_field = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweetTextarea_0"]')))
            reply_field.send_keys(reply_text)
            reply_field.send_keys(Keys.ENTER)
            time.sleep(random.uniform(2, 4))
        except Exception as e:
            print(f"Could not reply to tweet: {e}")

    def get_tweet_text(self, tweet_element):
        """Extract tweet text with fallback selectors."""
        try:
            text_element = tweet_element.find_element(By.CSS_SELECTOR, '[data-testid="tweetText"]')
            return text_element.text
        except:
            try:
                text_element = tweet_element.find_element(By.CSS_SELECTOR, 'div[lang], span')
                return text_element.text
            except Exception as e:
                print(f"Could not extract tweet text: {e}")
                return ""

    def run(self):
        """Run the bot to analyze and interact with tweets."""
        self.login()
        time.sleep(5)

        for _ in range(3):  # Reduced scrolls to avoid rate limiting
            self.scroll()
            try:
                tweets = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid="tweet"]')))
                print(f"Found {len(tweets)} tweets")
                for tweet in tweets[:5]:  # Process up to 5 tweets
                    tweet_text = self.get_tweet_text(tweet)
                    if not tweet_text:
                        continue

                    # Analyze tweet with TinyLlama
                    is_interesting, reply_text = self.analyze_tweet(tweet_text)
                    if is_interesting:
                        print(f"Interesting tweet: {tweet_text}")
                        print(f"Replying with: {reply_text}")
                        self.like_tweet(tweet)
                        self.reply_to_tweet(tweet, reply_text)
                time.sleep(random.uniform(5, 10))
            except Exception as e:
                print(f"Error processing tweets: {e}")
        self.driver.quit()

if __name__ == "__main__":
    bot = TwitterBot(os.getenv("TWITTER_USERNAME"), os.getenv("TWITTER_PASSWORD"))
    bot.run()
