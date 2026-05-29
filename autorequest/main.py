import json
import logging
import os
import sys

import httpx
from anthropic import Anthropic

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

PROVIDERS = json.loads(os.environ["PROVIDERS"])
PROMPT = "Hello! This is a scheduled check-in. Reply with one sentence."


def send_anthropic(provider):
    client = Anthropic(api_key=provider["api_key"], base_url=provider["base_url"])
    message = client.messages.create(
        model=provider["model"],
        max_tokens=50,
        messages=[{"role": "user", "content": PROMPT}],
    )
    return message.content[0].text


def send_openai(provider):
    url = f"{provider['base_url'].rstrip('/')}/chat/completions"
    resp = httpx.post(
        url,
        headers={"Authorization": f"Bearer {provider['api_key']}"},
        json={
            "model": provider["model"],
            "messages": [{"role": "user", "content": PROMPT}],
            "max_tokens": 50,
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


SENDERS = {
    "anthropic": send_anthropic,
    "openai": send_openai,
}


def send_request(provider):
    name = provider.get("name", provider["model"])
    api_type = provider.get("api_type", "anthropic")
    sender = SENDERS.get(api_type)
    if not sender:
        raise ValueError(f"Unknown api_type: {api_type}")

    log.info("[%s] Sending request (%s)...", name, api_type)
    content = sender(provider)
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
