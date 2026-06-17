from __future__ import annotations

import typing
import typing_extensions

from ..core.domain import Area
from .agent import Agent
from .vendors.base import BaseAvatar, BaseLLM, BaseSTT, BaseTTS
from .vendors.cn import (
    AliyunLLM,
    BytedanceDuplexTTS,
    BytedanceLLM,
    BytedanceTTS,
    CosyVoiceTTS,
    DeepSeekLLM,
    FengmingSTT,
    MiniMaxTTS as MiniMaxCNTTS,
    MicrosoftSTT as MicrosoftCNSTT,
    MicrosoftTTS as MicrosoftCNTTS,
    SenseTimeAvatar,
    StepFunTTS,
    TencentLLM,
    TencentSTT,
    TencentTTS,
    XfyunBigModelSTT,
    XfyunDialectSTT,
    XfyunSTT,
)
from .vendors.stt import (
    AmazonSTT,
    AresSTT,
    AssemblyAISTT,
    DeepgramSTT,
    GoogleSTT,
    MicrosoftSTT,
    OpenAISTT,
    SarvamSTT,
    SpeechmaticsSTT,
)
from .vendors.llm import (
    AmazonBedrock,
    Anthropic,
    AzureOpenAI,
    CustomLLM,
    Dify,
    Gemini,
    Groq,
    OpenAI,
    VertexAILLM,
)
from .vendors.tts import (
    AmazonTTS,
    CartesiaTTS,
    DeepgramTTS,
    ElevenLabsTTS,
    FishAudioTTS,
    GoogleTTS,
    HumeAITTS,
    MicrosoftTTS,
    MiniMaxTTS,
    MurfTTS,
    OpenAITTS,
    RimeTTS,
    SarvamTTS,
)
from .vendors.avatar import AkoolAvatar, AnamAvatar, GenericAvatar, HeyGenAvatar, LiveAvatarAvatar

if typing.TYPE_CHECKING:
    from ..pool_client import Agora, AsyncAgora

CNSTT = typing.Union[TencentSTT, FengmingSTT, MicrosoftCNSTT, XfyunSTT, XfyunBigModelSTT, XfyunDialectSTT]
CNTTS = typing.Union[MiniMaxCNTTS, TencentTTS, BytedanceTTS, MicrosoftCNTTS, CosyVoiceTTS, BytedanceDuplexTTS, StepFunTTS]
CNLLM = typing.Union[AliyunLLM, BytedanceLLM, DeepSeekLLM, TencentLLM]
CNAvatar = SenseTimeAvatar

GlobalSTT = typing.Union[
    AresSTT,
    DeepgramSTT,
    MicrosoftSTT,
    OpenAISTT,
    GoogleSTT,
    AmazonSTT,
    AssemblyAISTT,
    SpeechmaticsSTT,
    SarvamSTT,
]
GlobalTTS = typing.Union[
    MicrosoftTTS,
    ElevenLabsTTS,
    MiniMaxTTS,
    MurfTTS,
    CartesiaTTS,
    OpenAITTS,
    HumeAITTS,
    RimeTTS,
    FishAudioTTS,
    GoogleTTS,
    AmazonTTS,
    SarvamTTS,
    DeepgramTTS,
]
GlobalLLM = typing.Union[
    OpenAI,
    AzureOpenAI,
    Anthropic,
    Gemini,
    Groq,
    VertexAILLM,
    AmazonBedrock,
    Dify,
    CustomLLM,
]
GlobalAvatar = typing.Union[AkoolAvatar, LiveAvatarAvatar, AnamAvatar, GenericAvatar, HeyGenAvatar]


class CNAgent(Agent):
    def with_stt(self, vendor: CNSTT) -> "CNAgent":
        return typing.cast("CNAgent", super().with_stt(typing.cast(BaseSTT, vendor)))

    def with_llm(self, vendor: CNLLM) -> "CNAgent":
        return typing.cast("CNAgent", super().with_llm(typing.cast(BaseLLM, vendor)))

    def with_tts(self, vendor: CNTTS) -> "CNAgent":
        return typing.cast("CNAgent", super().with_tts(typing.cast(BaseTTS, vendor)))

    def with_avatar(self, vendor: CNAvatar) -> "CNAgent":
        return typing.cast("CNAgent", super().with_avatar(typing.cast(BaseAvatar, vendor)))


class GlobalAgent(Agent):
    def with_stt(self, vendor: GlobalSTT) -> "GlobalAgent":
        return typing.cast("GlobalAgent", super().with_stt(typing.cast(BaseSTT, vendor)))

    def with_llm(self, vendor: GlobalLLM) -> "GlobalAgent":
        return typing.cast("GlobalAgent", super().with_llm(typing.cast(BaseLLM, vendor)))

    def with_tts(self, vendor: GlobalTTS) -> "GlobalAgent":
        return typing.cast("GlobalAgent", super().with_tts(typing.cast(BaseTTS, vendor)))

    def with_avatar(self, vendor: GlobalAvatar) -> "GlobalAgent":
        return typing.cast("GlobalAgent", super().with_avatar(typing.cast(BaseAvatar, vendor)))


RegionalAgent = typing.Union[CNAgent, GlobalAgent]
_GlobalArea = typing_extensions.Literal[Area.US, Area.EU, Area.AP]


@typing.overload
def AgoraAgent(*, client: "Agora[typing_extensions.Literal[Area.CN]]", **kwargs: typing.Any) -> CNAgent:
    ...


@typing.overload
def AgoraAgent(*, client: "Agora[_GlobalArea]", **kwargs: typing.Any) -> GlobalAgent:
    ...


@typing.overload
def AgoraAgent(*, client: "AsyncAgora[typing_extensions.Literal[Area.CN]]", **kwargs: typing.Any) -> CNAgent:
    ...


@typing.overload
def AgoraAgent(*, client: "AsyncAgora[_GlobalArea]", **kwargs: typing.Any) -> GlobalAgent:
    ...


def AgoraAgent(*, client: typing.Any, **kwargs: typing.Any) -> RegionalAgent:
    area_scope = getattr(client, "area_scope", None)
    agent_cls = CNAgent if area_scope == "cn" else GlobalAgent
    return agent_cls(client=client, **kwargs)
