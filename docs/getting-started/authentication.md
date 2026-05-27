---
sidebar_position: 2
title: Authentication
description: Configure the Python SDK with app credentials and understand other supported auth modes.
---

# Authentication

Create `Agora` or `AsyncAgora` with `app_id` and `app_certificate` only. The SDK mints a fresh ConvoAI REST token for each API call and generates the RTC join token when the session starts.

## App credentials

```python
from agora_agent import Agent, Agora, Area, DeepgramSTT, OpenAI, MiniMaxTTS

client = Agora(
    area=Area.US,
    app_id="your-app-id",
    app_certificate="your-app-certificate",
)

agent = (
    Agent(instructions="Be concise.")
    .with_stt(DeepgramSTT(model="nova-3"))
    .with_llm(OpenAI(model="gpt-4o-mini"))
    .with_tts(MiniMaxTTS(model="speech_2_6_turbo", voice_id="English_captivating_female1"))
)

session = agent.create_session(
    client,
    channel="room-123",
    agent_uid="1",
    remote_uids=["100"],
)
```

## Why app credentials

- Fresh short-lived tokens per API call instead of reusing long-lived credentials
- No Customer ID / Customer Secret in request headers
- No manual REST or RTC token provisioning in application code

## Inspecting auth mode

```python
print(client.auth_mode)  # "app-credentials"
```

## Other auth modes

The SDK also supports pre-minted REST tokens and HTTP Basic Auth for legacy integrations. These are not recommended for new applications.

### Token auth (`auth_token`)

Pass a pre-minted Agora REST token on the client. You must also supply the RTC join token on `create_session(..., token=...)`.

```python
client = Agora(
    area=Area.US,
    app_id="your-app-id",
    app_certificate="your-app-certificate",
    auth_token="your-rest-auth-token",
)

session = agent.create_session(
    client,
    channel="room-123",
    agent_uid="1",
    remote_uids=["100"],
    token="your-rtc-join-token",
)
```

### Basic Auth (`customer_id` + `customer_secret`)

Uses HTTP Basic Auth with Customer ID and Secret from Agora Console. Avoid for new integrations — the same credentials are sent on every request instead of minting fresh tokens.

```python
client = Agora(
    area=Area.US,
    app_id="your-app-id",
    app_certificate="your-app-certificate",
    customer_id="your-customer-id",
    customer_secret="your-customer-secret",
)
```
