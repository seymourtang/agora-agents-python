from __future__ import annotations

import typing

from ..core.domain import Area
from .vendors.region import area_to_scope, validate_vendor_for_scope


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
