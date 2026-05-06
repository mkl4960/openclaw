#!/usr/bin/env python3
"""
YouTube Live Link Monitor - Enhanced
Scans laumiex@agentmail.to for emails with "新澤西州宣恩堂中文主日崇拜連結"
and posts YouTube live links to Discord channel 1484402794055336128
"""

import os
import re
import json
import logging
import sys
import subprocess
import shlex
# Suppress root logger to avoid unwanted stdout/stderr messages that OpenClaw would forward as a summary
root_logger = logging.getLogger()
root_logger.handlers.clear()
root_logger.setLevel(logging.WARNING)
from pathlib import Path

# Setup
os.environ.setdefault('PYTHONPATH', '/home/mlau/.nvm/versions/node/v24.14.1/lib/node_modules/openclaw')

# Fixed imports with fallbacks
client = None
def get_agentmail():
    try:
        from agentmail import AgentMail
        return AgentMail()
    except ImportError:
        return None

def send_discord_message(content):
    try:
        # Use OpenClaw CLI to send message (more reliable than tools module)
        result = subprocess.run([
            '/home/mlau/.nvm/versions/node/v24.14.1/bin/openclaw', 'message', 'send',
            '--target', '1484402794055336128',
            '--channel', 'discord',
            '--message', content
        ], capture_output=True, text=True, check=True)
        logger.info(f"✅ Discord notification sent for YouTube link: {content}, result: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ CLI failed: {e.stderr}")
        return False
    except Exception as e:
        logger.error(f"❌ Failed to send Discord notification: {e}")
        return False

# Configuration
AGENTMAIL_EMAIL = "laumiex@agentmail.to"
SEARCH_SUBJECT = "新澤西州宣恩堂中文主日崇拜連結"
YOUTUBE_REGEX = r'https://(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/live/)([a-zA-Z0-9_-]+)'

DATA_DIR = Path.home() / '.openclaw' / 'workspace' / 'data'
# Ensure data and logs directories exist
(DATA_DIR).mkdir(parents=True, exist_ok=True)
(DATA_DIR.parent / 'logs').mkdir(parents=True, exist_ok=True)

# Configure logging: write INFO+ to file, but only WARN+ to stderr (so INFO logs aren't sent to Discord)
logger = logging.getLogger(__name__)
# Ensure a clean logger without inherited handlers
logger.handlers.clear()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# File handler for persistent logs
file_handler = logging.FileHandler(DATA_DIR.parent / 'logs' / 'youtube_monitor.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
# Stream handler for stderr, set to WARNING to avoid INFO messages being forwarded
stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setLevel(logging.WARNING)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
# Prevent propagation to root logger which may also emit to stderr
logger.propagate = False
logger = logging.getLogger(__name__)

def load_sent_links():
    """Load previously sent YouTube link IDs from JSON file."""
    logger.info("Loading sent links...")
    sent_file = DATA_DIR / 'sent_youtube_links.json'
    if sent_file.exists():
        try:
            return set(json.loads(sent_file.read_text()))
        except Exception:
            return set()
    return set()

def save_sent_links(sent):
    logger.info(f"Saving {len(sent)} sent links...")
    sent_file = DATA_DIR / 'sent_youtube_links.json'
    try:
        sent_file.write_text(json.dumps(list(sent), indent=2))
    except Exception as e:
        logger.error(f"Save failed: {e}")

def load_processed_ids():
    processed_file = DATA_DIR / 'processed_message_ids.json'
    if processed_file.exists():
        try:
            return set(json.loads(processed_file.read_text()))
        except Exception:
            return set()
    return set()

def save_processed_ids(processed):
    processed_file = DATA_DIR / 'processed_message_ids.json'
    try:
        processed_file.write_text(json.dumps(list(processed), indent=2))
    except Exception as e:
        logger.error(f"Save processed IDs failed: {e}")

def extract_links(text):
    return re.findall(YOUTUBE_REGEX, text)

def process_message(msg):
    """Extract potential YouTube links from message, scanning full body (including forwarded text) but ignoring attachments."""
    # Ensure the subject matches the filter
    logger.info(f"Subject: {msg.subject}")
    if not msg.subject or SEARCH_SUBJECT not in str(msg.subject):
        return []

    # Build a searchable content string
    parts = [str(msg.subject)]
    # Prefer full text body over extracted text (which may only contain headers)
    if hasattr(msg, 'text') and msg.text:
        parts.append(str(msg.text))
    elif hasattr(msg, 'html') and msg.html:
        parts.append(str(msg.html))
    elif hasattr(msg, 'extracted_text') and msg.extracted_text:
        parts.append(str(msg.extracted_text))
    # Include preview (short snippet) if present
    if hasattr(msg, 'preview') and msg.preview:
        parts.append(str(msg.preview))

    content = " ".join(parts)
    logger.info(f"Message content: {content}")

    # Find YouTube links in the combined content
    youtube_links = extract_links(content)

    # Debug log when a potential reference is seen but no link extracted
    if not youtube_links and 'youtube' in content.lower():
        logger.info(f"Found potential YouTube reference without a link: {content[:100]}...")

    return youtube_links

def main():
    logger.info("🚀 YouTube monitor script started")
    try:
        client = get_agentmail()
        if not client:
            logger.error("AgentMail unavailable")
            return
            
        response = client.inboxes.messages.list(
            inbox_id=AGENTMAIL_EMAIL,
            limit=20
        )
        
        messages = response.messages or []
        logger.info(f"📧 Processing {len(messages)} emails...")
        
        sent_links = load_sent_links()
        processed_ids = load_processed_ids()
        logger.info(f"Loaded {len(sent_links)} previously sent links, {len(processed_ids)} processed message IDs")
        new_count = 0
        processed_changed = False

        for msg in messages:
            # Some SDK versions return dicts; convert to simple object for attribute access
            if isinstance(msg, dict):
                class SimpleMsg:
                    pass
                simple = SimpleMsg()
                for k, v in msg.items():
                    setattr(simple, k, v)
                msg = simple
            msg_id = str(msg.message_id)
            if msg_id in processed_ids:
                logger.info(f"Skipping already-processed message ID: {msg_id}")
                continue
            logger.info(f"Processing message ID: {msg_id}")
            msg = client.inboxes.messages.get(AGENTMAIL_EMAIL, msg.message_id)
            logger.debug(f"Full msg: {vars(msg) if hasattr(msg, '__dict__') else msg}")
            links = process_message(msg)
            processed_ids.add(msg_id)
            processed_changed = True

            for link in links:
                if link not in sent_links:
                    # This is a genuinely new link we haven't announced yet
                    logger.info(f"New YouTube link ID: {link}")
                    message = f"🕊️ Live Stream: https://youtube.com/live/{link}"
                    logger.info(f"➡️ {message}")
                    if send_discord_message(message):
                        sent_links.add(link)
                        new_count += 1
                        logger.info(f"✅ Successfully recorded sent link: {link}")
                    else:
                        logger.error(f"❌ Failed to send Discord notification for link: {link}")
                else:
                    # Already announced; keep quiet to avoid false positives in cron summaries
                    logger.debug(f"Already sent link ID: {link}")
        
        if new_count > 0:
            save_sent_links(sent_links)
            logger.info(f"✅ Sent {new_count} link(s)")
        else:
            logger.info("ℹ️ No new links found")
        if processed_changed:
            save_processed_ids(processed_ids)
            
    except Exception as e:
        logger.error(f"💥 Error: {e}")

if __name__ == "__main__":
    main()