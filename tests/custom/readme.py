"""README Quick Start example — runnable with:

    python tests/custom/readme.py

Requires AGORA_APP_ID and AGORA_APP_CERTIFICATE in the environment.
Install project dependencies first (``pip install -e .`` or ``poetry install``).
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

from agora_agent.agentkit.vendors.cn import TencentSTT

_SRC = Path(__file__).resolve().parents[2] / "src"
if _SRC.is_dir() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from agora_agent import (  # noqa: E402
    Agent,
    Agora,
    Area,
    DeepgramSTT,
    MiniMaxTTS,
    OpenAI,
    expires_in_hours,
)

AGENT_PROMPT = (
    "You are a concise, technically credible voice assistant. "
    "Keep replies short unless the user asks for detail."
)

GREETING = "Hi there! I am your Agora voice assistant. How can I help?"


def start_conversation() -> str:
    app_id = os.environ["AGORA_APP_ID"]
    app_certificate = os.environ["AGORA_APP_CERTIFICATE"]

    client = Agora(
        area=Area.US,
        app_id=app_id,
        app_certificate=app_certificate,
    )

    agent = (
        Agent(client=client, turn_detection={"language": "en-US"})
        .with_stt(DeepgramSTT(model="nova-3", language="en"))
        .with_llm(
            OpenAI(
                model="gpt-4o-mini",
                system_messages=[{"role": "system", "content": AGENT_PROMPT}],
                greeting_message=GREETING,
                failure_message="Please wait a moment.",
                max_history=50,
                params={
                    "max_tokens": 1024,
                    "temperature": 0.7,
                    "top_p": 0.95,
                },
            )
        )
        .with_tts(
            MiniMaxTTS(
                model="speech_2_6_turbo",
                voice_id="English_captivating_female1",
            )
        )
    )

    session = agent.create_session(
        channel=f"demo-channel-{int(time.time())}",
        agent_uid="123456",
        remote_uids=["*"],
        name=f"conversation-{int(time.time())}",
        idle_timeout=30,
        expires_in=expires_in_hours(1),
        debug=True,
    )

    return session.start()


if __name__ == "__main__":
    missing = [
        name
        for name in ("AGORA_APP_ID", "AGORA_APP_CERTIFICATE")
        if not os.environ.get(name)
    ]
    if missing:
        raise SystemExit(
            f"Missing required environment variables: {', '.join(missing)}"
        )

    print(f"Agent started: {start_conversation()}")
