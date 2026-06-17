"""Shared helpers for AgentKit unit tests."""

from agora_agent import AgentClient, Area

TEST_APP_ID = "0" * 32
TEST_APP_CERTIFICATE = "1" * 32


def test_client(area: Area = Area.US) -> AgentClient:
    return AgentClient(area=area, app_id=TEST_APP_ID, app_certificate=TEST_APP_CERTIFICATE)
