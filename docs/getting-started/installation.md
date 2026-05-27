---
sidebar_position: 1
title: Installation
description: Install the Agora Conversational AI Python SDK.
---

# Installation

## Prerequisites

- Python >= 3.8

## Install with pip

```sh
pip install agora-agents
```

## Install with Poetry

```sh
poetry add agora-agents
```

## Imports

```python
from agora_agent import Agent, Agora, Area, DeepgramSTT, OpenAI
```

The package installs as `agora-agents` and imports as `agora_agent`.

## Sync vs. Async

The SDK supports both synchronous and asynchronous usage:

- **Synchronous** — import `Agora` from `agora_agent` and use blocking method calls
- **Asynchronous** — import `AsyncAgora` and `AsyncAgentSession` from `agora_agent` and use `await` with all API calls

```python
# Sync
from agora_agent import Agora, Area

# Async
from agora_agent import AsyncAgora, AsyncAgentSession, Area
```

## Dependencies

| Package                        | Purpose                                                |
| ------------------------------ | ------------------------------------------------------ |
| `httpx` (>= 0.21.2)            | HTTP client for sync and async requests                |
| `pydantic` (>= 1.9.2)          | Data validation for vendor configuration and API types |
| `typing_extensions` (>= 4.0.0) | Backported type hints for Python 3.8+                  |

See [Authentication](./authentication.md) for setup details.
