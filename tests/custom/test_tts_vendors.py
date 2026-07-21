import pytest

from agora_agent import AmazonTTS, CartesiaTTS, CredentialMode, DeepgramTTS, ElevenLabsTTS, FishAudioTTS, GoogleTTS, HumeAITTS, MicrosoftTTS, MiniMaxTTS, MurfTTS, OpenAITTS, RimeTTS, SarvamTTS
from agora_agent.agents.types.start_agents_request_properties import StartAgentsRequestProperties
from agora_agent.core.jsonable_encoder import jsonable_encoder
from agora_agent.core.pydantic_utilities import parse_obj_as


def test_tts_vendor_params_match_generated_core_shapes() -> None:
    assert MicrosoftTTS(key="ms-key", region="eastus", voice_name="en-US-JennyNeural").to_config()["params"] == {
        "key": "ms-key",
        "region": "eastus",
        "voice_name": "en-US-JennyNeural",
    }

    assert AmazonTTS(access_key="access", secret_key="secret", region="us-east-1", voice_id="Joanna", engine="neural").to_config()["params"] == {
        "aws_access_key_id": "access",
        "aws_secret_access_key": "secret",
        "region_name": "us-east-1",
        "voice": "Joanna",
        "engine": "neural",
    }

    assert GoogleTTS(key="{}", voice_name="en-US-JennyNeural", language_code="en-US", sample_rate_hertz=24000).to_config()["params"] == {
        "credentials": "{}",
        "VoiceSelectionParams": {"name": "en-US-JennyNeural", "language_code": "en-US"},
        "AudioConfig": {"sample_rate_hertz": 24000},
    }

    assert CartesiaTTS(api_key="cartesia-key", voice_id="voice", model_id="sonic-2", sample_rate=24000).to_config()["params"] == {
        "api_key": "cartesia-key",
        "model_id": "sonic-2",
        "voice": {"mode": "id", "id": "voice"},
        "output_format": {"container": "raw", "sample_rate": 24000},
    }

    assert RimeTTS(key="rime-key", speaker="speaker", model_id="mist").to_config()["params"] == {
        "api_key": "rime-key",
        "speaker": "speaker",
        "modelId": "mist",
    }

    assert FishAudioTTS(key="fish-key", reference_id="ref", backend="speech-1.5").to_config()["params"] == {
        "api_key": "fish-key",
        "reference_id": "ref",
        "backend": "speech-1.5",
    }

    assert ElevenLabsTTS(key="eleven-key", model_id="eleven_flash_v2_5", voice_id="voice", base_url="wss://api.elevenlabs.io/v1").to_config()["params"] == {
        "key": "eleven-key",
        "base_url": "wss://api.elevenlabs.io/v1",
        "model_id": "eleven_flash_v2_5",
        "voice_id": "voice",
    }

    assert DeepgramTTS(api_key="deepgram-key", model="aura-2-thalia-en", base_url="wss://api.deepgram.com/v1/speak", sample_rate=24000, additional_params={"encoding": "linear16"}).to_config()["params"] == {
        "api_key": "deepgram-key",
        "model": "aura-2-thalia-en",
        "base_url": "wss://api.deepgram.com/v1/speak",
        "sample_rate": 24000,
        "encoding": "linear16",
    }

    assert OpenAITTS(api_key="openai-key", voice="coral", model="gpt-4o-mini-tts", base_url="https://api.openai.com/v1", instructions="speak clearly").to_config()["params"] == {
        "voice": "coral",
        "api_key": "openai-key",
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-4o-mini-tts",
        "instructions": "speak clearly",
    }

    assert OpenAITTS(voice="coral").to_config()["params"] == {
        "voice": "coral",
    }

    assert HumeAITTS(key="hume-key", voice_id="voice", provider="CUSTOM_VOICE").to_config()["params"] == {
        "key": "hume-key",
        "voice_id": "voice",
        "provider": "CUSTOM_VOICE",
    }

    assert MiniMaxTTS(key="minimax-key", group_id="group", model="speech-02-turbo", voice_id="voice").to_config()["params"] == {
        "model": "speech-02-turbo",
        "key": "minimax-key",
        "group_id": "group",
        "voice_setting": {"voice_id": "voice"},
    }

    assert MiniMaxTTS(
        key="minimax-key",
        group_id="group",
        model="speech-01-turbo",
        voice_id="female-shaonv",
        speed=1,
        vol=1,
        pitch=0,
        emotion="happy",
        latex_read=True,
        english_normalization=True,
        sample_rate=16000,
        pronunciation_dict={"tone": ["example/(ex1)(am2)(ple0)", "message/(mes1)(sage4)"]},
        language_boost="auto",
    ).to_config()["params"] == {
        "model": "speech-01-turbo",
        "key": "minimax-key",
        "group_id": "group",
        "voice_setting": {
            "voice_id": "female-shaonv",
            "speed": 1,
            "vol": 1,
            "pitch": 0,
            "emotion": "happy",
            "latex_read": True,
            "english_normalization": True,
        },
        "audio_setting": {"sample_rate": 16000},
        "pronunciation_dict": {"tone": ["example/(ex1)(am2)(ple0)", "message/(mes1)(sage4)"]},
        "language_boost": "auto",
    }

    assert SarvamTTS(key="sarvam-key", speaker="anushka", target_language_code="en-IN", sample_rate=24000).to_config()["params"] == {
        "api_subscription_key": "sarvam-key",
        "speaker": "anushka",
        "target_language_code": "en-IN",
        "sample_rate": 24000,
    }

    assert MurfTTS(
        key="murf-key",
        voice_id="Ariana",
        base_url="wss://murf.example/ws",
        locale="en-US",
        rate=0,
        pitch=0,
        model="FALCON",
        sample_rate=24000,
    ).to_config()["params"] == {
        "api_key": "murf-key",
        "base_url": "wss://murf.example/ws",
        "voiceId": "Ariana",
        "locale": "en-US",
        "rate": 0,
        "pitch": 0,
        "model": "FALCON",
        "sample_rate": 24000,
    }

    assert MurfTTS(key="murf-key").to_config()["params"] == {
        "api_key": "murf-key",
    }


