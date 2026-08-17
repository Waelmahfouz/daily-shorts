#!/usr/bin/env python3
"""
Pick a fresh short-video topic in your niche each day using Groq (free).
Reads the niche from niche.txt. If niche.txt has several lines, it rotates
through them by day so each niche gets a turn.

Outputs (to GitHub Actions): topic, title, caption.
If anything fails, it falls back to using the raw niche as the topic so the
video still gets made.
"""

import os
import json
import datetime
import urllib.request
import urllib.error

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "openai/gpt-oss-20b"


def read_niche() -> str:
    try:
        with open("niche.txt", "r", encoding="utf-8") as f:
            lines = [ln.strip() for ln in f if ln.strip() and not ln.strip().startswith("#")]
    except FileNotFoundError:
        lines = []
    if not lines:
        return "interesting science facts"
    # Rotate through multiple niches by day-of-year.
    day = datetime.date.today().timetuple().tm_yday
    return lines[day % len(lines)]


def ask_groq(niche: str, api_key: str) -> dict:
    today = datetime.date.today().isoformat()
    system = (
        "You are a short-form video producer. You output ONLY compact JSON."
    )
    user = (
        f"Niche: {niche}\n"
        f"Today: {today}\n\n"
        "Propose ONE fresh, specific, engaging topic for a 30-60 second vertical "
        "short video in this niche. Avoid generic or repetitive angles. Then write "
        "a punchy title and a caption with 3-5 relevant hashtags.\n\n"
        "Return ONLY this JSON, nothing else:\n"
        '{"topic": "...", "title": "...", "caption": "..."}\n'
        "Rules: topic <= 14 words; title <= 70 characters; caption <= 200 characters."
    )
    body = json.dumps({
        "model": MODEL,
        "temperature": 1.0,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "response_format": {"type": "json_object"},
    }).encode("utf-8")

    req = urllib.request.Request(
        GROQ_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    content = data["choices"][0]["message"]["content"]
    return json.loads(content)


def write_output(topic: str, title: str, caption: str) -> None:
    out_path = os.environ.get("GITHUB_OUTPUT")
    fields = {"topic": topic, "title": title, "caption": caption}
    if not out_path:
        print(json.dumps(fields, ensure_ascii=False))
        return
    with open(out_path, "a", encoding="utf-8") as f:
        for name, value in fields.items():
            f.write(f"{name}<<GHEOF\n{value}\nGHEOF\n")


def main() -> None:
    override = os.environ.get("TOPIC_OVERRIDE", "").strip()
    niche = read_niche()
    api_key = os.environ.get("GROQ_API_KEY", "").strip()

    if override:
        topic = override
        title = override
        caption = f"{override}"
        print(f"Using manual topic override: {topic}")
        write_output(topic, title, caption)
        return

    try:
        result = ask_groq(niche, api_key)
        topic = (result.get("topic") or niche).strip()
        title = (result.get("title") or topic).strip()
        caption = (result.get("caption") or topic).strip()
        print(f"Niche: {niche}")
        print(f"Chosen topic: {topic}")
    except Exception as e:  # noqa: BLE001
        print(f"Topic generation failed ({e!r}); falling back to raw niche.")
        topic = niche
        title = niche
        caption = niche

    write_output(topic, title, caption)


if __name__ == "__main__":
    main()
