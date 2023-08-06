from typing import Dict

from agent.commands.utils import prepare_message_to_send
from agent.constants import NOTIFY_CONTROL_CENTER
from agent.websocket.client import AgentWebSocketClient


def notify_control_center(body: Dict[str, str]) -> None:
    details_message = prepare_message_to_send(
        message_type=NOTIFY_CONTROL_CENTER, body=body
    )
    client = AgentWebSocketClient.get_instance()
    client.safe_message_send(details_message)
