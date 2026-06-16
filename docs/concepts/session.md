---
sidebar_position: 3
title: AgentSession
description: Manage the full lifecycle of a running Agora Conversational AI agent.
---

# AgentSession

`AgentSession` (sync) and `AsyncAgentSession` (async) manage the lifecycle of a running AI agent. They handle starting, stopping, sending speech, interrupting, updating configuration, and retrieving history.

Presets are configured at session creation time when you use them explicitly. Most applications should configure vendors on the `Agent` builder instead — see [Quick Start](../getting-started/quick-start.md).

## State Machine

An agent session moves through these states:

```
idle → starting → running → stopping → stopped
                    ↓
                  error
```

| State | Description |
|---|---|
| `idle` | Session created, not yet started |
| `starting` | `start()` called, waiting for API response |
| `running` | Agent is active and processing audio |
| `stopping` | `stop()` called, waiting for graceful shutdown |
| `stopped` | Agent has stopped (can be restarted) |
| `error` | An error occurred (can be restarted) |

You can check the current state with `session.status`.

## Creating a Session

Use `Agent.create_session()` to create a session:

<!-- snippet: executable -->
```python
from agora_agent import Agent, Agora, Area

client = Agora(area=Area.US, app_id='your-app-id', app_certificate='your-app-certificate')

agent = (
    Agent(client=client, name='my-agent')
    .with_llm(client.vendors.llm.openai(
        api_key='your-openai-key',
        base_url='https://api.openai.com/v1/chat/completions',
        model='gpt-4o-mini',
        system_messages=[{'role': 'system', 'content': 'You are helpful.'}],
    ))
    .with_tts(client.vendors.tts.elevenlabs(key='your-elevenlabs-key', model_id='eleven_flash_v2_5', voice_id='your-voice-id', base_url='wss://api.elevenlabs.io/v1'))
    .with_stt(client.vendors.stt.deepgram(api_key='your-deepgram-key', language='en-US'))
)

session = agent.create_session(channel='my-channel', agent_uid='1', remote_uids=['100'])
```

## Sync Methods

<!-- snippet: fragment -->
```python
# Start the agent — returns the agent ID
agent_id = session.start()

# Send text to be spoken
session.say('Hello! How can I help?')

# Send with priority and interruptability
session.say('Important message', priority='INTERRUPT', interruptable=False)

# Interrupt the agent while speaking
session.interrupt()

# Update agent configuration at runtime
session.update(properties)

# Get conversation history
history = session.get_history()

# Get current session info
info = session.get_info()

# Stop the agent
session.stop()
```

## Async Methods

`AsyncAgentSession` provides the same methods as coroutines. Every call that makes an HTTP request requires `await`:

<!-- snippet: fragment -->
```python
agent_id = await session.start()
await session.say('Hello! How can I help?')
await session.say('Important message', priority='INTERRUPT', interruptable=False)
await session.interrupt()
await session.update(properties)
history = await session.get_history()
info = await session.get_info()
await session.stop()
```

## Method Comparison

| Action | Sync (`AgentSession`) | Async (`AsyncAgentSession`) |
|---|---|---|
| Start | `session.start()` → `str` | `await session.start()` → `str` |
| Stop | `session.stop()` → `None` | `await session.stop()` → `None` |
| Say | `session.say(text)` → `None` | `await session.say(text)` → `None` |
| Interrupt | `session.interrupt()` → `None` | `await session.interrupt()` → `None` |
| Update | `session.update(props)` → `None` | `await session.update(props)` → `None` |
| History | `session.get_history()` → response | `await session.get_history()` → response |
| Info | `session.get_info()` → response | `await session.get_info()` → response |

## Agora-managed models and BYOK

When you omit credentials for supported Agora-managed global models on the builder, AgentKit sends the matching Agora-managed configuration at session start. Pass your own vendor API keys when you need BYOK. CN MiniMax TTS is not Agora-managed in the same way and typically includes `key`.

<!-- snippet: fragment -->
```python
from agora_agent import Agent, DeepgramSTT, OpenAI, OpenAITTS

agent = (
    Agent()
    .with_stt(DeepgramSTT(model="nova-3", language="en-US"))
    .with_llm(OpenAI(
        model="gpt-4o-mini",
        system_messages=[{"role": "system", "content": "Be concise."}],
    ))
    .with_tts(OpenAITTS(voice="alloy"))
)
```

For explicit project-specific preset values and the full list of Agora-managed models, see [AgentSession Reference](../reference/session.md).

## Events

Both `AgentSession` and `AsyncAgentSession` support event handlers via `on()` and `off()`:

<!-- snippet: fragment -->
```python
def on_started(data):
    print(f'Agent started: {data["agent_id"]}')

def on_stopped(data):
    print(f'Agent stopped: {data["agent_id"]}')

def on_error(error):
    print(f'Error: {error}')

session.on('started', on_started)
session.on('stopped', on_stopped)
session.on('error', on_error)

# Remove a handler
session.off('started', on_started)
```

| Event | Payload | When |
|---|---|---|
| `started` | `{"agent_id": str}` | Agent successfully started |
| `stopped` | `{"agent_id": str}` | Agent successfully stopped |
| `error` | `Exception` | An error occurred during any operation |

## Properties

| Property | Type | Description |
|---|---|---|
| `session.id` | `Optional[str]` | The agent ID (set after `start()`) |
| `session.status` | `str` | Current state (`idle`, `starting`, `running`, etc.) |
| `session.agent` | `Agent` | The agent configuration |
| `session.app_id` | `str` | The Agora App ID |
| `session.raw` | `AgentsClient` | Direct access to the Fern-generated agents client |

## Direct API access with `session.raw`

If AgentKit does not yet expose a method for a new API endpoint, use `session.raw` to access the generated `AgentsClient` (sync) or `AsyncAgentsClient` (async) directly:

<!-- snippet: fragment -->
```python
# Access any generated REST method
response = session.raw.list(session.app_id)
```

## Error Handling

Session methods raise `RuntimeError` if called in an invalid state:

<!-- snippet: fragment -->
```python
session = agent.create_session(channel='my-channel', agent_uid='1', remote_uids=['100'])

# This raises RuntimeError — session hasn't started yet
session.say('Hello!')  # RuntimeError: Cannot say in idle state
```

The `stop()` method handles already-stopped agents gracefully — if the API returns a 404 (agent already gone), the session transitions to `stopped` without raising.
