import logging
import os
import sys

from anthropic import Anthropic

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

API_BASE_URL = os.environ.get("API_BASE_URL", "https://open.bigmodel.cn/api/anthropic")
API_KEY = os.environ["API_KEY"]
MODEL = os.environ.get("MODEL", "glm-5")


def send_request():
    client = Anthropic(api_key=API_KEY, base_url=API_BASE_URL)
    log.info("Sending request (model: %s)", MODEL)
    message = client.messages.create(
        model=MODEL,
        max_tokens=50,
        messages=[
            {"role": "user", "content": "Hello! This is a scheduled check-in. Reply with one sentence."},
        ],
    )
    content = message.content[0].text
    log.info("Response: %s", content)


def main():
    try:
        send_request()
    except Exception:
        log.exception("Request failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