def test_tts_managed_mode_validation_matches_core_shapes() -> None:
    with pytest.raises(Exception, match="OpenAITTS requires api_key"):
        OpenAITTS(voice="coral", model="tts-1-hd")

    with pytest.raises(Exception, match="MiniMaxTTS requires key unless using a supported Agora-managed model|MiniMaxTTS requires exactly one of voice_id or timber_weights"):
        MiniMaxTTS(model="unsupported-model")

    with pytest.raises(Exception, match="MiniMaxTTS requires exactly one of voice_id or timber_weights"):
        MiniMaxTTS(key="minimax-key", group_id="group", model="speech-01-turbo")

    with pytest.raises(Exception, match="MiniMaxTTS requires exactly one of voice_id or timber_weights"):
        MiniMaxTTS(
            key="minimax-key",
            group_id="group",
            model="speech-01-turbo",
            voice_id="voice",
            timber_weights=[{"voice_id": "voice-2", "weight": 1}],
        )


def test_rime_tts_managed_credential_mode_params() -> None:
    config = RimeTTS(
        credential_mode=CredentialMode.MANAGED,
        base_url="wss://users.rime.ai/ws",
        model_id="mist",
    ).to_config()
    assert config == {
        "vendor": "rime",
        "credential_mode": "managed",
        "params": {
            "modelId": "mist",
            "base_url": "wss://users.rime.ai/ws",
        },
    }


@pytest.mark.parametrize("credential_mode", [None, CredentialMode.BYOK])
def test_rime_tts_byok_credential_mode_params(credential_mode) -> None:
    config = RimeTTS(
        credential_mode=credential_mode,
        key="rime-key",
        speaker="speaker",
        model_id="mist",
    ).to_config()
    expected = {
        "modelId": "mist",
        "api_key": "rime-key",
        "speaker": "speaker",
    }
    assert config["params"] == expected
    if credential_mode is None:
        assert "credential_mode" not in config
    else:
        assert config["credential_mode"] == credential_mode


