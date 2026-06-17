from __future__ import annotations

import typing

from ..core.domain import Area
from .vendors.region import area_to_scope, validate_vendor_for_scope

_CN_VENDOR_CLASS_NAMES = {
    "asr": {
        "agora_agent.agentkit.vendors.cn.TencentSTT",
        "agora_agent.agentkit.vendors.cn.FengmingSTT",
        "agora_agent.agentkit.vendors.cn.MicrosoftSTT",
        "agora_agent.agentkit.vendors.cn.XfyunSTT",
        "agora_agent.agentkit.vendors.cn.XfyunBigModelSTT",
        "agora_agent.agentkit.vendors.cn.XfyunDialectSTT",
    },
    "llm": {
        "agora_agent.agentkit.vendors.cn.AliyunLLM",
        "agora_agent.agentkit.vendors.cn.BytedanceLLM",
        "agora_agent.agentkit.vendors.cn.DeepSeekLLM",
        "agora_agent.agentkit.vendors.cn.TencentLLM",
    },
    "tts": {
        "agora_agent.agentkit.vendors.cn.MiniMaxTTS",
        "agora_agent.agentkit.vendors.cn.TencentTTS",
        "agora_agent.agentkit.vendors.cn.BytedanceTTS",
        "agora_agent.agentkit.vendors.cn.MicrosoftTTS",
        "agora_agent.agentkit.vendors.cn.CosyVoiceTTS",
        "agora_agent.agentkit.vendors.cn.BytedanceDuplexTTS",
        "agora_agent.agentkit.vendors.cn.StepFunTTS",
    },
    "avatar": {
        "agora_agent.agentkit.vendors.cn.SenseTimeAvatar",
    },
}

_GLOBAL_VENDOR_CLASS_NAMES = {
    "asr": {
        "agora_agent.agentkit.vendors.stt.AresSTT",
        "agora_agent.agentkit.vendors.stt.DeepgramSTT",
        "agora_agent.agentkit.vendors.stt.MicrosoftSTT",
        "agora_agent.agentkit.vendors.stt.OpenAISTT",
        "agora_agent.agentkit.vendors.stt.GoogleSTT",
        "agora_agent.agentkit.vendors.stt.AmazonSTT",
        "agora_agent.agentkit.vendors.stt.AssemblyAISTT",
        "agora_agent.agentkit.vendors.stt.SpeechmaticsSTT",
        "agora_agent.agentkit.vendors.stt.SarvamSTT",
    },
    "llm": {
        "agora_agent.agentkit.vendors.llm.OpenAI",
        "agora_agent.agentkit.vendors.llm.AzureOpenAI",
        "agora_agent.agentkit.vendors.llm.Anthropic",
        "agora_agent.agentkit.vendors.llm.Gemini",
        "agora_agent.agentkit.vendors.llm.Groq",
        "agora_agent.agentkit.vendors.llm.VertexAILLM",
        "agora_agent.agentkit.vendors.llm.AmazonBedrock",
        "agora_agent.agentkit.vendors.llm.Dify",
        "agora_agent.agentkit.vendors.llm.CustomLLM",
    },
    "tts": {
        "agora_agent.agentkit.vendors.tts.MicrosoftTTS",
        "agora_agent.agentkit.vendors.tts.ElevenLabsTTS",
        "agora_agent.agentkit.vendors.tts.MiniMaxTTS",
        "agora_agent.agentkit.vendors.tts.MurfTTS",
        "agora_agent.agentkit.vendors.tts.CartesiaTTS",
        "agora_agent.agentkit.vendors.tts.OpenAITTS",
        "agora_agent.agentkit.vendors.tts.HumeAITTS",
        "agora_agent.agentkit.vendors.tts.RimeTTS",
        "agora_agent.agentkit.vendors.tts.FishAudioTTS",
        "agora_agent.agentkit.vendors.tts.GoogleTTS",
        "agora_agent.agentkit.vendors.tts.AmazonTTS",
        "agora_agent.agentkit.vendors.tts.SarvamTTS",
        "agora_agent.agentkit.vendors.tts.DeepgramTTS",
    },
    "avatar": {
        "agora_agent.agentkit.vendors.avatar.AkoolAvatar",
        "agora_agent.agentkit.vendors.avatar.LiveAvatarAvatar",
        "agora_agent.agentkit.vendors.avatar.AnamAvatar",
        "agora_agent.agentkit.vendors.avatar.GenericAvatar",
        "agora_agent.agentkit.vendors.avatar.HeyGenAvatar",
    },
}


def _validate_vendor_instance_for_area(category: str, vendor: typing.Any, area: Area) -> None:
    class_name = f"{vendor.__class__.__module__}.{vendor.__class__.__name__}"
    if area_to_scope(area) == "cn":
        allowed = _CN_VENDOR_CLASS_NAMES.get(category, set())
        scope = "cn"
    else:
        allowed = _GLOBAL_VENDOR_CLASS_NAMES.get(category, set())
        scope = "global"
    if class_name not in allowed:
        allowed_joined = ", ".join(sorted(allowed))
        raise ValueError(
            f"{category} vendor '{class_name}' is not available for area scope '{scope}'. "
            f"Supported {category} vendor classes for this scope: {allowed_joined}"
        )


def validate_agent_region_vendor_config(category: str, config: typing.Mapping[str, typing.Any], area: Area) -> None:
    vendor = config.get("vendor")
    if vendor:
        validate_vendor_for_scope(category, typing.cast(str, vendor), area_to_scope(area))


def validate_agent_region_vendor(category: str, vendor: typing.Any, config: typing.Mapping[str, typing.Any], area: Area) -> None:
    _validate_vendor_instance_for_area(category, vendor, area)
    validate_agent_region_vendor_config(category, config, area)


def validate_agent_region_compatibility(agent: typing.Any, area: Area) -> None:
    scope = area_to_scope(area)

    stt = getattr(agent, "stt", None)
    if isinstance(stt, dict) and stt.get("vendor"):
        validate_vendor_for_scope("asr", stt["vendor"], scope)

    tts = getattr(agent, "tts", None)
    if isinstance(tts, dict) and tts.get("vendor"):
        validate_vendor_for_scope("tts", tts["vendor"], scope)

    llm = getattr(agent, "llm", None)
    if isinstance(llm, dict) and llm.get("vendor"):
        validate_vendor_for_scope("llm", llm["vendor"], scope)

    avatar = getattr(agent, "avatar", None)
    if isinstance(avatar, dict) and avatar.get("enable") is not False and avatar.get("vendor"):
        validate_vendor_for_scope("avatar", avatar["vendor"], scope)
