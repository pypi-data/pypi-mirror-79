import threading
import time
from typing import Any, Dict

import pika
from pika.exceptions import AMQPConnectionError

from agent.communication.message_processor import process_message
from agent.config.properties import RABBITMQ_URL
from agent.constants import NOTIFY_CONTROL_CENTER, EXCHANGE, EXCHANGE_TYPE
from agent.rabbitmq import logger
from agent.services.utils import get_services_id_list


class RabbitMqClient:
    _instance = None

    @staticmethod
    def init():
        RabbitMqClient._instance = RabbitMqClient()
        return RabbitMqClient._instance

    @staticmethod
    def get_instance():
        if not RabbitMqClient._instance:
            return RabbitMqClient.init()
        return RabbitMqClient._instance

    def __init__(self):
        self._parameters = None
        self._connection = None
        self._channel = None
        self._exchange_declared = False
        self.thread = None

        url_params = pika.URLParameters(RABBITMQ_URL)
        self._parameters = pika.ConnectionParameters(
            host=url_params.host,
            port=url_params.port,
            credentials=url_params.credentials,
        )

        self._connect()

        if not self._exchange_declared:
            self.declare_exchange()

    def _connect(self):
        logger.info(f"Creating connection with parameters {self._parameters}")
        self._connection = self._wait_for_connection()
        self._channel = self._connection.channel()

    def _wait_for_connection(self):
        while True:
            try:
                return pika.BlockingConnection(self._parameters)
            except AMQPConnectionError as e:
                logger.error(e)
                logger.error(
                    "Cannot establish connection with RabbitMQ. Trying to reconnect..."
                )
                time.sleep(3)

    @property
    def channel(self):
        if self._connection is None:
            self._connect()

        if self._channel is None or not self._channel.is_open:
            logger.info("Trying to reconnect RabbitMQ...")
            self._connect()

        return self._channel

    def declare_exchange(self):
        logger.info("Declare exchange")
        self.channel.exchange_declare(exchange=EXCHANGE, exchange_type=EXCHANGE_TYPE)
        self._exchange_declared = True

    def declare_queue(self, routing_key: str) -> None:
        self.channel.queue_declare(queue=routing_key)
        self.channel.queue_bind(
            exchange=EXCHANGE, queue=routing_key, routing_key=routing_key
        )
        logger.info(f"Declared queue with topic: {routing_key}")

    def start_consuming_messages_to_control_center(self):
        self.declare_queue(NOTIFY_CONTROL_CENTER)
        self.channel.basic_consume(
            queue=NOTIFY_CONTROL_CENTER,
            auto_ack=True,
            on_message_callback=self.dispatch_message,
        )
        self.thread = threading.Thread(target=lambda: self.channel.start_consuming())
        self.thread.start()
        logger.info("Waiting for messages...")

    @staticmethod
    def dispatch_message(channel_id, method, properties, body):
        logger.info(f"Received message: {body}")
        process_message(body)

    def publish_message(self, message: Dict[str, Any]):
        self.channel.basic_publish(
            exchange=EXCHANGE,
            routing_key=message["nodeServiceId"],
            body=message,
            properties=pika.BasicProperties(
                content_type="application/json", type=message["messageType"]
            ),
        )
        logger.info(f"Message sent to RabbitMQ: {message}")

    def start_rabbitmq_client(self) -> None:
        for service_id in get_services_id_list():
            self.get_instance().declare_queue(service_id)
        self.get_instance().start_consuming_messages_to_control_center()
