"""Golden-master snapshots for the trickiest vendor transformations.

These freeze to_config() output BEFORE the collapse refactor and must stay green
throughout it. The broader tests/custom/test_*_vendors.py suite guards the rote
classes; this file targets the classes with custom __init__, sample_rate logic,
cross-vendor inheritance, or aliases.
"""
from agora_agent import (
    DeepgramSTT,
    ElevenLabsTTS,
    GoogleTTS,
    OpenAITTS,
    OpenAI,
    Groq,
    CustomLLM,
    VertexAILLM,
)
from agora_agent.agentkit.vendors.cn import AliyunLLM, FengmingSTT, SenseTimeAvatar
from agora_agent.agentkit.vendors.avatar import HeyGenAvatar


def test_deepgram_stt_golden() -> None:
    cfg = DeepgramSTT(model="nova-3", language="en-US", smart_format=True).to_config()
    assert cfg == {
        "vendor": "deepgram",
        "params": {"model": "nova-3", "language": "en-US", "smart_format": True},
    }


def test_elevenlabs_sample_rate_field_golden() -> None:
    tts = ElevenLabsTTS(
        key="k", model_id="eleven_flash_v2_5", voice_id="v",
        base_url="wss://api.elevenlabs.io/v1", sample_rate=24000,
    )
    assert tts.sample_rate == 24000
    assert tts.to_config()["params"]["sample_rate"] == 24000


def test_google_tts_sample_rate_hertz_golden() -> None:
    # GoogleTTS uses `key` for the credentials JSON string (not project_id/location/adc_credentials_string).
    tts = GoogleTTS(
        key="{}", voice_name="en-US-Neural2-A", language_code="en-US", sample_rate_hertz=16000,
    )
    assert tts.sample_rate == 16000
    assert tts.to_config()["params"]["AudioConfig"]["sample_rate_hertz"] == 16000


def test_openai_tts_fixed_sample_rate_golden() -> None:
    assert OpenAITTS(voice="alloy").sample_rate == 24000


def test_openai_llm_golden() -> None:
    cfg = OpenAI(model="gpt-4o-mini").to_config()
    assert cfg["style"] == "openai"
    assert cfg["params"]["model"] == "gpt-4o-mini"
    assert cfg["url"] == "https://api.openai.com/v1/chat/completions"


def test_groq_golden() -> None:
    cfg = Groq(api_key="k", model="llama-3.3-70b-versatile",
               base_url="https://api.groq.com/openai/v1/chat/completions").to_config()
    assert cfg["url"] == "https://api.groq.com/openai/v1/chat/completions"
    assert cfg["style"] == "openai"
    assert cfg["params"]["model"] == "llama-3.3-70b-versatile"


def test_custom_llm_golden() -> None:
    cfg = CustomLLM(api_key="k", model="m", base_url="https://x/chat").to_config()
    assert cfg["vendor"] == "custom"
    assert cfg["url"] == "https://x/chat"


def test_vertexai_llm_golden() -> None:
    cfg = VertexAILLM(api_key="tok", project_id="proj", location="us-central1",
                      model="gemini-1.5-pro").to_config()
    assert cfg["api_key"] == "tok"
    assert "us-central1-aiplatform.googleapis.com" in cfg["url"]


def test_aliyun_llm_pins_vendor_golden() -> None:
    cfg = AliyunLLM(api_key="k", model="qwen-max",
                    base_url="https://dashscope.example/chat").to_config()
    assert cfg["vendor"] == "aliyun"
    assert cfg["api_key"] == "k"


def test_sensetime_avatar_camelcase_golden() -> None:
    # Verifies that the camelCase alias "appId" still works as constructor input
    # (populate_by_name=True means both the field name and alias are accepted at runtime).
    # Dict-unpack is used so mypy does not call-arg-check the alias keyword.
    cfg = SenseTimeAvatar(**{"agora_uid": "2", "appId": "app", "app_key": "key"}).to_config()
    assert cfg["vendor"] == "sensetime"
    assert cfg["params"]["appId"] == "app"


def test_heygen_avatar_golden() -> None:
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        cfg = HeyGenAvatar(api_key="k", quality="high", agora_uid="2").to_config()
    assert cfg["vendor"] == "heygen"


def test_fengming_rejects_kwargs() -> None:
    import pytest
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        FengmingSTT(unexpected="x")  # type: ignore[call-arg]
    assert FengmingSTT().to_config() == {"vendor": "fengming"}
