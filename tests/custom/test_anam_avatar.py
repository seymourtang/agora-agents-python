import pytest

from agora_agent.agentkit import validate_avatar_config
from agora_agent.agentkit.avatar_types import is_anam_avatar
from agora_agent.agentkit.vendors import AnamAvatar


def test_anam_avatar_to_config_shape() -> None:
    config = AnamAvatar(
        api_key="anam-key",
        avatar_id="anam-avatar",
    ).to_config()

    assert config == {
        "enable": True,
        "vendor": "anam",
        "params": {
            "api_key": "anam-key",
            "avatar_id": "anam-avatar",
        },
    }
    assert is_anam_avatar(config)


@pytest.mark.parametrize(
    ("params", "message"),
    [
        ({}, "Anam avatar requires api_key"),
        ({"api_key": "key"}, "Anam avatar requires avatar_id"),
    ],
)
def test_validate_avatar_config_rejects_incomplete_anam(
    params: dict, message: str
) -> None:
    with pytest.raises(ValueError, match=message):
        validate_avatar_config({"vendor": "anam", "params": params})