@pytest.mark.parametrize(
    ("kwargs", "missing"),
    [
        ({"model_id": "mist"}, "base_url"),
        ({"base_url": "wss://users.rime.ai/ws"}, "model_id"),
        ({}, "base_url, model_id"),
    ],
)
def test_rime_tts_managed_mode_requires_base_url_and_model_id(kwargs: dict, missing: str) -> None:
    with pytest.raises(Exception, match=rf"RimeTTS requires {missing} for credential_mode='managed'"):
        RimeTTS(credential_mode=CredentialMode.MANAGED, **kwargs)


@pytest.mark.parametrize("credential_mode", [None, CredentialMode.BYOK])
@pytest.mark.parametrize(
    ("kwargs", "missing"),
    [
        ({"speaker": "speaker", "model_id": "mist"}, "key"),
        ({"key": "rime-key", "model_id": "mist"}, "speaker"),
        ({"key": "rime-key", "speaker": "speaker"}, "model_id"),
    ],
)
def test_rime_tts_byok_mode_requires_key_speaker_and_model_id(
    credential_mode,
    kwargs: dict,
    missing: str,
) -> None:
    with pytest.raises(Exception, match=rf"RimeTTS requires {missing}"):
        RimeTTS(credential_mode=credential_mode, **kwargs)


def test_rime_tts_rejects_unknown_credential_mode() -> None:
    with pytest.raises(Exception, match="credential_mode"):
        RimeTTS(credential_mode="unknown", base_url="wss://users.rime.ai/ws", model_id="mist")  # type: ignore[arg-type]


def test_tts_wire_serialization_applies_fern_aliases() -> None:
    """Verify alias-sensitive TTS params keep the exact provider wire keys."""
    _BASE = dict(channel="ch", token="tok", agent_rtc_uid="1", remote_rtc_uids=["100"])

    google_config = GoogleTTS(
        key="{}", voice_name="en-US-JennyNeural", language_code="en-US", sample_rate_hertz=24000
    ).to_config()
    assert "VoiceSelectionParams" in google_config["params"]
    google_wire = jsonable_encoder(parse_obj_as(StartAgentsRequestProperties, {**_BASE, "tts": google_config}))
    google_params = google_wire["tts"]["params"]
    assert "VoiceSelectionParams" in google_params, f"wire missing VoiceSelectionParams, got: {list(google_params)}"
    assert "voice_selection_params" not in google_params
    assert "AudioConfig" in google_params
    assert "audio_config" not in google_params

    rime_config = RimeTTS(key="rime-key", speaker="speaker", model_id="mist").to_config()
    assert "modelId" in rime_config["params"]
    rime_wire = jsonable_encoder(parse_obj_as(StartAgentsRequestProperties, {**_BASE, "tts": rime_config}))
    rime_params = rime_wire["tts"]["params"]
    assert "modelId" in rime_params, f"wire missing modelId, got: {list(rime_params)}"
    assert "model_id" not in rime_params

    managed_rime_config = RimeTTS(
        credential_mode=CredentialMode.MANAGED,
        base_url="wss://users.rime.ai/ws",
        model_id="mist",
    ).to_config()
    managed_rime_wire = jsonable_encoder(
        parse_obj_as(StartAgentsRequestProperties, {**_BASE, "tts": managed_rime_config})
    )
    assert managed_rime_wire["tts"] == {
        "vendor": "rime",
        "credential_mode": "managed",
        "params": {
            "modelId": "mist",
            "base_url": "wss://users.rime.ai/ws",
        },
    }

    murf_config = MurfTTS(key="murf-key", voice_id="Ariana").to_config()
    assert "voiceId" in murf_config["params"]
    murf_wire = jsonable_encoder(parse_obj_as(StartAgentsRequestProperties, {**_BASE, "tts": murf_config}))
    murf_params = murf_wire["tts"]["params"]
    assert "voiceId" in murf_params, f"wire missing voiceId, got: {list(murf_params)}"
    assert murf_params["voiceId"] == "Ariana"
