import pytest

from agora_agent import (
    AgentClient,
    Area,
    AgoraAgent,
    DeepgramSTT,
)


def _client(area: Area) -> AgentClient:
    return AgentClient(area=area, app_id="0" * 32, app_certificate="1" * 32)


def test_cn_client_exposes_cn_vendor_catalog() -> None:
    client = _client(Area.CN)

    assert client.area_scope == "cn"
    assert client.vendors.stt.tencent is not None
    assert client.vendors.tts.bytedance is not None
    assert client.vendors.llm.deepseek is not None
    assert client.vendors.avatar.sensetime is not None
    assert not hasattr(client.vendors.stt, "deepgram")
    assert client.vendors.stt.xfyun is not client.vendors.stt.xfyun_bigmodel
    assert client.vendors.stt.xfyun is not client.vendors.stt.xfyun_dialect
    assert client.create_agent().__class__.__name__ == "CNAgent"


def test_global_client_exposes_global_vendor_catalog() -> None:
    client = _client(Area.US)

    assert client.area_scope == "global"
    assert client.vendors.stt.deepgram is not None
    assert client.vendors.tts.elevenlabs is not None
    assert client.vendors.llm.openai is not None
    assert client.vendors.avatar.liveavatar is not None
    assert not hasattr(client.vendors.avatar, "sensetime")
    assert client.create_agent().__class__.__name__ == "GlobalAgent"


def test_shared_vendor_names_use_distinct_cn_and_global_classes() -> None:
    cn_client = _client(Area.CN)
    global_client = _client(Area.US)

    assert cn_client.vendors.tts.minimax is not global_client.vendors.tts.minimax
    assert cn_client.vendors.tts.microsoft is not global_client.vendors.tts.microsoft
    assert cn_client.vendors.stt.microsoft is not global_client.vendors.stt.microsoft


def test_regional_agent_builder_preserves_agent_kwargs() -> None:
    cn_agent = AgoraAgent(client=_client(Area.CN), name="cn-support", turn_detection={"language": "zh-CN"})
    global_agent = AgoraAgent(client=_client(Area.US), name="us-support", turn_detection={"language": "en-US"})

    assert cn_agent.__class__.__name__ == "CNAgent"
    assert cn_agent.name == "cn-support"
    assert global_agent.__class__.__name__ == "GlobalAgent"
    assert global_agent.name == "us-support"


def test_cn_client_rejects_global_only_vendor() -> None:
    client = _client(Area.CN)
    agent = AgoraAgent(client=client, name="cn-agent").with_stt(
        DeepgramSTT(api_key="dg-key", model="nova-2", language="en-US")
    )

    with pytest.raises(ValueError, match="area scope 'cn'"):
        agent.create_session(
            channel="room",
            token="rtc-token",
            agent_uid="1",
            remote_uids=["100"],
        ).start()


def test_global_client_rejects_cn_only_vendor() -> None:
    client = _client(Area.US)
    tencent_stt = __import__("agora_agent").TencentSTT(
        key="sec", app_id="appid", secret="secret", engine_model_type="16k_zh", voice_id="voice"
    )
    agent = AgoraAgent(client=client, name="global-agent").with_stt(tencent_stt)

    with pytest.raises(ValueError, match="area scope 'global'"):
        agent.create_session(
            channel="room",
            token="rtc-token",
            agent_uid="1",
            remote_uids=["100"],
        ).start()
