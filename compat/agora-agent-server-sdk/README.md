# agora-agent-server-sdk

This package has been renamed to `agora-agents`.

New projects should install:

```sh
pip install agora-agents
```

This compatibility package is kept only to preserve the legacy distribution name during the migration window. It depends on `agora-agents`, which continues to provide the `agora_agent` Python import path.

It intentionally contains only a minimal compatibility module so the distribution can be built and published cleanly with Poetry.
