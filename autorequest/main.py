import json
import logging
import os
import sys

from anthropic import Anthropic

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

PROVIDERS = json.loads(os.environ["PROVIDERS"])


def send_request(provider):
    name = provider.get("name", provider["model"])
    client = Anthropic(api_key=provider["api_key"], base_url=provider["base_url"])
    log.info("[%s] Sending request...", name)
    message = client.messages.create(
        model=provider["model"],
        max_tokens=50,
        messages=[
            {"role": "user", "content": "Hello! This is a scheduled check-in. Reply with one sentence."},
        ],
    )
    content = message.content[0].text
    log.info("[%s] Response: %s", name, content)


def main():
    targets = [p for p in PROVIDERS if p.get("enabled", True)]
    if not targets:
        log.warning("No enabled providers, skipping.")
        return

    failed = False
    for provider in targets:
        try:
            send_request(provider)
        except Exception:
            log.exception("[%s] Request failed", provider.get("name", provider["model"]))
            failed = True

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
